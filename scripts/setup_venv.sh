#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install numpy scipy pandas matplotlib scikit-learn pyarrow pyyaml tqdm rich

python -c "import sklearn, pyarrow, pandas; print('OK', sklearn.__version__)"
echo "Done. Activate with: source .venv/bin/activate"
