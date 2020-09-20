PROXY_PORT=5000
DIRECTORY_OF_THIS_FILE="$(dirname "${BASH_SOURCE[0]}")"
./"${DIRECTORY_OF_THIS_FILE}"/run_yahoo_proxy_server_locally.sh "${PROXY_PORT}"
PROXY_BASE_URL="http://localhost:${PROXY_PORT}" pipenv run python -m src.jobs.local_pipeline
