import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scores-csv", required=True, help="CSV with per-file scores (expects columns: file, score_mean)")
    ap.add_argument("--metrics-json", required=True, help="JSON with tau threshold (expects key: tau)")
    ap.add_argument("--out-pdf", required=True)
    ap.add_argument("--out-png", required=True)
    ap.add_argument("--quantile-label", default=r"99.9\%", help=r'Legend label, e.g. "99.9\\%"')
    ap.add_argument("--dpi", type=int, default=600)
    args = ap.parse_args()

    # APS-ish typography
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "mathtext.fontset": "cm",
        "font.size": 9,
        "axes.linewidth": 0.8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        # IMPORTANT: avoid weird dash caps in PDF viewers
        "lines.dash_capstyle": "butt",
        "lines.solid_capstyle": "butt",
    })

    scores = pd.read_csv(args.scores_csv)
    with open(args.metrics_json, "r") as f:
        metrics = json.load(f)

    tau = float(metrics["tau"])

    # label inference (consistent with your colab)
    scores["label"] = scores["file"].astype(str).str.contains("abnormal").map({True: "abnormal", False: "normal"})
    normal_scores = scores.loc[scores["label"] == "normal", "score_mean"].astype(float).to_numpy()
    abnormal_scores = scores.loc[scores["label"] == "abnormal", "score_mean"].astype(float).to_numpy()

    # Tail enrichment
    tail_norm = float(np.mean(normal_scores > tau)) if len(normal_scores) else 0.0
    tail_abn = float(np.mean(abnormal_scores > tau)) if len(abnormal_scores) else 0.0
    enrichment = tail_abn / (tail_norm + 1e-12)

    print("tau =", tau)
    print(f"N normal = {len(normal_scores)}, N abnormal = {len(abnormal_scores)}")
    print(f"Tail normal  > tau: {tail_norm}")
    print(f"Tail abnormal> tau: {tail_abn}")
    print(f"Enrichment factor: {enrichment}")

    # log bins (avoid <=0)
    all_scores = np.concatenate([normal_scores, abnormal_scores]) if len(normal_scores) and len(abnormal_scores) else (normal_scores if len(normal_scores) else abnormal_scores)
    pos = all_scores[all_scores > 0]
    if len(pos) == 0:
        raise SystemExit("All scores are non-positive; cannot use log scale.")
    min_pos = float(np.min(pos))
    max_pos = float(np.max(pos))
    bins = np.logspace(np.log10(min_pos), np.log10(max_pos), 60)

    fig = plt.figure(figsize=(6.2, 4.0))
    ax = plt.gca()

    # Histograms
    ax.hist(normal_scores[normal_scores > 0], bins=bins, density=True, histtype="step",
            linewidth=2, label="Normal", color="gray")
    ax.hist(abnormal_scores[abnormal_scores > 0], bins=bins, density=True, histtype="step",
            linewidth=2, label="Abnormal", color="black")

    # Threshold line in the plot (keep dashed)
    ax.axvline(
        tau,
        color="red",
        linewidth=2,
        linestyle=(0, (6, 4)),
        dash_capstyle="butt",
        solid_capstyle="butt",
        zorder=10,
    )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Anomaly score")
    ax.set_ylabel("Probability density")
    ax.set_title("Tail enrichment of morphological anomaly scores")

    # Legend: use proxy handle for tau line (prevents random dash artefacts in some PDF renderers)
    proxy_tau = Line2D(
        [0], [0],
        color="red",
        linewidth=2,
        linestyle=(0, (6, 4)),
        dash_capstyle="butt",
        solid_capstyle="butt",
    )
    handles, labels = ax.get_legend_handles_labels()
    handles.append(proxy_tau)
    labels.append(rf"$\tau$ ({args.quantile_label})")

    ax.legend(handles=handles, labels=labels, frameon=False, loc="upper right",
              handlelength=3.0, handletextpad=0.8)

    fig.tight_layout()

    out_pdf = Path(args.out_pdf)
    out_png = Path(args.out_png)
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    out_png.parent.mkdir(parents=True, exist_ok=True)

    fig.savefig(out_pdf, bbox_inches="tight", pad_inches=0.02)
    fig.savefig(out_png, dpi=args.dpi, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)

    print("Saved:", out_pdf)
    print("Saved:", out_png)


if __name__ == "__main__":
    main()
