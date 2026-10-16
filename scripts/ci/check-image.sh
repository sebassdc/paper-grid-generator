#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
image="paper-grid-ci:${GITHUB_RUN_ID:-local}-$$"
container=""
trap 'if [ -n "$container" ]; then docker rm -f "$container" >/dev/null; fi; docker image rm "$image" >/dev/null 2>&1 || true' EXIT
flock /tmp/coolify-rollout-ci-build.lock docker build -f deploy/coolify-pilot/Dockerfile -t "$image" .
container=$(docker run -d -p 127.0.0.1::80 "$image")
port=$(docker port "$container" 80/tcp | sed 's/127.0.0.1://')
export CI_BASE_URL="http://127.0.0.1:$port"
for attempt in {1..30}; do curl -fsS "$CI_BASE_URL/up" >/dev/null && break; sleep 1; done
node scripts/ci/browser.mjs
