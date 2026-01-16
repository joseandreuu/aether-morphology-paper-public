#!/usr/bin/env bash
set -euo pipefail

OUT="data/processed/fig6"
mkdir -p "$OUT"

BASE="gs://aether-dataset-v2/experiments/cwru/paper_tables"

SCORES_CSV="$BASE/reverb_L1_scores_by_file.csv"
METRICS_JSON="$BASE/cwru_auc_metrics.json"

echo "Downloading Fig6 inputs..."
echo " - $SCORES_CSV"
gsutil -q cp "$SCORES_CSV" "$OUT/reverb_L1_scores_by_file.csv"

echo " - $METRICS_JSON"
gsutil -q cp "$METRICS_JSON" "$OUT/cwru_auc_metrics.json"

echo "Done. Files in $OUT:"
ls -lh "$OUT"
