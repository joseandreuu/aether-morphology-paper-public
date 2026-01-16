#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="data/processed/fig2_ims"
mkdir -p "$OUT_DIR"

# Cambia esta fecha si subes otra versión
DATE_TAG="2026-01-13"

BASE="gs://aether-dataset-v2/runs/ims_nasa"

fetch_one () {
  local RUN="$1"   # IMS_1st_test / IMS_2nd_test / IMS_3rd_test
  local slug="$2"  # ims_1st_test / ims_2nd_test / ims_3rd_test

  echo "==> Fetching $RUN"
  gsutil cp "${BASE}/${RUN}__HEALTH_INDEX_NORM__${DATE_TAG}/${slug}_health_index_norm_tau.csv" "${OUT_DIR}/"
  gsutil cp "${BASE}/${RUN}__HEALTH_INDEX_NORM__${DATE_TAG}/${slug}_health_index_norm_tau_summary.json" "${OUT_DIR}/" 2>/dev/null || true

  # Drift/TTD summary (opcional, si existe)
  gsutil cp "${BASE}/${RUN}__DRIFT_TTD__${DATE_TAG}/${slug}_drift_ttd_summary.json" "${OUT_DIR}/" 2>/dev/null || true
}

fetch_one "IMS_1st_test" "ims_1st_test"
fetch_one "IMS_2nd_test" "ims_2nd_test"
fetch_one "IMS_3rd_test" "ims_3rd_test"

echo
echo "Done. Files in: ${OUT_DIR}"
ls -lh "${OUT_DIR}"
