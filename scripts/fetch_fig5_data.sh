#!/usr/bin/env bash
set -euo pipefail

OUT="data/processed/fig5"
mkdir -p "$OUT"

AETHER_CSV="gs://aether-dataset-v2/experiments/cwru/paper_tables/aether_physical_correlation.csv"
CONVAE_CSV="gs://aether-dataset-v2/experiments/cwru/paper_tables/convae_physical_correlation.csv"

echo "Downloading: $AETHER_CSV"
gsutil -q cp "$AETHER_CSV" "$OUT/aether_physical_correlation.csv"

echo "Downloading: $CONVAE_CSV"
gsutil -q cp "$CONVAE_CSV" "$OUT/convae_physical_correlation.csv"

echo "Done. Files in $OUT:"
ls -lh "$OUT"
