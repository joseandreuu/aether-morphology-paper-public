import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score


def infer_label_from_split(split_series: pd.Series) -> np.ndarray:
    s = split_series.astype(str).str.lower()
    return s.isin(["abnormal", "fault", "anomaly", "anomalous", "defect", "broken"]).astype(int).to_numpy()


def get_scores_and_labels(df: pd.DataFrame, score_col: str = "S_raw"):
    if score_col not in df.columns:
        raise ValueError(f"Missing score col '{score_col}'. Have: {df.columns.tolist()}")

    if "label" in df.columns:
        y = df["label"].astype(int).to_numpy()
    elif "y" in df.columns:
        y = df["y"].astype(int).to_numpy()
    elif "split" in df.columns:
        y = infer_label_from_split(df["split"])
    else:
        raise ValueError("No label/split column found to infer ground truth.")

    s = df[score_col].astype(float).to_numpy()

    auc = roc_auc_score(y, s)
    if auc < 0.5:
        s = -s
        auc = 1 - auc

    fpr, tpr, _ = roc_curve(y, s)
    return fpr, tpr, auc


def file_level(df: pd.DataFrame, score_col="S_raw"):
    if "file" not in df.columns:
        raise ValueError("Need column 'file' for file-level aggregation")

    g = df.groupby("file", as_index=False)[score_col].mean().rename(columns={score_col: "score_file"})

    if "label" in df.columns:
        lab = df.groupby("file", as_index=False)["label"].first().rename(columns={"label": "label_file"})
        g = g.merge(lab, on="file", how="left")
        y = g["label_file"].astype(int).to_numpy()
    elif "y" in df.columns:
        lab = df.groupby("file", as_index=False)["y"].first().rename(columns={"y": "label_file"})
        g = g.merge(lab, on="file", how="left")
        y = g["label_file"].astype(int).to_numpy()
    elif "split" in df.columns:
        lab = df.groupby("file", as_index=False)["split"].first()
        y = infer_label_from_split(lab["split"])
        g["label_file"] = y
    else:
        raise ValueError("Need split/label/y for file-level labels")

    s = g["score_file"].astype(float).to_numpy()
    auc = roc_auc_score(y, s)
    if auc < 0.5:
        s = -s
        auc = 1 - auc

    fpr, tpr, _ = roc_curve(y, s)
    return fpr, tpr, auc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cwru", required=True, help="Path to cwru_scored_windows.parquet")
    ap.add_argument("--vsb", required=True, help="Path to vsb_scored_windows.parquet")
    ap.add_argument("--out-pdf", required=True)
    ap.add_argument("--out-png", required=True)
    ap.add_argument("--score-col", default="S_raw")
    args = ap.parse_args()

    cwru_df = pd.read_parquet(args.cwru)
    vsb_df = pd.read_parquet(args.vsb)

    # Window-level
    cwru_fpr_w, cwru_tpr_w, cwru_auc_w = get_scores_and_labels(cwru_df, args.score_col)
    vsb_fpr_w,  vsb_tpr_w,  vsb_auc_w  = get_scores_and_labels(vsb_df,  args.score_col)

    # File-level
    cwru_fpr_f, cwru_tpr_f, cwru_auc_f = file_level(cwru_df, args.score_col)
    vsb_fpr_f,  vsb_tpr_f,  vsb_auc_f  = file_level(vsb_df,  args.score_col)

    print(f"CWRU AUC window: {cwru_auc_w:.4f}")
    print(f"CWRU AUC file  : {cwru_auc_f:.4f}")
    print(f"VSB  AUC window: {vsb_auc_w:.4f}")
    print(f"VSB  AUC file  : {vsb_auc_f:.4f}")

    # Plot
    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm",
        "font.size": 9,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })

    fig = plt.figure(figsize=(6.75, 2.6))  # APS-ish wide figure
    ax1 = plt.subplot(1, 2, 1)
    ax2 = plt.subplot(1, 2, 2)

    # (a) Rotating machinery
    ax1.plot(cwru_fpr_f, cwru_tpr_f, linewidth=2.0,
             label=f"File-level (mean over windows), AUC={cwru_auc_f:.3f}")
    ax1.plot(cwru_fpr_w, cwru_tpr_w, linewidth=1.3, linestyle="--",
             label=f"Window-level, AUC={cwru_auc_w:.3f}")
    ax1.plot([0, 1], [0, 1], "--", linewidth=1)
    ax1.set_title("(a) Rotating machinery")
    ax1.set_xlabel("False Positive Rate")
    ax1.set_ylabel("True Positive Rate")
    ax1.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.22), fontsize=8)

    # (b) Electrical control
    ax2.plot(vsb_fpr_f, vsb_tpr_f, linewidth=2.0,
             label=f"File-level (mean over windows), AUC={vsb_auc_f:.3f}")
    ax2.plot(vsb_fpr_w, vsb_tpr_w, linewidth=1.3, linestyle="--",
             label=f"Window-level, AUC={vsb_auc_w:.3f}")
    ax2.plot([0, 1], [0, 1], "--", linewidth=1)
    ax2.set_title("(b) Electrical control (VSB)")
    ax2.set_xlabel("False Positive Rate")
    ax2.set_ylabel("True Positive Rate")
    ax2.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.22), fontsize=8)

    fig.subplots_adjust(bottom=0.28, wspace=0.30)

    out_pdf = Path(args.out_pdf)
    out_png = Path(args.out_png)
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    out_png.parent.mkdir(parents=True, exist_ok=True)

    fig.savefig(out_pdf, bbox_inches="tight", pad_inches=0.02)
    fig.savefig(out_png, dpi=600, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)

    print("Saved:", out_pdf)
    print("Saved:", out_png)


if __name__ == "__main__":
    main()
