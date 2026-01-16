#!/usr/bin/env bash
set -euo pipefail

BUCKET="gs://aether-dataset-v2"
OUT="data/processed/fig3"
mkdir -p "$OUT"

# Panel (a): rotating mechanical systems (representative condition)
CWRU_PARQ="$BUCKET/experiments/cwru/morphology_destruction/runs/destroy_runs/reverb_L1/cwru_destroy_id_00_scored_windows.parquet"

# Panel (b): VSB scored parquet with labels
VSB_PARQ="$BUCKET/paper_snapshot/20260108_133742/aether_vsb_run/vsb_id_00_scored_windows.parquet"

echo "Downloading CWRU: $CWRU_PARQ"
gsutil -q cp "$CWRU_PARQ" "$OUT/cwru_scored_windows.parquet"

echo "Downloading VSB:  $VSB_PARQ"
gsutil -q cp "$VSB_PARQ" "$OUT/vsb_scored_windows.parquet"

echo "Done. Files in $OUT:"
ls -lh "$OUT"
