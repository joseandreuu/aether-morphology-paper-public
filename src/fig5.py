import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


FEATURE_ORDER = ["rms", "peak", "crest", "spec_entropy", "bandwidth", "kurtosis", "skewness"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aether", required=True, help="CSV aether_physical_correlation.csv")
    ap.add_argument("--convae", required=True, help="CSV convae_physical_correlation.csv")
    ap.add_argument("--out-pdf", required=True)
    ap.add_argument("--out-png", required=True)
    ap.add_argument("--dpi", type=int, default=600)
    ap.add_argument("--vmin", type=float, default=-0.7)
    ap.add_argument("--vmax", type=float, default=0.7)
    ap.add_argument("--no-title", action="store_true", help="Remove title (recommended if title goes in caption)")
    args = ap.parse_args()

    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif"],
            "mathtext.fontset": "cm",
            "font.size": 9,
            "axes.linewidth": 0.8,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )

    aether = pd.read_csv(args.aether, index_col=0)
    convae = pd.read_csv(args.convae, index_col=0)

    aether = aether.loc[FEATURE_ORDER]
    convae = convae.loc[FEATURE_ORDER]

    corr = pd.DataFrame(
        {
            "Aether": aether.iloc[:, 0].astype(float).to_numpy(),
            "ConvAE": convae.iloc[:, 0].astype(float).to_numpy(),
        },
        index=FEATURE_ORDER,
    )

    fig, ax = plt.subplots(figsize=(3.4, 4.6))  # APS single-column-ish

    im = ax.imshow(
        corr.values,
        cmap="coolwarm",
        vmin=args.vmin,
        vmax=args.vmax,
        aspect="auto",
    )

    ax.set_xticks(np.arange(corr.shape[1]))
    ax.set_xticklabels(corr.columns)
    ax.set_yticks(np.arange(corr.shape[0]))
    ax.set_yticklabels(corr.index)

    for i in range(corr.shape[0]):
        for j in range(corr.shape[1]):
            ax.text(
                j,
                i,
                f"{corr.values[i, j]:.2f}",
                ha="center",
                va="center",
                fontsize=8,
                color="black",
            )

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Pearson correlation", fontsize=9)

    if not args.no_title:
        ax.set_title("Physical feature correlation:\nAether vs ConvAE", fontsize=10)

    ax.set_ylabel("Physical features")

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
