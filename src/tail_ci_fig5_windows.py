import json
import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IN_PARQUET = ROOT / "data" / "processed" / "fig2" / "cwru_scored_windows.parquet"
OUT_JSON = ROOT / "paper" / "tables" / "fig5_tail_ci_windows.json"

Q = 0.999
B = 20000
SEED = 123

def bootstrap_ci_p_abn(s_abn, tau, B, seed):
    rng = np.random.default_rng(seed)
    n = len(s_abn)
    p = np.empty(B, dtype=float)
    for b in range(B):
        samp = rng.choice(s_abn, size=n, replace=True)
        p[b] = float(np.mean(samp > tau))
    lo, hi = np.quantile(p, [0.025, 0.975])
    return float(lo), float(hi)

def main():
    df = pd.read_parquet(IN_PARQUET)

    # 1) Filtrar SOLO condición reverb_L1 (por el path)
    m = df["path"].astype(str).str.contains("reverb_L1", case=False, na=False)
    df = df.loc[m].copy()

    # 2) Label binario desde split
    s = df["split"].astype(str).str.lower().str.strip()
    df["_y"] = (s == "abnormal").astype(int)

    # 3) Score column (usamos S_z)
    score_col = "S_z"
    if score_col not in df.columns:
        raise SystemExit(f"ERROR: no existe {score_col} en el parquet. Columns={list(df.columns)}")

    s_nom = df.loc[df["_y"] == 0, score_col].to_numpy()
    s_abn = df.loc[df["_y"] == 1, score_col].to_numpy()

    if len(s_nom) < 2000:
        print(f"WARN: nominal windows={len(s_nom)} parece bajo para q=0.999 (ideal >> 1000).")

    # 4) Tau en nominal (cuantil)
    tau = float(np.quantile(s_nom, Q))

    # 5) Probabilidades de excedencia
    p_nom_obs = float(np.mean(s_nom > tau))
    p_abn = float(np.mean(s_abn > tau))

    far = float(1.0 - Q)
    lam = float(p_abn / far)

    # 6) CI bootstrap SOLO abnormal (denominador fijo)
    ci_pabn = bootstrap_ci_p_abn(s_abn, tau, B, SEED)
    ci_lam = (ci_pabn[0] / far, ci_pabn[1] / far)

    out = {
        "input": str(IN_PARQUET.relative_to(ROOT)),
        "filter": "path contains reverb_L1",
        "columns": {"score": score_col, "label": "_y", "split": "split"},
        "n_windows_total": int(len(df)),
        "n_windows_nominal": int(len(s_nom)),
        "n_windows_abnormal": int(len(s_abn)),
        "q": float(Q),
        "far_theoretical": far,
        "tau": tau,
        "p_nominal_observed": p_nom_obs,
        "p_abnormal": p_abn,
        "lambda_tail": lam,
        "bootstrap": {
            "B": int(B),
            "seed": int(SEED),
            "ci95_p_abnormal": [float(ci_pabn[0]), float(ci_pabn[1])],
            "ci95_lambda_tail": [float(ci_lam[0]), float(ci_lam[1])],
        },
    }

    OUT_JSON.write_text(json.dumps(out, indent=2))
    print(f"Wrote: {OUT_JSON}")
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
