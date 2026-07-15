# THM-M-0594 validation-phase evidence

Item: `S56-M-0594-VALIDATION`. Base revision:
`b366bdd9f72217b5465ccd19133760b911ed0b58`; base tree:
`987b635fe76400c0818b485a6e5fc7a7067311e4`.

## Verdict

`blocked`, with a self-tested fail-closed validation packet proposed as `[_]`.
The structured recipe copies the exact statement, compact specialization,
conditional compositions, partial proof bodies, empty boundary, and two
independently written differential probes into a fresh temporary directory.
It resolves the pinned executable and package path through `lake env`, then
invokes Lean directly at trust level zero inside a read-only, network-isolated
bubblewrap namespace.

This does not validate the unrestricted Whitney embedding theorem. The proof
dependency is worker-provisional and unaccepted, while `M0594-C-GLOBAL` still
has no premise-free construction for arbitrary inhabited noncompact manifolds.
The accepted root vector therefore remains `[H1, M3, R3]` and accepted proof
closure remains empty.

## Commands and results

Commands ran in this isolated worker clone on 2026-07-15 (`Asia/Shanghai`). No
`lake update`, `lake build`, dependency clone/fetch/checkout, or `.lake`
mutation was performed.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0594` | 0 | rank 255; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0594/check_obligation_tree.py` | 0 | 16 obligations and 46 typed edges passed; authoritative root remains open M3 |
| `bash Stage1_Instances/THM-M-0594/check_proof.sh` | 0 | disposable trust-zero replay confirmed the unconditional topological bridge and conditional exact-root composition are sorry-free with the expected three axioms |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0594/check_validation.py --probe` | 0 | network-isolated trust-zero replay checked all seven Lean modules; differential closure had 2 roots, 28110 declarations, 1052 modules, only the expected axioms, no unexpected bodyless declaration, and no unsafe declaration |
| execute `validation-spec.json` `argv` without shell interpolation | 0 | frozen inputs, kernel/trust observations, selected provenance, fail-closed gate decisions, receipt/blocker/spec, and worker packet agree |
| `python3 -m json.tool` over validation spec, receipt, blocker, and worker packet | 0 | all four structured artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0594-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0594/check_validation.py` | 0 | checker syntax passed outside the repository |
| `git diff --check -- Stage1_Instances/THM-M-0594 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

The replay uses Lean 4.29.0 and the existing compiled package paths from the
automation-provided canonical `.lake` symlink. Bubblewrap denies network and
exposes the host read-only except for a fresh temporary directory. This is
stronger than an ordinary warm replay, but remains shared-cache nonrelease
evidence, not section 10.6 cold hermetic evidence.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | Exact statement and every extant local body or composition elaborate at trust zero with network denied. |
| Placeholder and observed trust boundary | provisional pass | Lean `assert_no_sorry`, `#print sorries`, parser-aware scanning, and a transitive constant walk agree; checked declarations expose only `propext`, `Classical.choice`, and `Quot.sound`. This is observation, not accepted complete TCB closure. |
| Selected provenance | provisional pass | Frozen local hashes, clean pinned mathlib revision/tree/remote/license, four selected source/blob/olean triples, and executable identities agree. |
| Same-worker differential probe | provisional pass | `Validation.lean` independently reconstructs the topological bridge and conditional exact target without importing `Proof.lean`; it is not a distinct runner or independent theorem proof. |
| Proof dependency and exact root | fail closed | `S56-M-0594-PROOF` is only `[_]`, its receipt is unaccepted, and `M0594-C-GLOBAL` has no body. Conditional composers do not prove their premises. |
| Complete trust and provenance | fail closed | The foundation policy remains audit-pending and no accepted complete declaration/import/object/compiler/bootstrap/plugin TCB, SBOM, archive, or source-boundary closure exists. |
| Hermetic reproduction | fail closed | Shared warm cache; no immutable clean checkout, empty-cache cold build, offline archive restoration, or deterministic release bundle. |
| Independent verification | fail closed | No distinct signed runner, independently provisioned clean checkout, second attestation, or independently implemented minimal release verifier. |
| Human and readable review | fail closed | No independently accepted H0 primary-source crosswalk or R0 reconstruction exists. |

The first node gate is
`dependency.S56-M-0594-PROOF.master_acceptance`; the first mathematical gate is
`M0594-C-GLOBAL`; and the first release gate is
`S56-10.6-HERMETIC-COLD-EMPTY-CACHE-REPLAY`. The authoritative frozen cut
remains `M0594-C-GLOBAL, M0594-L-TOPOLOGICAL`; after provisional proof evidence
it would reduce to `M0594-C-GLOBAL`, pending master reconciliation.

The packet itself is genuinely replayed and self-tested, so the handoff
proposes only `[_]` for review. It grants no accepted obligation, exact root,
M0, validation completion, `AUDIT-Z`, `THEOREM-Z`, release, independent
verification, theorem completion, or master acceptance.
