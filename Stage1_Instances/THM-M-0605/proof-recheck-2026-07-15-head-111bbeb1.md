# THM-M-0605 proof-phase recheck at base 111bbeb1

Item: `S56-M-0605-PROOF`

Recheck date: `2026-07-15T06:50:05+08:00`

Base revision: `111bbeb1a210ae4e8525a4342012921ab60e466f`

Base tree: `8f705aa79622bf1e9be0665ae1254313df21b4f6`

## Verdict

`blocked`. The exact target `Stage1.THM_M_0605.ExoticSevenSphereExists` has no
eligible terminal Lean 4 proof body in the repository or pinned dependency
closure. No proof body was added. The proof item stays `[ ]`, the root vector
stays `[H1, M4, R3]`, and root closure, audit completion, validation, release,
and theorem completion remain false.

The immediate frozen root cut is `M0605-T-WITNESS`: a specific smooth
seven-manifold together with a homeomorphism to the standard seven-sphere and
an `IsEmpty Diffeomorph` certificate. The first unavailable construction is
`M0605-C-BUNDLE`, the selected Milnor 3-sphere bundle over the 4-sphere with
its clutching and characteristic data. Its dependent total-space,
homotopy-sphere, topological-identification, bounding-manifold,
smooth-obstruction, standard-comparison, and nondiffeomorphism packages are
also open.

The local theorem `exoticSevenSphereExists_of_witness` is a genuine checked
composition term, but it consumes the complete witness package and constructs
none of it. Pinned mathlib contains the exact signature only as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`.
`proof_wanted` does not retain a declaration, and a direct trust-zero import
probe reports the name as unknown. Scoped searches across all pinned packages
and repo-local Lean sources found no alternate proof-bearing candidate.

Closing the target therefore requires a new formalization of the Milnor
sphere-bundle construction, its topological identification, and its smooth
obstruction, or an immutable compatible exact proof integrated into the
pinned closure. Assuming any missing package, treating `proof_wanted` as a
theorem, or returning only the conditional composer would be a placeholder or
substituted theorem and was not done.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused
read-only. Lean outputs were confined to disposable directories and removed.
No `lake update`, `lake build`, dependency clone/fetch, network request, or
`.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets and ranks passed. |
| `python3 scripts/stage1_target.py show THM-M-0605` | 0 | Rank 643; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0605/check_anchor_audit.py` | 0 | Exact marker, pins, discard semantics, and M4 boundary passed. |
| `python3 Stage1_Instances/THM-M-0605/check_obligation_tree.py` | 0 | 19 obligations and 90 typed edges passed; root remains open M4. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0605/Statement.lean` | 0 | Exact canonical target elaborated and printed. |
| trust-zero temporary-copy recipe below for `ObligationTree.lean` | 0 | Conditional composition elaborated; axioms were only `propext`, `Classical.choice`, and `Quot.sound`. |
| trust-zero temporary-copy recipe below for `AnchorAudit.lean` | 0 | Exact packaging transport and retained-marker rejection check passed. |
| direct trust-zero probe of the `proof_wanted` name | 1 | Expected negative evidence: `Unknown identifier`. |
| scoped retained-body searches | 0 | Only the discarded marker, local/duplicate statement and conditional composition, and non-proof metadata were found. |
| scoped prior-base diff | 0 | No statement, composition, registry, graph, audit, validation-spec, toolchain, or manifest input changed. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

The two trust-zero replays used the following exact pattern, first with the
obligation tree and then with `AnchorAudit.lean` and its corresponding
temporary-directory prefix:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0605-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0605/ObligationTree.lean "$tmp/ObligationTree.lean"
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300s \
  "$lean" --trust=0 -t0 -R "$tmp" ObligationTree.lean
```

The direct marker probe wrote these lines to a temporary `Probe.lean` and ran
the same pinned executable, `LEAN_PATH`, trust, timeout, and root options:

```lean
import Mathlib.Geometry.Manifold.PoincareConjecture
#check exists_homeomorph_isEmpty_diffeomorph_sphere_seven
```

It exited 1 with `Unknown identifier`.

The paired JSON artifact binds the current base and tree, source hashes,
registry denominator, pinned environment, commands, open cut set, and status
boundary.

## Retry Condition

Resume after placeholder-free implementations of the frozen bundle,
topological, and smooth-obstruction packages. Alternatively, integrate an
immutable compatible Lean 4 proof-bearing declaration of the exact target
with complete dependency and license evidence, then rerun the exact-type,
trust, provenance, and composition checks.

This is blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0605-PROOF`, proposes no state promotion, and supports neither root
closure nor theorem completion. Because the assigned phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` remains absent.
