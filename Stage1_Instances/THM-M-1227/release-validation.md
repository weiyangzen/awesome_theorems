# THM-M-1227 release reconciliation

Item: `S56-M-1227-RELEASE`. Base revision:
`ed9193169ea1291e0e28619c37c2594f6452edc6`.

## Exact verdict

`blocked`. The lifecycle remains `planned`, the accepted root vector remains
`[H2, M4, R4]`, and both `audit_complete` and `theorem_complete` are false. There are no accepted
receipt IDs. This is a self-tested negative release decision, not theorem completion, release, or
master acceptance.

The first workflow failure is `dependency.S56-M-1227-VALIDATION.master_acceptance`. The validation
receipt is only provisional worker evidence with `accepted=false` and `release_grade=false`. Its
checker is also a historical validation-turn recipe: it requires that turn's root self-test packet
and hard-binds revision `a1a7e939e58f103f5ff5d23af51437fa8658aa04`, so this release does not
misreport it as a current-HEAD replay.

## Evidence reconciliation

The frozen target and zero-data branch have real, narrow Lean evidence. A fresh current-run replay
elaborates `Statement.lean` and checks `zero_isLerayHopfSolution` and
`lerayHopfExistence_of_eq_zero` at trust zero. Both declarations are sorry-free and report exactly
`propext`, `Classical.choice`, and `Quot.sound`. This validates only a local implementation
candidate for `M1227-B-ZERO`; the registry fingerprint is still planned and no closure is accepted.

There is no theorem declaration for the canonical general target. The authoritative graph records
no closed obligations, keeps the root at `M4`, and preserves the five-node cut
`M1227-N-DATA`, `M1227-N-GLOBAL`, `M1227-C-GALERKIN`, `M1227-C-BOUNDS`, and
`M1227-C-COMPACT`. The first theorem failure is `proof.M1227-N-DATA.kernel_closure`.

`AUDIT-Z` is blocked independently. Exact primary-source theorem/page/assumption/errata review and
independent H0 acceptance are absent. The scope map describes dimensions two or three, optional
forcing, and a source-prescribed weak trace, while the frozen Prop is three-dimensional, unforced,
and imposes a strong squared-L2 trace. The test class and dissipation formulation also remain open
source-equivalence questions. No independently reviewed R0 reconstruction exists.

The first release-specific failure is `S56-10.6-HERMETIC-COLD-BUILD`. The fresh narrow replay uses
the automation-provided shared warm `.lake` symlink, not an immutable empty-cache cold build with
offline restoration. Complete transitive provenance/TCB/SBOM/license closure, two independent
signed runner attestations, an independently implemented minimal verifier, protected adversarial
CI, and a deterministic content-addressed release bundle are all absent.

## Commands and results

Commands ran from the worker clone on 2026-07-15 in `Asia/Shanghai`. Existing pinned Lean artifacts
were reused without mutation. No `lake update`, `lake build`, clone, fetch, checkout, dependency
mutation, or network request ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets and ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1227` | 0 | Rank 416 remains planned, L0/rework-required, and theorem-incomplete. |
| `python3 Stage1_Instances/THM-M-1227/check_obligation_tree.py` | 0 | 21 obligations and 63 typed edges passed; the root remains M4 with the five-node cut. |
| `python3 Stage1_Instances/THM-M-1227/check_proof.py` | 0 | The B-ZERO implementation candidate and evidence hashes passed; the exact root remains open. |
| `bash Stage1_Instances/THM-M-1227/check_proof.sh` | 0 | Fresh isolated trust-zero replay checked both zero-data declarations as sorry-free with the expected axiom set. |
| `python3 -I -B Stage1_Instances/THM-M-1227/check_release.py` | 0 | Current authority, evidence hashes, fresh zero-branch Lean evidence, and all negative release gates reconciled to the blocked verdict. |
| JSON parsing, Python syntax compilation, scoped hygiene checks, and `git diff --check` | 0 | Structured artifacts parsed, the checker compiled outside the repository, and whitespace/file hygiene passed. |

Retry requires current dependency-legal validation and exact-root proof closure, then accepted
H0/R0 and audit reconciliation, complete transitive provenance and TCB evidence, a separately
provisioned cold offline-capable release run, independent verification, a deterministic bundle, and
master acceptance.

Status boundary: this artifact self-tests only the negative release decision. It supplies no
accepted `M0`, `E0`, `E1`, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or master acceptance.
