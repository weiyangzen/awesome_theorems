# S56-M-1133-VALIDATION worker evidence

Validation date: 2026-07-14 (Asia/Shanghai). Base revision:
`bad90e2e2479d376609447202eb4f437789d0d11`.

The node-scoped validator copies the frozen statement, composition module, repo-local proof, and an
exact-type probe into a fresh temporary module tree. It invokes the pinned Lean executable with
`--trust=0` inside a bubblewrap sandbox with a read-only host root, isolated network namespace,
cleared environment, and writable temporary target outputs. The exact root, frozen composition,
eight material proof declarations, and import-dependent exact-type probe elaborate. Eleven
elaborator-aware no-sorry checks pass, and every machine axiom report is exactly `propext`,
`Classical.choice`, and `Quot.sound`.

`Validation.lean` deliberately imports `Proof.lean`: it checks the declaration's exact frozen type
but does not simulate a second mathematical proof. The immutable typed graph also preserves its
honest pre-proof observation. Both boundaries fail closed pending integration-lane reconciliation.

## Gate results

| Gate | Result | Evidence or boundary |
|---|---|---|
| Exact kernel replay | provisional pass | Fresh target oleans for `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `Validation.lean` pass under `--trust=0`. |
| Network/write isolation | provisional pass | Lean runs with outbound network isolated, host files read-only, and only the temporary module tree writable. |
| Target and composition | provisional pass | The exact heat maximum-principle root and equality-to-subsolution composition elaborate without a substituted theorem. |
| Placeholder and unsafe policy | pass | Eleven `assert_no_sorry` checks and a nested-comment-aware source scan find no admission, added axiom, unsafe injection, oracle, or native shortcut. |
| Axiom observation | pass as observation only | All reports contain the same three classical Lean/mathlib principles; the versioned foundation profile remains unaccepted. |
| Direct provenance | provisional pass | Local hashes, clean pinned mathlib revision/tree/origin/license, seven direct source/olean pairs, and tool digests agree. Complete transitive provenance and TCB closure remain open. |
| Structured-state freshness | fail closed | `typed-graphs.json` predates the proof and retains M3, `root_closed=false`, and cut `M1133-T-LIMIT`; only the master may reconcile it. |
| Source/readability | fail closed | The source is H2 with no pinpoint immutable edition, premise/errata audit, or independent review; every graph node remains R3. |
| Hermetic release replay | fail closed | The sandbox reuses the shared warm `.lake`; this is not a new clean checkout, cold empty-cache build, or offline restoration. |
| Independent verification | fail closed | The exact-type probe imports `Proof` and runs in this worker/cache; there is no distinct signed runner or independently implemented minimal verifier. |

The source gate also retains two concrete statement-record boundaries. The Lean regularity predicate
is slice-wise pointwise `ContDiffAt`, not joint `C2,1`, and it requires an ambient two-sided
derivative at `t = T`; exact correspondence with the textbook formulation is not yet reviewed.
Also, `statement.json` says dimension zero cannot satisfy the premises, but `U = univ` in
zero-dimensional Euclidean space is a counterexample to that metadata sentence. The kernel theorem
still quantifies and proves `n = 0`; the error blocks clean source/readability reconciliation rather
than the local Lean proof.

## Commands and results

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework-required

python3 scripts/stage1_target.py show THM-M-1133
  exit 0: rank 338, planned, theorem_complete=false

bash Stage1_Instances/THM-M-1133/check_proof.sh
  exit 0: exact three-module proof replay passed; all eight proof declarations
  reported exactly propext, Classical.choice, and Quot.sound

python3 Stage1_Instances/THM-M-1133/check_obligation_tree.py
  exit 0: frozen 16-obligation, 37-edge architecture and conditional
  composition passed; its historical pre-proof root remained open

/usr/bin/python3 -B Stage1_Instances/THM-M-1133/check_validation.py
  exit 0: trust-zero network-isolated exact-root replay, eleven no-sorry
  checks, direct provenance, structured-state boundary, receipt, and handoff passed

git diff --check -- Stage1_Instances/THM-M-1133 .stage1-worker-selftest.json
  exit 0: no output
```

No `lake update`, `lake build`, dependency clone/fetch, network dependency operation, or `.lake`
mutation was performed. The first node failure is proof master acceptance, the first validation
failure is accepted foundation/complete TCB closure, and the first release failure is the cold
hermetic gate. This is provisional `[_]` worker evidence, not `E0/E1`, accepted `M0-L`, `H0`, `R0`,
`AUDIT-Z`, `THEOREM-Z`, release, or theorem completion.
