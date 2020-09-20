#!/usr/bin/env bash

CONTAINER_NAME=yahoo-proxy-server
IMAGE_NAME="local-${CONTAINER_NAME}"

PROXY_PORT="${1}"
INTERNAL_PORT="${PROXY_PORT}"
EXTERNAL_PORT="${PROXY_PORT}"

build() {
  docker build . \
    -t ${IMAGE_NAME} \
    -f Dockerfile \
    --build-arg PROXY_PORT="${INTERNAL_PORT}"
}

run_detached() {
  docker rm -f ${CONTAINER_NAME}
  docker run -d -p "${EXTERNAL_PORT}:${INTERNAL_PORT}" --name ${CONTAINER_NAME} ${IMAGE_NAME}
}

wait_until_api_is_running_before_exiting() {
  is_not_ready() {
    OUTPUT=$(docker exec ${CONTAINER_NAME} curl --silent localhost:${INTERNAL_PORT})
    if [[ "${OUTPUT}" != "hello world" ]]; then
        echo "Container is not ready. Waiting..."
        sleep 2s
        return 0
    fi
    echo "API is running on port ${EXTERNAL_PORT}!"
    return 1
  }

  MAX_ATTEMPTS=5
  iteration=0
  while is_not_ready
  do
    iteration=$((iteration+1))
    if [[ iteration -ge ${MAX_ATTEMPTS} ]]; then
      echo "Operation ran for more than: ${MAX_ATTEMPTS} attempts. Exiting..."
      exit 1
    fi
  done
}

build
run_detached
wait_until_api_is_running_before_exiting