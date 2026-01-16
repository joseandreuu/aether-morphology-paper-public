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

Only **derived, publication-safe, non-invertible artifacts** are provided.

---

## Repository layout

- `src/` — figure generation scripts (Fig1–Fig6)
- `scripts/` — data-fetch and environment setup utilities
- `paper/figures/` — final PDF figures used in the manuscript (committed)
- `paper/tables/` — derived tabular artifacts used to generate figures (committed)
- `outputs/figures/` — generated PNGs (git-ignored)
- `data/processed/` — intermediate artifacts downloaded by fetch scripts (git-ignored)
- `configs/` — experiment configuration (paths, constants)
- `environment.yml` — conda environment specification
- `Makefile` — reproducible build entrypoints

---

## What is reproducible

- Figures **Fig. 1–Fig. 6**
- Exact numerical results used in the manuscript figures
- Plot styles, thresholds, annotations, and metrics

Not included:

- Latent operator / model weights
- Training code
- Raw sensor data

All released artifacts are **post-hoc, non-invertible**, and sufficient to reproduce the published results exactly.

---

## Figure-to-data mapping

Each figure is generated from a fixed and minimal set of derived artifacts:

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

Figures **Fig. 2–Fig. 6** are **fully reproducible at the figure level** using the
derived numerical artifacts committed in this repository (`paper/tables/`).

The original raw sensor streams and intermediate execution artifacts used to
produce those tables are hosted in a **restricted Google Cloud Storage (GCS) bucket**
and are **not publicly accessible**.

- The bucket is **not public**
- No anonymous or public access is enabled
- Access is controlled via Google Cloud IAM

Users without access permissions can still:

- Reproduce **all manuscript figures (Fig. 1–Fig. 6)** from the committed tables
- Verify **all numerical values reported in the paper**
- Inspect the final manuscript figures under `paper/figures/`

What is not reproducible without private access:

- Re-execution from raw sensor streams
- Regeneration of intermediate scoring artifacts

This design ensures both:
- **Scientific reproducibility of published results**
- **Protection of proprietary representations and operators**

## Prerequisites

- Python **3.9+**
- `git`
- `gsutil` authenticated (only required for fetching intermediate artifacts)
- macOS / Linux recommended

---

## Quickstart (recommended: virtual environment)

```bash
git clone https://github.com/joseandreuu/aether-morphology-paper-public.git
cd aether-morphology-paper-public

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

The core method described in the associated manuscript is protected by a filed patent application:

Spanish Patent Application No. P202630043 (filed 2026).

This repository is intentionally limited to figure-level reproducibility and post-hoc numerical artifacts in order to support scientific validation and peer review, while preventing disclosure of proprietary implementations covered by the above patent application.

No model weights, trainable representations, or implementation details enabling reconstruction of the protected method are included.
All shared artifacts are non-invertible and publication-safe.

## Licensing

This repository is multi-licensed by component:
	•	Code: MIT License (LICENSE)
	•	Manuscript text and figures: CC BY 4.0 (LICENSE-PAPER)
	•	Derived numerical artifacts: CC BY 4.0 (LICENSE-DATA)

Proprietary components are intentionally excluded.

Citation
```bibtex
@article{aether_morphology_2026,
  title  = {Morphological Invariance and Selective Zero-Shot Transfer from Interferometric Instrumentation to Rotating Mechanical Systems},
  author = {Sanchez Andreu, Jose},
  year   = {2026}
}
```
## Contact

Jose Antonio Sanchez Andreu
GitHub: https://github.com/joseandreuu
