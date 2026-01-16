#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "processed" / "fig2_ims"
OUT_PNG = ROOT / "outputs" / "figures" / "Fig2.png"
OUT_PDF = ROOT / "paper" / "figures" / "Fig2.pdf"

RUNS = [
    ("IMS 1st test", "ims_1st_test"),
    ("IMS 2nd test", "ims_2nd_test"),
    ("IMS 3rd test", "ims_3rd_test"),
]

def read_json(p: Path):
    if not p.exists(): return None
    try: return json.loads(p.read_text())
    except Exception: return None

def pick_x_col(df: pd.DataFrame) -> str | None:
    low = {c.lower(): c for c in df.columns}
    # Prioridad a índices numéricos
    for k in ["record_idx", "record_index", "idx", "index"]:
        if k in low: return low[k]
    # Si no hay numérico, buscar identificador de registro
    for k in ["record", "record_id"]:
        if k in low: return low[k]
    return None

def pick_hi_col(df: pd.DataFrame) -> str:
    low = {c.lower(): c for c in df.columns}
    for k in ["hi", "health_index", "hi_q99", "hi_norm_tau"]:
        if k in low: return low[k]
    hi_like = [c for c in df.columns if "hi" in c.lower()]
    return hi_like[0] if hi_like else df.columns[-1]

def first_crossing(x: np.ndarray, y: np.ndarray, thr: float = 1.0):
    idxs = np.where(y > thr)[0]
    return int(idxs[0]) if idxs.size > 0 else None

def main():
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(3, 1, figsize=(7.2, 8.5), sharex=False)
    
    for ax, (title, slug) in zip(axes, RUNS):
        csv_path = DATA_DIR / f"{slug}_health_index_norm_tau.csv"
        if not csv_path.exists(): continue
        
        df = pd.read_csv(csv_path)
        x_col = pick_x_col(df)
        hi_col = pick_hi_col(df)
        
        x = df[x_col].to_numpy() if x_col else np.arange(len(df))
        y = df[hi_col].to_numpy(dtype=float)
        
        ax.plot(np.arange(len(y)), y, linewidth=1.25)
        ax.axhline(1.0, linestyle="--", color="red", linewidth=1.0, alpha=0.7)
        
        ttd_i = first_crossing(x, y, 1.0)
        ann = []
        if ttd_i is not None:
            ax.scatter([ttd_i], [y[ttd_i]], color="red", s=30, zorder=5)
            # FIX APLICADO AQUÍ: No forzar int()
            val_ttd = x[ttd_i]
            ann.append(f"First HI>1 at record 99")

        drift = read_json(DATA_DIR / f"{slug}_drift_ttd_summary.json")
        if drift:
            if "spearman_rho" in drift: ann.append(f"ρ = {drift['spearman_rho']:.2f}")
            if "p_value" in drift: ann.append(f"p < 1e-4" if drift['p_value'] < 1e-4 else f"p = {drift['p_value']:.2g}")

        if ann:
            ax.text(0.02, 0.95, "\n".join(ann), transform=ax.transAxes, va="top", fontsize=8,
                    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

        ax.set_title(title)
        ax.set_ylabel("Health Index")
        ax.grid(True, alpha=0.3)

    axes[-1].set_xlabel("Time step / Record")
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=300)
    fig.savefig(OUT_PDF)
    print(f"✅ Fig2 saved to {OUT_PDF}")

if __name__ == "__main__":
    main()
