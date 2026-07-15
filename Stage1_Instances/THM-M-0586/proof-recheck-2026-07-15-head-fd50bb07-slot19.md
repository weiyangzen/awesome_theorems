# THM-M-0586 proof phase blocked at `fd50bb07` (`slot19`)

Item: `S56-M-0586-PROOF`

Intent: `prove`

Recheck time: `2026-07-15T19:29:35+08:00` (`Asia/Shanghai`)

Base revision: `fd50bb07f6632a2ad0bdc17737c200432ee242c8`

Base tree: `ed66432029954bfa5b17e0afda5f3817eeb32d48`

## Verdict

`blocked`. No retained placeholder-free Lean 4 proof body inhabits the exact
frozen target `Stage1Instances.THMM0586.HighDimensionalPoincareTarget` or its
two exhaustive terminal branches. The target is the substantive theorem that
every compact Hausdorff smooth boundaryless `n`-manifold homotopy equivalent to
the unit `n`-sphere is homeomorphic to it when `n >= 5`.

The local declaration
`highDimensionalPoincare_of_dimension_packages` elaborates under `--trust=0`,
but it consumes `DimensionFivePackage` and `StableDimensionPackage`. Those
arguments are exactly the missing mathematical proofs. It checks exhaustive
branch composition; it does not prove either branch or the root. Likewise,
`generalizedTopologicalTarget_implies_highDimensionalTarget` is only transport
from an unproved broader target.

Pinned mathlib's matching source name,
`ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere`, occurs only under
`proof_wanted`. A fresh trust-zero imported-environment probe confirms that it
and the two related dimension-three marker names are unknown constants. The
bounded search of all `9,676` retained Lean package sources found no
h-/s-cobordism, surgery, Smale, or equivalent sphere-homeomorphism proof body.
The immutable external candidate already recorded in `anchor-audit.json` proves
only dimension zero.

No premise, axiom, placeholder, weaker target, changed dimension range, moving
dependency, or fake certificate was added. The root remains `[H2, M3, R4]` and
the theorem remains incomplete.

## Failed Gate And Required Split

The first failed gate is terminal proof-body availability for
`M0586-T-FIVE` and `M0586-T-STABLE`. They remain the minimal immediate open root
cut set. The expanded proof route is:

- `M0586-N-PUNCTURE`
- `M0586-C-DISKS`
- `M0586-C-COBORDISM`
- `M0586-L-HCOB`
- `M0586-L-FIVE`
- `M0586-L-STABLE`
- `M0586-C-GLUE`
- `M0586-T-FIVE`
- `M0586-T-STABLE`

Before this packet the repository already tracked `42` Markdown and `33` JSON
root-sized rechecks, while the authoritative DAG still recorded `attempts: 0`
and `children: []`. This is far beyond the five-unresolved-tick threshold in
rev-5.6 section 10.2. The retry condition is a master-owned reconciliation and
dependency-legal split into the frozen child obligations, not another unsplit
root attempt. This worker did not edit the authoritative DAG, generated
checklist, or item state.

## Current-Base Validation

