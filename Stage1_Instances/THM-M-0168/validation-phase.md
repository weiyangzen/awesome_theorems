# THM-M-0168 validation-phase evidence

Item: `S56-M-0168-VALIDATION`. Base revision:
`7505614b75de56cf10bbd196a4aaa0ca2a117064`; base tree:
`730e162a2133e4a077d764043b5e722c1f7feb39`.

## Verdict

`blocked`, with a self-tested negative validation packet proposed as `[_]`.
The structured recipe replays the exact statement, frozen conditional
composition, affine-integration body, canonical transport, and trust-only
probe at Lean trust level zero. Each Lean process uses a fresh temporary
directory, read-only host root, fixed cleared environment, and unshared network
namespace. All six inspected declarations are transitively sorry-free and
report exactly `propext`, `Classical.choice`, and `Quot.sound`.

This does not validate Bernstein's theorem. The only provisionally closed
package is `M0168-T-INTEGRATE`. Every canonical-root declaration still consumes
`DerivativeRigidity`; graph geometry, PDE-to-minimality, stability,
logarithmic cutoff, curvature vanishing, and derivative rigidity remain open.
The exact root therefore remains `M2` with the six-node cut recorded below.

## Commands and results

Commands ran in this worker clone on 2026-07-15 (`Asia/Shanghai`). No
`lake update`, `lake build`, dependency clone/fetch, checkout, or `.lake`
mutation was performed.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0168` | 0 | rank 665; planned; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0168/check_statement.py` | 0 | expression `b5cef8a8...33254f5`; all four structural mutations killed; pinned mathlib revision agreed |
| `python3 Stage1_Instances/THM-M-0168/check_anchor_audit.py` | 0 | audit boundary, five Lean probes, pinned mathlib revision, and immutable external-candidate metadata passed |
| `python3 Stage1_Instances/THM-M-0168/check_obligation_tree.py` | 0 | 11 obligations and typed acyclic proof graph passed; frozen root open M2 |
| `bash Stage1_Instances/THM-M-0168/check_proof.sh` | 0 | disposable trust-zero replay rechecked affine integration and conditional canonical transport; axiom reports exactly matched the classical trio |
| execute `validation-spec.json` `argv` without shell interpolation | 0 | network-isolated trust-zero kernel/trust replay, selected provenance checks, and fail-closed gate decisions passed |
| `python3 -m json.tool` over spec, receipt, blocker, and worker packet | 0 | all four structured artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0168-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0168/check_validation.py` | 0 | checker syntax passed outside the repository |
| `git diff --check -- Stage1_Instances/THM-M-0168 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

The validator derives Lean through `lake env` in the manifest-pinned mathlib
checkout, then uses only existing compiled pinned paths and writes fresh local
oleans under `/tmp`. This avoids top-level package materialization and keeps the
canonical `.lake` symlink read-only. It is a network-isolated warm-cache run,
not a cold hermetic release run.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | Exact statement, composition harness, proof body, transport, and trust probe elaborate at trust zero with network denied. |
| Placeholder and observed trust | provisional pass | Parser-aware source scan and transitive sorry collectors pass; all six axiom reports contain only the selected classical trio. |
| Selected provenance | provisional pass | Frozen local hashes, clean pinned mathlib revision/tree/origin/license, four direct source/blob/olean triples, and Lean/Lake identities agree. |
| Proof dependency and exact root | fail closed | Proof is only worker-provisional and no premise-free `DerivativeRigidity` or exact root body exists. |
| Structured-state freshness | fail closed | The pre-proof registry and graphs still classify `M0168-T-INTEGRATE` as M4 with no evidence; only the provisional proof receipt closes it. |
| Complete trust and provenance | fail closed | No complete declaration/import/TCB/compiler/plugin/SBOM/license-archive closure or accepted foundation policy exists. |
| Hermetic reproduction | fail closed | Shared warm cache; no immutable clean checkout, empty-cache cold build, offline restoration, or deterministic release bundle. |
| Independent verification | fail closed | `Validation.lean` shares this worker, checkout, kernel, and cache; no distinct signed runner or independent minimal release verifier exists. |
| Human and readable review | fail closed | No pinpoint H0 source mapping or independently accepted R0 reconstruction exists. |

The first node gate is
`dependency.S56-M-0168-PROOF.master_acceptance_and_exact_root_closure`; the
first theorem package is `M0168-C-GRAPH`; and the first release gate is
`S56-10.6-HERMETIC-COLD-EMPTY-CACHE-REPLAY`. The remaining root cut is
`M0168-C-GRAPH`, `M0168-N-PDE-MINIMAL`, `M0168-L-STABILITY`,
`M0168-C-CUTOFF`, `M0168-L-CURVATURE`, and
`M0168-L-DERIVATIVE-RIGIDITY`.

The validation packet itself is genuinely replayed and self-tested, so the
worker handoff proposes only `[_]`. It grants no accepted receipt, accepted
obligation closure, M0/E0/E1, validation completion, `AUDIT-Z`, `THEOREM-Z`,
release, theorem completion, or master acceptance.
