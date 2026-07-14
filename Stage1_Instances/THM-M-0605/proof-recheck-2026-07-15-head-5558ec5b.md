# THM-M-0605 proof-phase recheck at base 5558ec5b

Item: `S56-M-0605-PROOF`  
Date: `2026-07-15T07:23:26+08:00`  
Base revision: `5558ec5b162bfdfa95b44fafcf97b69a44d1ff37`

## Verdict

`blocked`. No eligible Lean 4 proof body for the exact target
`Stage1.THM_M_0605.ExoticSevenSphereExists` exists in the repository or the
pinned dependency closure. No proof body or obligation closure was added. The
proof item remains `[ ]`, the root vector remains `[H1, M4, R3]`, and root
closure, audit completion, validation, release, and theorem completion remain
false.

The immediate frozen root cut is `M0605-T-WITNESS`: one smooth
seven-manifold, a homeomorphism to the standard seven-sphere, and an
`IsEmpty Diffeomorph` certificate. The first unavailable construction is
`M0605-C-BUNDLE`, the selected Milnor 3-sphere bundle over the 4-sphere with
its clutching and characteristic data. Its total-space, homotopy-sphere,
topological-identification, bounding-manifold, smooth-obstruction,
standard-comparison, and nondiffeomorphism packages are also open.

The local theorem `exoticSevenSphereExists_of_witness` is a genuine checked
composition term, but it consumes the complete witness and constructs none of
it. The other checked theorem transports only the target's statement shape.
Choosing the standard sphere itself is no shortcut: its identity map is a
diffeomorphism, incompatible with the required `IsEmpty` certificate.

Pinned mathlib contains the exact signature only as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`.
`proof_wanted` leaves no retained declaration, and a direct trust-zero import
probe reports that name as unknown. Scoped searches across pinned packages and
repo-local Lean sources found no proof-bearing Milnor-sphere, clutching,
Eells-Kuiper, Kervaire-Milnor, or equivalent candidate. Assuming one of these
missing packages or returning only the conditional composer would be a
placeholder or a substituted theorem and was not done.

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
| Trust-zero disposable replay of `ObligationTree.lean` | 0 | Conditional composition elaborated; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Trust-zero disposable replay of `AnchorAudit.lean` | 0 | Exact packaging transport and retained-marker rejection check passed. |
| Direct trust-zero probe of the `proof_wanted` name | 1 | Expected negative evidence: `Unknown identifier`. |
| Scoped retained-body search | 0 | Only the discarded marker, statement/composer artifacts, and metadata probes were found. |
| Prohibited-device scan of the checked Lean files | 1 | Expected no-match exit; no prohibited proof device was found. |
| Scoped diff from prior recheck base `111bbeb1` | 0 | No statement, composition, registry, graph, audit, validation-spec, toolchain, manifest, or target-manifest input changed. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

The trust-zero replays used the following pattern for each checked file:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0605-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0605/ObligationTree.lean "$tmp/ObligationTree.lean"
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300s \
  "$lean" --trust=0 -t0 -R "$tmp" "$tmp/ObligationTree.lean"
```

The same recipe checked `AnchorAudit.lean`. The marker probe instead used a
disposable file containing:

```lean
import Mathlib.Geometry.Manifold.PoincareConjecture
#check exists_homeomorph_isEmpty_diffeomorph_sphere_seven
```

It exited 1 with `Unknown identifier`, confirming that the source marker is
not an importable theorem.

## Reopen Condition

Resume only after placeholder-free implementations of the frozen bundle,
topological, and smooth-obstruction packages are available. Alternatively,
integrate an immutable, compatible, proof-bearing Lean 4 declaration of the
exact target with complete dependency and license evidence, then repeat the
exact-type, trust, provenance, and composition checks.

This packet is blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0605-PROOF`, promote scheduler state, or support theorem completion.
Because the assigned phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` remains absent.
