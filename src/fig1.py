import argparse
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


def _ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def draw_fig1(out_pdf: str, out_png: str) -> None:
    # APS-like typography (portable)
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["DejaVu Serif"],
        "mathtext.fontset": "cm",
        "font.size": 10,
        "axes.linewidth": 0.9,
        "text.usetex": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })

    # APS double-column width ~ 6.75 in
    # Make height compact so diagram fills the page, not drowned in whitespace
    fig = plt.figure(figsize=(6.75, 2.15))
    ax = fig.add_subplot(111)
    ax.axis("off")

    # Layout coordinate system (trimmed by bbox_inches="tight")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 32)

    ec = "#111111"
    fc_left = "#F2F2F2"
    fc_mid = "#FFFFFF"
    arrow_c = "#111111"
    lw = 1.1

    # --- Geometry (fills width) ---
    # Left boxes
    gw_x, gw_y, wL, hL = 3, 19, 34, 11
    me_x, me_y = 3, 2

    # Operator + latent
    op_x, op_y, wO, hO = 42, 9.5, 23, 14
    z_x, z_y, wZ, hZ = 72, 9.5, 25, 14

    # --- Boxes ---
    box_gw = FancyBboxPatch(
        (gw_x, gw_y), wL, hL,
        boxstyle="round,pad=0.25,rounding_size=0.9",
        ec=ec, fc=fc_left, lw=lw
    )
    ax.add_patch(box_gw)
    ax.text(
        gw_x + wL / 2, gw_y + 7.2,
        "Gravitational-Wave\nInstrumentation",
        ha="center", va="center", weight="bold", fontsize=12
    )
    ax.text(
        gw_x + wL / 2, gw_y + 3.0,
        "Interferometric strain",
        ha="center", va="center", style="italic", fontsize=10
    )

    box_me = FancyBboxPatch(
        (me_x, me_y), wL, hL,
        boxstyle="round,pad=0.25,rounding_size=0.9",
        ec=ec, fc=fc_left, lw=lw
    )
    ax.add_patch(box_me)
    ax.text(
        me_x + wL / 2, me_y + 7.2,
        "Rotating machinery",
        ha="center", va="center", weight="bold", fontsize=12
    )
    ax.text(
        me_x + wL / 2, me_y + 3.0,
        "Mechanical vibration",
        ha="center", va="center", style="italic", fontsize=10
    )

    box_op = FancyBboxPatch(
        (op_x, op_y), wO, hO,
        boxstyle="round,pad=0.25,rounding_size=0.9",
        ec=ec, fc=fc_mid, lw=lw
    )
    ax.add_patch(box_op)
    ax.text(
        op_x + wO / 2, op_y + 9.2,
        r"$\mathcal{F}$",
        ha="center", va="center", fontsize=30
    )
    ax.text(
        op_x + wO / 2, op_y + 4.2,
        "Frozen latent\noperator",
        ha="center", va="center", fontsize=10
    )

    box_z = FancyBboxPatch(
        (z_x, z_y), wZ, hZ,
        boxstyle="round,pad=0.25,rounding_size=0.9",
        ec=ec, fc=fc_mid, lw=lw
    )
    ax.add_patch(box_z)
    ax.text(
        z_x + wZ / 2, z_y + 9.2,
        r"$\mathcal{Z}$",
        ha="center", va="center", fontsize=30
    )
    ax.text(
        z_x + wZ / 2, z_y + 4.2,
        "Shared latent\nspace",
        ha="center", va="center", fontsize=10
    )

    # --- Arrows ---
    kw = dict(arrowstyle="-|>", mutation_scale=14, lw=1.15, color=arrow_c)

    # Small offsets so arrows don't visually "stick" to rounded corners
    gw_start = (gw_x + wL + 0.3, gw_y + 6.2)
    me_start = (me_x + wL + 0.3, me_y + 4.8)
    f_top = (op_x - 0.2, op_y + 11.0)
    f_bot = (op_x - 0.2, op_y + 3.0)

    # GW -> F
    ax.add_patch(FancyArrowPatch(
        gw_start, f_top,
        connectionstyle="arc3,rad=-0.12", **kw
    ))
    # Mech -> F
    ax.add_patch(FancyArrowPatch(
        me_start, f_bot,
        connectionstyle="arc3,rad=0.12", **kw
    ))
    # F -> Z
    ax.add_patch(FancyArrowPatch(
        (op_x + wO, op_y + hO / 2), (z_x, z_y + hZ / 2),
        connectionstyle="arc3,rad=0.0", **kw
    ))

    _ensure_parent_dir(out_pdf)
    _ensure_parent_dir(out_png)

    fig.savefig(out_pdf, format="pdf", bbox_inches="tight", pad_inches=0.03)
    fig.savefig(out_png, format="png", dpi=600, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-pdf", default="paper/figures/Fig1.pdf")
    parser.add_argument("--out-png", default="outputs/figures/Fig1.png")
    args = parser.parse_args()

    draw_fig1(args.out_pdf, args.out_png)
    print(f"Saved: {args.out_pdf} and {args.out_png}")


if __name__ == "__main__":
    main()
