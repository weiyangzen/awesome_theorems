# THM-M-1088 validation-phase evidence

Item: `S56-M-1088-VALIDATION`

Base revision: `9584b263a758e0dbab59344389554570dcf2e535`

## Verdict

`blocked`, with a self-tested worker handoff proposed as `[_]`. The validator re-elaborates the
exact frozen statement, the conditional engine-to-root composition, all four proof-phase partial
declarations, and four same-route declarations in a separate module namespace. Every Lean replay uses
`--trust=0` in fresh target output space. The recorded recipe runs under Bubblewrap with the host
root read-only, a private writable `/tmp`, a cleared environment, fixed locale/timezone/thread count,
and network disabled.

All nine declarations that emit axiom reports use exactly `propext`, `Classical.choice`, and
`Quot.sound`. The four separate-module declarations pass `assert_no_sorry` and `#print sorries`.
Frozen hashes, the clean pinned mathlib revision/tree/remote, two direct mathlib sources and compiled
artifacts, the toolchain, manifest, and license agree.

The separate-module bodies deliberately follow the proof-phase route and receive no implementation-
diversity or independent-verifier credit. This is narrow open-state validation, not theorem or release
validation. The predecessor proof receipt is provisional and `accepted=false`; it closes zero frozen
obligations. Neither proof nor
the separate module constructs the sharp centered-supremum MGF or inhabits
`ObligationTree.UpperTailEngine`. The exact root therefore remains `[H2, M3, R4]`, with
`audit_complete=false` and `theorem_complete=false`.

## Commands and results

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1088` | 0 | Rank 530; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1088/check_obligation_tree.py` | 0 | 19 obligations and 43 typed edges passed; exact root open M3 with architectural cut `M1088-T-ENGINE`. |
| `bash Stage1_Instances/THM-M-1088/check_proof.sh` | 0 | Four partial declarations elaborated under `--trust=0`; each reported exactly the selected three classical axioms. |
| recorded Bubblewrap/Python recipe in `validation-spec.json` | 0 | Exact statement, conditional composition, four partial proof bodies, and four same-route separate-module bodies replayed; nine exact axiom reports; zero frozen obligations closed. |
| `python3 -m json.tool` on `validation-spec.json`, `validation-receipt.json`, and `.stage1-worker-selftest.json` | 0 | All three structured artifacts parse. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m1088-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-1088/check_validation.py` | 0 | Validator syntax passed without writing into the repository. |
| `git diff --check -- Stage1_Instances/THM-M-1088 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |

The predecessor `check_proof.py` was not presented as current validation evidence: it is deliberately
bound to its proof-worker base revision and proof-phase self-test packet. This validation instead
hash-binds the integrated proof receipt and directly replays the Lean sources.

## Gate decisions

| Gate | Decision | Boundary |
|---|---|---|
| Exact local kernel replay | partial pass | The exact target statement, conditional composition, and eight partial declarations elaborate. No premise-free root declaration exists. |
| Placeholder and unsafe scan | pass | The four replayed Lean sources have no executable placeholder, bodyless declaration, unsafe/opaque/extern escape, implementation hook, or native oracle. |
| Observed axiom profile | partial pass | Nine reports are exactly the selected classical subset; the foundation policy and complete TCB inventory remain unaccepted. |
| Selected provenance | partial pass | Bound local sources and direct pinned mathlib source/artifact identities agree; complete transitive proof-body provenance and SBOM do not exist. |
| Proof dependency | fail closed | `S56-M-1088-PROOF` is only `[_]`, its receipt is `accepted=false`, and master acceptance is absent. |
| Exact theorem root | fail closed | `M1088-L-FINITE-CONCENTRATION`, the downstream limit/covariance packages, `M1088-T-ENGINE`, and the root remain unproved. |
| Hermetic release replay | fail closed | Network denial, read-only inputs, and fresh target outputs still reuse the shared warm dependency cache; there is no clean-checkout empty-cache cold build or offline archive restoration. |
| Independent verification | fail closed | The separate module duplicates the proof route and ran in this worker clone with the same identity and shared cache; it supplies neither implementation diversity nor a distinct signed runner/minimal release verifier. |

The validation implementation is genuinely self-tested as a truthful negative/open-root gate run and
is ready for master inspection. It grants no accepted obligation, `M0`, `E0/E1`, `AUDIT-Z`,
`THEOREM-Z`, theorem completion, release, or master-acceptance credit.