All commands ran in this worker clone using the existing pinned Lake artifacts
read-only. No `lake update`, `lake build`, dependency clone/fetch, checkout,
network request, or `.lake` mutation was performed. Temporary Lean sources,
objects, and logs were kept under `/tmp` and removed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard structure passed for all 1546 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Target manifest passed with ranks 1 through 1546 and uniform L0/rework-required state. |
| `python3 scripts/stage1_target.py show THM-M-0586` | 0 | Rank 117 remains planned and theorem-incomplete. |
| `LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 600s python3 Stage1_Instances/THM-M-0586/check_statement.py` | 0 | Exact expression hash `48062820...346e7`; all four statement mutations killed. |
| `python3 Stage1_Instances/THM-M-0586/check_obligation_tree.py` | 0 | 18 obligations, 38 typed edges, denominator `bbeb74bb...07b3e`; root M3 and terminal packages M4. |
| `python3 Stage1_Instances/THM-M-0586/check_anchor_audit.py` | 0 | Anchor inventory, `proof_wanted` boundary, eight probes, and immutable pins passed. |
| Direct pinned Lean replay of `Statement.lean`, `ObligationTree.lean`, and `ProofBlockerProbe.lean` with `--trust=0 -t0` and temporary oleans | 0 | All elaborated. The composer/equivalence axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; the three marker names are unknown constants. |
| Temporary trust-zero direct wrapper using `e.nonempty_homeomorph_sphere n` | 1 (expected) | Lean reports that the environment does not contain `ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere`. |
| Bounded `rg --follow` over all pinned package Lean sources | 0 | Only five adjacent lines in mathlib's Poincare statement module; no terminal proof body. |
| Prohibited-construct scan over target Lean files | 1 (expected no match) | No executable `sorry`, `admit`, `sorryAx`, `native_decide`, custom bodyless declaration, unsafe/extern escape, or implementation override. |
| Pinned dependency revision/tree/clean checks | 0 | mathlib, flt-regular, and Batteries matched their immutable revisions and had clean worktrees. |
| Frozen-input diff from `1199aa8f3` | 0 | Statement, composition, probe, registry, graphs, anchor audit, recipes, lock, and toolchain are unchanged; intervening target changes are blocker records only. |

The companion JSON binds exact source hashes, environment revisions, command
results, output hashes, registry identity, cut set, and retry boundary.

## Exact Command Transcript

The simple validator commands are reproduced literally in the table above.
The compound validation commands were:

```bash
set -euo pipefail
ROOT=$PWD
LEAN_DIR="$ROOT/Formalizations/Lean"
TARGET_DIR="$ROOT/Stage1_Instances/THM-M-0586"
LEAN=$(cd "$LEAN_DIR" && lake env which lean)
LP=$(cd "$LEAN_DIR" && lake env printenv LEAN_PATH)
TMP=$(mktemp -d /tmp/thm-m-0586-slot19-fd50bb07.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET_DIR/Statement.lean" "$TARGET_DIR/ObligationTree.lean" \
  "$TARGET_DIR/ProofBlockerProbe.lean" "$TMP/"
cd "$TMP"
LEAN_PATH="$LP" "$LEAN" --trust=0 -t0 -o Statement.olean Statement.lean \
  > Statement.stdout 2> Statement.stderr
LEAN_PATH="$TMP:$LP" "$LEAN" --trust=0 -t0 -o ObligationTree.olean \
  ObligationTree.lean > ObligationTree.stdout 2> ObligationTree.stderr
LEAN_PATH="$TMP:$LP" "$LEAN" --trust=0 -t0 -o ProofBlockerProbe.olean \
  ProofBlockerProbe.lean > ProofBlockerProbe.stdout 2> ProofBlockerProbe.stderr
sha256sum Statement.stdout ObligationTree.stdout ProofBlockerProbe.stdout
sha256sum Statement.stderr ObligationTree.stderr ProofBlockerProbe.stderr
sha256sum Statement.olean ObligationTree.olean ProofBlockerProbe.olean
cat ObligationTree.stdout
cat ProofBlockerProbe.stdout
wc -c Statement.stderr ObligationTree.stderr ProofBlockerProbe.stderr
```

That replay exited `0`. Its three stdout hashes were `13268e72...ade7`,
`b5b6811e...f70`, and `76878cc0...695b`; all stderr files were empty. Its olean
hashes were `902abcbc...2dc`, `d9a6b306...3db`, and `6747efd6...f4a1`.

The expected-failure wrapper probe was:

