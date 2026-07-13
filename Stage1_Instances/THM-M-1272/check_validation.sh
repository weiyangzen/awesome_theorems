#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "$0")/../.." && pwd)
toolchain_root=${ELAN_HOME:-"$HOME/.elan"}/toolchains/leanprover--lean4---v4.29.0
lean_bin="$toolchain_root/bin/lean"
lean_paths=()
for package in Cli batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible checkdecls mathlib flt-regular; do
  path="$repo_root/Formalizations/Lean/.lake/packages/$package/.lake/build/lib/lean"
  if [[ -d "$path" ]]; then
    lean_paths+=("$path")
  fi
done
lean_paths+=("$repo_root/Formalizations/Lean/.lake/build/lib/lean" "$toolchain_root/lib/lean")
lean_path=$(IFS=:; printf '%s' "${lean_paths[*]}")
tmp_root=$(mktemp -d /tmp/thm-m-1272-validation-wrapper.XXXXXX)
trap 'rm -rf "$tmp_root"' EXIT
mkdir -p "$tmp_root/home" "$tmp_root/tmp"

exec /usr/bin/bwrap \
  --clearenv \
  --unshare-net \
  --die-with-parent \
  --ro-bind / / \
  --bind "$tmp_root/tmp" /tmp \
  --dev /dev \
  --proc /proc \
  --dir /run \
  --setenv HOME /tmp/home \
  --setenv TMPDIR /tmp \
  --setenv LANG C.UTF-8 \
  --setenv LC_ALL C.UTF-8 \
  --setenv TZ UTC \
  --setenv LEAN_NUM_THREADS 1 \
  --setenv PATH "$PATH" \
  --setenv STAGE1_NETWORK_DENIED 1 \
  --setenv STAGE1_LEAN_BIN "$lean_bin" \
  --setenv STAGE1_LEAN_PATH "$lean_path" \
  --chdir "$repo_root" \
  -- /usr/bin/python3 -I -B Stage1_Instances/THM-M-1272/check_validation.py
