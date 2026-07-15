# THM-M-0321 validation-phase evidence

Item: `S56-M-0321-VALIDATION`. Base revision:
`1729533156a59958dac4908793303a66434eb925`.

## Verdict

`blocked_after_self_test_pending_master_acceptance`. The exact frozen Markov-Kakutani root,
all proof-phase declarations, and a second exact-root composition elaborate at `--trust=0` in a
fresh temporary output tree. Every Lean process ran with fixed locale, timezone, and one thread
under Bubblewrap network isolation and a read-only host root. Both exact roots are sorry-free and
use only `propext`, `Classical.choice`, and `Quot.sound`. Lean's dependency-closure inspection
found 14374 declarations across 553 modules, no unexpected bodyless nonaxiom, and no unsafe
declaration. Frozen local hashes, seven selected mathlib source/blob/olean boundaries, tool
identities, the clean dependency pin, and the mathlib license agree.

This is deliberately nonrelease evidence. The proof prerequisite is only `[_]`. The separately
written validation root does not call `markovKakutani_proof`, but it shares the proof phase's
`finiteFamilyStep` and `continuousCompactnessUpgrade`; it is not an independent implementation or
distinct verifier. The shared warm `.lake` artifacts are not an empty-cache cold replay. The
accepted vector remains `[H2, M3, R4]`; `audit_complete=false` and `theorem_complete=false`.

## Frozen defect

The prerequisite architecture's `ObligationTree.CompactnessUpgrade` assumes compactness and a
finite-subfamily witness but omits continuity or closedness of the fixed sets. It is false for
arbitrary maps. The proof and validation roots correctly use `continuousCompactnessUpgrade`, which
consumes the canonical target's continuity hypothesis. No closure credit is assigned to the false
helper, `M0321-N-INFINITE`, or `M0321-T-UPGRADE`. The architecture owner must reconcile and refreeze
that interface; the validation worker did not modify prerequisite artifacts or authoritative state.

## Commands and results

All checks reused the automation-provided pinned `.lake` artifacts without update, build, clone,
fetch, or mutation.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0321` | 0 | Rank 687; planned, L0/rework-required, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0321/check_statement.py` | 0 | Exact expression hash `7a9628fca04eb72d787efad1f852517f4385377b3ad16f3eba662ccea4bb86a5` and four mutations passed. |
| `python3 Stage1_Instances/THM-M-0321/check_anchor_audit.py` | 0 | Exact target, rejected candidates, and pinned mathlib environment passed. |
| `python3 Stage1_Instances/THM-M-0321/check_obligation_tree.py` | 0 | Frozen 30-obligation registry and 33 typed edges passed in their pre-proof M3 snapshot. |
| `bash Stage1_Instances/THM-M-0321/check_proof.sh` | 0 | Disposable trust-zero exact-root replay passed with no placeholder or prohibited device. |
| `python3 -I -B Stage1_Instances/THM-M-0321/check_validation.py` | 0 | Network-isolated trust-zero replay, closure inspection, selected provenance, receipt, and fail-closed boundaries passed. |
| `python3 -m json.tool Stage1_Instances/THM-M-0321/validation-spec.json` | 0 | Structured argv recipe parsed. |
| `python3 -m json.tool Stage1_Instances/THM-M-0321/validation-receipt.json` | 0 | Node-specific validation receipt parsed. |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | Worker handoff parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0321-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0321/check_validation.py` | 0 | Validator compiled outside the repository tree. |
| `git diff --check -- Stage1_Instances/THM-M-0321 .stage1-worker-selftest.json` | 0 | No scoped whitespace diagnostics. |

The inherited `check_proof.py` was not used: after proof integration it still hard-codes the old
proof-worker commit, tree, changed-path set, and authoritative proof state `[ ]`, while the current
DAG correctly has proof state `[_]`. The validation checker independently binds the current base,
all proof inputs, proof receipt, exact target, dependency pin, and authoritative validation item.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | Statement, conditional interfaces, all proof bodies, exact root, and differential composition elaborated in fresh output space with `--trust=0`. |
| Placeholder and unsafe boundary | provisional pass | `assert_no_sorry`, `#print sorries`, closure inspection, and a nested-comment-aware source scan found no prohibited proof device or unexpected bodyless/unsafe declaration. |
| Selected provenance | provisional pass | Frozen hashes, terminal body identity, seven source/blob/olean triples, clean mathlib pin, remote, license, manifest, and tool hashes agree. |
| Dependency authority | fail closed | `S56-M-0321-PROOF` is not master-accepted and accepted evidence lists remain empty. |
| Frozen composition | fail closed | `CompactnessUpgrade` is false without continuity/closedness; `M0321-T-UPGRADE` remains open. |
| Complete trust/provenance | fail closed | No accepted theorem-specific foundation profile, complete transitive declaration/source/compiled-artifact inventory, TCB closure, or SBOM exists. |
| Hermetic release | fail closed | Shared warm `.lake`; no clean checkout, empty-cache cold bootstrap, offline-restorable archive, or deterministic bundle. |
| Independent verification | fail closed | The validation root shares proof helpers, worker, checkout, and cache; no distinct signed runner or independently implemented minimal verifier exists. |

The first node failure is `dependency.S56-M-0321-PROOF.master_acceptance`. The first release failure
is `S56-10.6-HERMETIC-COLD-BUILD`. This self-tested validation implementation proposes only worker
state `[_]`; it grants no accepted `M0-L`, release-grade `E0/E1`, `AUDIT-Z`, `THEOREM-Z`, release,
or theorem-completion credit.
