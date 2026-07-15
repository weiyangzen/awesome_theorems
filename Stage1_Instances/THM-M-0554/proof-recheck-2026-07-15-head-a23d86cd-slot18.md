# THM-M-0554 proof-phase recheck: blocked

Item: `S56-M-0554-PROOF`

Intent: `prove`

Recheck time: `2026-07-15T09:06:06+08:00` through
`2026-07-15T09:14:50+08:00`

Base revision: `a23d86cd84f03c26102b43c6b1b3b6d0a7a31e61`

Base tree: `9268aa9f5379837642b6f748f01255e8744c4e78`

## Verdict

`blocked`. The exact Atiyah-Hirzebruch spectral-sequence proof body is absent
from the pinned dependency closure, and the frozen Lean proposition is not a
source-faithful encoding that this proof-only worker can honestly close. No
new proof body, frozen-obligation closure, composition certificate, or proof
receipt is claimed. The root remains `M4`.

`Proof.lean` already contains real, placeholder-free conditional composition
bodies. `dataOfBranches` consumes explicit E2, differential, convergence, and
naturality packages field by field; `statementShapeOfBranches` packages the
result; and `statementOfBranchFamily` reaches the literal `Statement` while
retaining the entire branch family as a premise. These declarations replay at
trust level zero and are sorry-free, but they construct none of the branch
packages and therefore cannot close a parent whose required children remain
open.

The unchanged immediate root cut is:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: a skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology E2 identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

## First Failed Gate

Exact-statement fidelity fails before positive root proof credit. The selected
human claim is the cohomological AHSS for a reduced generalized cohomology
theory on a finite CW complex. The frozen interface omits reducedness and
stores `pointIsPoint`, `exactnessAxiom`, `wedgeAxiomOrRepresentability`,
`finiteCW`, `exhaustive`, and `cellAttachments` as proposition-valued fields
without proofs. Its output chooses bare propositions for
`coefficientConvention`, `strongConvergence`, and `naturalityInSpace`, while
`filtrationIsInducedBy` is only `K.skeleton = K.skeleton`.

Thus a zero spectral-sequence with output-selected `True` propositions can
inhabit the literal target without constructing the mathematical AHSS. That
diagnostic term is deliberately not retained or credited because doing so
would be a fake result under the exact-statement and child-to-parent
composition gates.

Predecessor authority is also unresolved. The global obligation-tree item is
only provisional (`[_]`), `instance.json` still records null canonical formal
identity fields, and the local `task-dag.json` remains unfrozen with proof
blocked by predecessors. This proof-only recheck does not rewrite those
authorities.

Pinned mathlib provides a generic cohomological spectral-sequence container,
finite-CW substrate, and singular homology, but the scoped package scan found
no AHSS, generalized-cohomology, exact-couple, or strong-convergence terminal
body. `Mathlib/Algebra/Homology/SpectralObject/SpectralSequence.lean` still
labels its intended spectral-sequence and homology-data constructors `TODO`.

## Validation

All Lean commands reused the automation-provided symlink to the canonical
pinned Lake artifacts. No update, build, dependency clone/fetch, network
operation, or `.lake` mutation ran. All Lean objects and logs were written to
fresh temporary directories and removed by traps.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lane `frontier_deep_formalization_debt`; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | 32 obligations and 91 typed edges passed; denominator `3c72072a...8048b`; root remains open at `M4`, with no composition certificate or proof closure credited. |
| Isolated pinned `lean --trust=0 -t0` recipe below | 0 | `Statement.lean`, `Proof.lean`, and `DifferentialProbe.lean` elaborated with Lean 4.29.0; temporary objects were 429072, 280728, and 15576 bytes. |
| `#print axioms` in `Proof.lean` | 0 | All three conditional declarations reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| `#print sorries` in `Proof.lean` | 0 | All three conditional declarations reported `Declarations are sorry-free!`. |
| Pinned-package AHSS/generalized-cohomology/exact-couple/strong-convergence scan | 1 | Expected no-match result: no pinned terminal proof candidate. |
| Prohibited-device scan over owned Lean sources | 1 | Expected no-match result: no `sorry`, `admit`, `axiom`, `sorryAx`, unsafe declaration, or oracle. |
| `jq empty` over the 31 pre-existing top-level owned JSON artifacts, plus `jq empty` on this new JSON record | 0 | Every structured JSON artifact parsed. |
| `git diff --check -- Stage1_Instances/THM-M-0554 .stage1-worker-selftest.json`, plus `git diff --no-index --check /dev/null <new-artifact>` for each new untracked record | 0 / 1 | The tracked-diff check passed; each no-index check returned the expected content-difference status 1 with no whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest absent because this proof phase is blocked. |

The isolated Lean recipe was:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-0554
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0554-slot18.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -R "$target" -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -R "$target" -o "$tmp/Proof.olean" Proof.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -R "$target" -o "$tmp/DifferentialProbe.olean" DifferentialProbe.lean
```

The statement and proof logs had SHA-256 digests
`f1690fd11232bafbe452f7a63a140204ae23ca3a0f90e0126f4b22dacfd54d30`
and `8cfbfe08991a8a319a2a3a003e890b38e0c094dcf5971f158f65b3cb54c172a1`.
The differential probe log had SHA-256 digest
`30cba6d30c04fd4f4b0748a62294bccfe84c6b51e2453f9290c805b9cc041a56`.
An independent worker replayed `Statement.lean` and `Proof.lean` and obtained
the same object sizes and log hashes.

## Retry Condition

First publish and master-accept a source-faithful statement, reconcile the
instance/task/statement authorities, and issue obligation-registry version 2
with exact branch fingerprints. Then construct and compose all four root-cut
packages without placeholders. Alternatively, pin an immutable compatible
Lean 4 AHSS proof and pass exact-type, provenance, trust, and composition
checks.

This is durable current-base blocker evidence only. It does not satisfy
`S56-M-0554-PROOF`, propose `[_]`, close an obligation, complete the audit or
theorem, or authorize master acceptance. Because the assigned phase is not
genuinely self-tested as complete, `.stage1-worker-selftest.json` remains
absent.
