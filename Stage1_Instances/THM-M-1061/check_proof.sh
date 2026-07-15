#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
lean_root="$repo_root/Formalizations/Lean"
combined="$(mktemp /tmp/THM-M-1061-Proof.XXXXXX.lean)"
trap 'rm -f "$combined"' EXIT

sed -n '1,$p' "$repo_root/Stage1_Instances/THM-M-1061/Statement.lean" > "$combined"
sed -n '1,$p' "$repo_root/Stage1_Instances/THM-M-1061/Proof.lean" >> "$combined"

cd "$lean_root"
lake env lean --trust=0 "$combined"
