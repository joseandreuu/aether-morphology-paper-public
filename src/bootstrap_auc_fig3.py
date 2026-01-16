#!/usr/bin/env python3
"""
Bootstrap CIs for Fig.3 AUC (window-level and file-level) using derived artifacts.

Expected input:
- data/processed/fig3/cwru_scored_windows.parquet

We try to infer column names robustly. If inference fails, the script prints
available columns and exits with a clear error.

Outputs:
- paper/tables/fig3_auc_bootstrap.json
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score


ROOT = Path(__file__).resolve().parents[1]
IN_PARQUET = ROOT / "data" / "processed" / "fig3" / "cwru_scored_windows.parquet"
OUT_JSON = ROOT / "paper" / "tables" / "fig3_auc_bootstrap.json"


LABEL_CANDIDATES = [
    "label", "y", "target", "is_anomaly", "anomaly", "fault", "is_fault", "class",
    "split",
]
SCORE_CANDIDATES = [
    "S_z", "S_raw",
    "score", "anomaly_score", "S", "s", "mahalanobis", "dist", "distance",
]
FILEID_CANDIDATES = [
    "file", "file_id", "recording", "recording_id", "fname", "filename", "path"
]


@dataclass
class Cols:
    label: str
    score: str
    file_id: Optional[str] = None


def _pick_column(df: pd.DataFrame, candidates: list[str], required: bool = True) -> Optional[str]:
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in cols_lower:
            return cols_lower[cand.lower()]
    if required:
        raise KeyError(f"Could not infer required column. Tried: {candidates}")
    return None


def infer_columns(df: pd.DataFrame) -> Cols:
    label = _pick_column(df, LABEL_CANDIDATES, required=True)

    # If the label is encoded as a string split column (normal/abnormal), derive a binary target.
    if label == "split":
        s = df["split"].astype(str).str.lower().str.strip()
        df["_y"] = (s == "abnormal").astype(int)
        label = "_y"
    score = _pick_column(df, SCORE_CANDIDATES, required=True)
    file_id = _pick_column(df, FILEID_CANDIDATES, required=False)

    # Validate label binary
    y = df[label].values
    uniq = np.unique(y)
    if len(uniq) > 2:
        raise ValueError(
            f"Label column '{label}' does not look binary (unique={uniq[:10]}...). "
            f"Please rename/provide a binary label."
        )
    return Cols(label=label, score=score, file_id=file_id)


def auc_point_estimates(df: pd.DataFrame, cols: Cols) -> Tuple[float, float]:
    y = df[cols.label].astype(int).values
    s = df[cols.score].astype(float).values
    auc_win = roc_auc_score(y, s)

    if cols.file_id is None:
        raise ValueError(
            "Cannot compute file-level AUC: could not infer a file identifier column. "
            f"Available columns: {list(df.columns)}"
        )

    g = df.groupby(cols.file_id, dropna=False, sort=False).agg(
        y=(cols.label, "max"),
        s=(cols.score, "mean"),
    ).reset_index(drop=True)

    auc_file = roc_auc_score(g["y"].astype(int).values, g["s"].astype(float).values)
    return auc_win, auc_file


def bootstrap_auc(
    y: np.ndarray,
    s: np.ndarray,
    n_boot: int = 2000,
    seed: int = 0,
) -> Tuple[float, Tuple[float, float]]:
    rng = np.random.default_rng(seed)
    n = len(y)
    aucs = np.empty(n_boot, dtype=float)

    for b in range(n_boot):
        idx = rng.integers(0, n, size=n)
        # Ensure both classes present; if not, resample (rare but possible)
        for _ in range(25):
            yy = y[idx]
            if len(np.unique(yy)) == 2:
                break
            idx = rng.integers(0, n, size=n)
        yy = y[idx]
        ss = s[idx]
        aucs[b] = roc_auc_score(yy, ss)

    point = roc_auc_score(y, s)
    lo, hi = np.quantile(aucs, [0.025, 0.975])
    return point, (float(lo), float(hi))


def main() -> None:
    if not IN_PARQUET.exists():
        raise FileNotFoundError(f"Missing input parquet: {IN_PARQUET}")

    df = pd.read_parquet(IN_PARQUET)

    try:
        cols = infer_columns(df)
    except Exception as e:
        print("ERROR inferring columns:", e)
        print("Available columns:", list(df.columns))
        raise

    auc_win, auc_file = auc_point_estimates(df, cols)

    # Window-level bootstrap at window unit
    y_win = df[cols.label].astype(int).values
    s_win = df[cols.score].astype(float).values
    p_win, (lo_win, hi_win) = bootstrap_auc(y_win, s_win, n_boot=2000, seed=123)

    # File-level bootstrap at file unit (after aggregation)
    g = df.groupby(cols.file_id, dropna=False, sort=False).agg(
        y=(cols.label, "max"),
        s=(cols.score, "mean"),
    ).reset_index(drop=True)
    y_file = g["y"].astype(int).values
    s_file = g["s"].astype(float).values
    p_file, (lo_file, hi_file) = bootstrap_auc(y_file, s_file, n_boot=2000, seed=456)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "input": str(IN_PARQUET.relative_to(ROOT)),
        "columns": {"label": cols.label, "score": cols.score, "file_id": cols.file_id},
        "n_windows": int(len(df)),
        "n_files": int(len(g)),
        "auc_window": {"point": float(auc_win), "bootstrap_point": float(p_win), "ci95": [lo_win, hi_win]},
        "auc_file": {"point": float(auc_file), "bootstrap_point": float(p_file), "ci95": [lo_file, hi_file]},
        "bootstrap": {"B": 2000, "seeds": {"win": 123, "file": 456}},
    }

    OUT_JSON.write_text(json.dumps(payload, indent=2))
    print(f"Wrote: {OUT_JSON}")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
