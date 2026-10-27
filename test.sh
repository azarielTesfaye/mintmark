#!/usr/bin/env bash
set -uo pipefail

output_path=""
mode=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output_path)
      output_path="${2:-}"
      shift 2
      ;;
    base|new)
      mode="$1"
      shift
      ;;
    *)
      echo "unexpected argument: $1" >&2
      exit 2
      ;;
  esac
done

if [[ -z "$mode" || -z "$output_path" ]]; then
  echo "usage: ./test.sh --output_path PATH {base|new}" >&2
  exit 2
fi

cd "$(dirname "$0")"

ignore_args=()
target="tests"
if [[ "$mode" == "base" ]]; then
  if [[ -d tests/ext ]]; then
    ignore_args+=(--ignore=tests/ext)
  fi
  ignore_args+=(--ignore-glob='*_[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f].py')
elif [[ "$mode" == "new" ]]; then
  target="tests/ext"
else
  echo "unknown mode: $mode" >&2
  exit 2
fi

python -m pytest -p no:cacheprovider --junitxml="$output_path" "${ignore_args[@]}" "$target"
exit $?
