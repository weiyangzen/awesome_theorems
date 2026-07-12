#!/usr/bin/env bash
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
repo=$(cd "$here/../.." && pwd)
tmp=$(mktemp --suffix=.lean)
trap 'rm -f "$tmp"' EXIT

sed '/^set_option pp.explicit true in$/,$d' "$here/Statement.lean" > "$tmp"
sed '1,2d' "$here/ObligationTree.lean" >> "$tmp"
cat >> "$tmp" <<'LEAN'

namespace Stage1Instances.THM_M_1078.ObligationTree

theorem local_target_iff_frozen_target :
    MartingaleTransformTarget.{u} <-> Stage1Instances.THM_M_1078.MartingaleTransformTarget.{u} := by
  change Stage1Instances.THM_M_1078.ExpandedSourceShape.{u} <->
    Stage1Instances.THM_M_1078.ExpandedSourceShape.{u}
  rfl

#check local_target_iff_frozen_target
#print axioms local_target_iff_frozen_target

end Stage1Instances.THM_M_1078.ObligationTree
LEAN

(cd "$repo/Formalizations/Lean" && lake env lean "$tmp")