```bash
set -uo pipefail
ROOT=$PWD
LEAN_DIR="$ROOT/Formalizations/Lean"
TARGET_DIR="$ROOT/Stage1_Instances/THM-M-0586"
LEAN=$(cd "$LEAN_DIR" && lake env which lean)
LP=$(cd "$LEAN_DIR" && lake env printenv LEAN_PATH)
TMP=$(mktemp -d /tmp/thm-m-0586-wrapper-fd50bb07.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET_DIR/Statement.lean" "$TMP/Statement.lean"
cat > "$TMP/Attempt.lean" <<'EOF'
import Statement

open ContinuousMap
open scoped Manifold ContDiff

namespace Stage1Instances.THMM0586

universe u

theorem attemptedPinnedWrapper : HighDimensionalPoincareTarget.{u} := by
  intro n _ M _ _ _ _ _ e
  exact e.nonempty_homeomorph_sphere n

end Stage1Instances.THMM0586
EOF
cd "$TMP"
LEAN_PATH="$LP" "$LEAN" --trust=0 -t0 -o Statement.olean Statement.lean \
  > Statement.stdout 2> Statement.stderr
set +e
LEAN_PATH="$TMP:$LP" "$LEAN" --trust=0 -t0 Attempt.lean \
  > Attempt.stdout 2> Attempt.stderr
code=$?
set -e
printf 'exit=%s\n' "$code"
sha256sum Attempt.lean Attempt.stdout Attempt.stderr
cat Attempt.stdout
cat Attempt.stderr
if [ "$code" -eq 0 ]; then exit 91; fi
```

It observed the expected Lean exit `1` and `lean.invalidField` diagnostic. The
source/stdout/stderr hashes were `f4cdcf3e...aad`, `1245c3ed...83e`, and the
empty-stream hash `e3b0c442...855`.

The retained-source, placeholder, dependency, frozen-input, and retry-count
commands were:

```bash
find -L Formalizations/Lean/.lake/packages -type f -name '*.lean' | wc -l
TMP=$(mktemp /tmp/thm-m-0586-search.XXXXXX)
trap 'rm -f "$TMP"' EXIT
rg -n --follow -i --glob '*.lean' \
  'nonempty_homeomorph_sphere|h.?cobord|s.?cobord|whitehead torsion|manifold surgery|surgery exact|smale.{0,30}poincar|generalized.{0,30}poincar' \
  Formalizations/Lean/.lake/packages > "$TMP"
wc -l < "$TMP"
sha256sum "$TMP"
cat "$TMP"

rg -n --pcre2 \
  '^\s*(?:theorem|lemma|example|def|opaque|abbrev)?[^\n]*(?:\b(?:sorry|admit|sorryAx|native_decide)\b)|^\s*(?:axiom|constant|opaque)\b|^\s*(?:unsafe|extern)\b|implemented_by' \
  Stage1_Instances/THM-M-0586 --glob '*.lean'

for p in mathlib flt-regular batteries; do
  git -C "Formalizations/Lean/.lake/packages/$p" rev-parse HEAD
  git -C "Formalizations/Lean/.lake/packages/$p" rev-parse HEAD^{tree}
  git -C "Formalizations/Lean/.lake/packages/$p" status --porcelain
done

git diff --quiet 1199aa8f3 -- \
  Stage1_Instances/THM-M-0586/Statement.lean \
  Stage1_Instances/THM-M-0586/ObligationTree.lean \
  Stage1_Instances/THM-M-0586/ProofBlockerProbe.lean \
  Stage1_Instances/THM-M-0586/obligation-registry.json \
  Stage1_Instances/THM-M-0586/typed-graphs.json \
  Stage1_Instances/THM-M-0586/anchor-audit.json \
  Stage1_Instances/THM-M-0586/validation-specs.json \
  Formalizations/Lean/lake-manifest.json Formalizations/Lean/lean-toolchain

git ls-files 'Stage1_Instances/THM-M-0586/proof-recheck-*.md' | wc -l
git ls-files 'Stage1_Instances/THM-M-0586/proof-recheck-*.json' | wc -l
jq '.items[] | select(.id == "S56-M-0586-PROOF") |
  {state,attempts,children,depends_on}' Docs/Stage1_Execution_DAG_rev-5.6.json
```

Because the assigned proof phase is not complete, no
`.stage1-worker-selftest.json` is emitted. This packet is current-base blocker
evidence only. It is not a proof receipt, does not satisfy
`S56-M-0586-PROOF`, changes no scheduler authority, and claims no M0 state,
audit completion, theorem completion, validation, release, or master
acceptance.
