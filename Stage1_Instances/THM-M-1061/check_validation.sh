#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
lean_root="$repo_root/Formalizations/Lean"
owned="$repo_root/Stage1_Instances/THM-M-1061"
tmp="$(mktemp -d /tmp/stage1-m1061-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

for name in Statement.lean ObligationTree.lean Proof.lean AnchorAudit.lean Validation.lean; do
  cp "$owned/$name" "$tmp/$name"
done

cd "$lean_root"
toolchain_bin="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin"
lean_bin="$toolchain_bin/lean"
lean_path="$lean_root/.lake/packages/Cli/.lake/build/lib/lean"
for package in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible checkdecls mathlib; do
  lean_path="$lean_path:$lean_root/.lake/packages/$package/.lake/build/lib/lean"
done
lean_path="$lean_path:$lean_root/.lake/build/lib/lean:$toolchain_bin/../lib/lean"
bwrap_bin="$(command -v bwrap)"

run_lean() {
  local source="$1"
  local module_path="${2:-false}"
  local output="${3:-}"
  local active_path="$lean_path"
  local -a output_args=()

  if [[ "$module_path" == true ]]; then
    active_path="$tmp:$lean_path"
  fi
  if [[ -n "$output" ]]; then
    output_args=(-o "$output")
  fi

  "$bwrap_bin" \
    --ro-bind / / \
    --bind "$tmp" "$tmp" \
    --dev /dev \
    --proc /proc \
    --unshare-net \
    --die-with-parent \
    --setenv HOME "$tmp/home" \
    --setenv LANG C.UTF-8 \
    --setenv LC_ALL C.UTF-8 \
    --setenv TZ UTC \
    --setenv LEAN_NUM_THREADS 1 \
    --setenv LEAN_PATH "$active_path" \
    --chdir "$tmp" \
    "$lean_bin" --trust=0 -t0 "${output_args[@]}" "$source"
}

run_lean Statement.lean false "$tmp/Statement.olean"

for module in ObligationTree Proof; do
  combined="$tmp/${module}Combined.lean"
  cp "$tmp/Statement.lean" "$combined"
  printf '\n' >> "$combined"
  cat "$tmp/$module.lean" >> "$combined"
  run_lean "${module}Combined.lean" false
done

run_lean AnchorAudit.lean false

combined="$tmp/ValidationCombined.lean"
cp "$tmp/Statement.lean" "$combined"
printf '\n' >> "$combined"
cat "$tmp/Validation.lean" >> "$combined"
run_lean ValidationCombined.lean false
