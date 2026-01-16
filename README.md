# Aether Morphology Paper — Reproducibility Repository

This repository provides a **figure-level reproducibility package** for the manuscript:

**“Morphological Invariance and Selective Zero-Shot Transfer from Interferometric Instrumentation to Rotating Mechanical Systems”**

The goal of this repository is to enable **independent regeneration of all manuscript figures** while **explicitly protecting proprietary models, latent operators, and raw sensor data**.

---
## Scope of reproducibility

This repository allows reproduction of:

- All manuscript figures (**Fig. 1–Fig. 6**)
- Exact numerical values used in the plots
- Plot styling, thresholds, annotations, and metrics reported in the paper

This repository does **not** include:

- The latent operator or its weights
- Training code
- Raw gravitational-wave or mechanical sensor streams

Only **derived, publication-safe, non-invertible artifacts** are used.


## Repository layout

- `src/` — figure generators (Fig1–Fig6)
- `scripts/` — data fetch + environment setup
- `paper/figures/` — final PDFs included in the manuscript (committed)
- `paper/tables/` — derived tabular artifacts used to generate figures (committed)
- `outputs/figures/` — generated PNGs (git-ignored)
- `data/processed/` — downloaded intermediate artifacts (git-ignored)
- `configs/` — experiment configuration (paths, constants)
- `environment.yml` — conda environment specification
- `Makefile` — reproducible build entrypoints

---

## What is reproducible

- Figures **Fig1–Fig6**
- Exact numerical results used in the paper figures
- Plot styles, thresholds, annotations, and metrics

Not included:

- Latent operator / model weights
- Training code or raw sensor streams

Only **derived, non-invertible artifacts** (scores, tables, metrics) are used.

---
## Figure-to-data mapping

Each figure is generated from a fixed, minimal set of derived artifacts:

- **Fig. 1** — Analytical / schematic construction (no external data)
- **Fig. 2** — IMS-NASA bearing degradation experiments  
  - Health Index time series and summaries (`ims_*_health_index_norm_tau.csv`)
- **Fig. 3** — Cross-domain transferability and physical boundary validation
- **Fig. 4** — Controlled morphological degradation experiments
- **Fig. 5** — Correlation between latent scores and physical descriptors
- **Fig. 6** — Tail enrichment analysis of anomaly scores

All tabular artifacts are included under `paper/tables/` and are sufficient to regenerate the figures exactly.

---

## Data access and policy

Figures **Fig. 2–Fig. 6** rely on intermediate artifacts stored in a **private Google Cloud Storage (GCS) bucket**.

- The bucket is **not public**
- No anonymous or authenticated public access is enabled
- Access is controlled via Google Cloud IAM

Users without access permissions can still:

- Reproduce **Fig. 1**
- Inspect the final manuscript figures under `paper/figures/`

This design ensures:
- Scientific reproducibility
- Protection of proprietary representations and operators

---

## Prerequisites

- Python **3.11+**
- `git`
- `gsutil` authenticated (only required for Fig2–Fig5 data fetch)
- macOS / Linux recommended

---

## Quickstart (recommended: venv)

```bash
git clone git@github.com:joseandreuu/aether-morphology-paper.git
cd aether-morphology-paper

bash scripts/setup_venv.sh
source .venv/bin/activate

make figures
```
This will:
	1.	Create a local Python environment
	2.	Download the required intermediate artifacts (if you have access)
	3.	Regenerate Fig1–Fig6 from scratch

⸻

## Build figures individually
```bash
source .venv/bin/activate

make fig1
make fig2
make fig3
make fig4
make fig5
make fig6
```
Generated outputs:
	•	PDFs → paper/figures/Fig*.pdf
	•	PNGs → outputs/figures/Fig*.png

⸻
## Intellectual property notice

This repository does not expose:
	•	The latent operator
	•	Model weights
	•	Trainable representations
	•	Any component enabling reconstruction of the core method

All shared numerical artifacts are post-hoc, non-invertible, and publication-safe.
All figures are generated from a frozen snapshot of latent operator outputs (January 2026).

## Licensing

This repository is multi-licensed by component:
	•	Code: MIT License (LICENSE)
	•	Manuscript text and figures: CC BY 4.0 (LICENSE-PAPER)
	•	Derived numerical artifacts: CC BY 4.0 (LICENSE-DATA)

Proprietary components are intentionally excluded.

Citation
```bibtex
@article{aether_morphology_2026,
  title   = {Morphological Invariance and Selective Zero-Shot Transfer from Interferometric Instrumentation to Rotating Mechanical Systems},
  author  = {Jose Antonio Sanchez Andreu},
  year    = {2026}
}
```
## Contact

Jose Antonio Sanchez Andreu
GitHub: https://github.com/joseandreuu
