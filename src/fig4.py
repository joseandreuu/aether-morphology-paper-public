import argparse
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def main():
    ap = argparse.ArgumentParser(description="Generate Fig3 (morphology destruction sensitivity).")
    ap.add_argument("--csv", required=True, help="Path to morphology_destruction.csv")
    ap.add_argument("--out-pdf", required=True, help="Output PDF path")
    ap.add_argument("--out-png", required=True, help="Output PNG path")
    ap.add_argument("--raw-baseline", type=float, default=None,
                    help="Optional horizontal raw baseline AUC (e.g., 0.90)")
    ap.add_argument("--dpi", type=int, default=600, help="PNG DPI (default: 600)")
    args = ap.parse_args()

    # APS-ish typography + editable PDF text (no Type3)
    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm",
        "font.size": 9,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.linewidth": 1.0,
    })

    df = pd.read_csv(args.csv)

    required = {"kind", "level", "auc_window"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing columns: {sorted(missing)}. Have: {list(df.columns)}")

    # Style map (keeps your intended palette)
    colors = {
        "lowpass": "#1f77b4",
        "reverb":  "#d62728",
        "smear":   "#9467bd",
    }
    labels = {
        "lowpass": "Low-pass",
        "reverb":  "Reverb",
        "smear":   "Smear",
    }

    fig = plt.figure(figsize=(6.75, 2.6))
    ax = plt.gca()

    # Optional raw baseline line (recommended if you want Option A visible)
    if args.raw_baseline is not None:
        ax.axhline(args.raw_baseline, linestyle=":", linewidth=1.0)
        ax.text(
            0.02, args.raw_baseline + 0.01,
            "Raw baseline (Sec. III.A)",
            transform=ax.get_yaxis_transform(),
            fontsize=8,
            va="bottom"
        )

    for kind, color in colors.items():
        d = df[df["kind"].astype(str).str.lower() == kind].copy()
        if d.empty:
            continue
        d = d.sort_values("level")

        # L0: control point only
        d0 = d[d["level"] == 0]
        ax.plot(
            d0["level"], d0["auc_window"],
            marker="D", linestyle="None",
            color=color
        )

        # L1-L2: degradation curve
        d12 = d[d["level"].isin([1, 2])]
        ax.plot(
            d12["level"], d12["auc_window"],
            marker="o", linestyle="-",
            color=color,
            label=labels.get(kind, kind)
        )

    ax.set_title("Sensitivity under controlled destruction of signal morphology")
    ax.set_xlabel("Morphological degradation level")
    ax.set_ylabel(r"$\mathrm{AUC}_{\mathrm{win}}$")

    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels([r"$L_0$", r"$L_1$", r"$L_2$"])

    ax.set_ylim(0.45, 1.02)
    ax.grid(True, alpha=0.25)

    # Legend below (so it never overlaps theه similar to your Fig2 fix)
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=3)

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
