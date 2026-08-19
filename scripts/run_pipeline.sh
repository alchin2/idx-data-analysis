# Usage:
#   scripts/run_pipeline.sh                # fetch + all stages
#   scripts/run_pipeline.sh --skip-fetch   # start from stage 0 (use existing data/raw/)

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

SKIP_FETCH=0
if [[ "${1:-}" == "--skip-fetch" ]]; then
    SKIP_FETCH=1
fi

run_notebook() {
    echo "Running $1"
    jupyter nbconvert --to notebook --execute --inplace "$1"
}

if [[ "$SKIP_FETCH" -eq 0 ]]; then
    echo "Fetching raw data"
    python preprocessing/fetch_data.py
    python preprocessing/mortgage/fred.py
fi

echo "Stage 0: combine + residential filter"
python preprocessing/preprocess.py

#stage 1-4
jupyter nbconvert --execute --to notebook --log-level="ERROR" null_analysis.ipynb > /dev/null 2>&1
jupyter nbconvert --execute --to notebook --log-level="ERROR" preprocessing/mortgage/merge.ipynb > /dev/null 2>&1
jupyter nbconvert --execute --to notebook --log-level="ERROR" validation.ipynb > /dev/null 2>&1
jupyter nbconvert --execute --to notebook --log-level="ERROR" school_districting.ipynb > /dev/null 2>&1


echo "Stage 5: feature engineering"
python features.py

echo "Stage 6: IQR outlier filter"
python iqr_filter.py

echo "Pipeline complete"
