#!/usr/bin/env bash
set -euo pipefail

OUT="data/processed/fig4"
mkdir -p "$OUT"

CSV_PATH="gs://aether-dataset-v2/experiments/cwru/morphology_destruction/tables/morphology_destruction.csv"

echo "Downloading Fig3 CSV: $CSV_PATH"
gsutil -q cp "$CSV_PATH" "$OUT/morphology_destruction.csv"

echo "Done. Files in $OUT:"
ls -lh "$OUT"
