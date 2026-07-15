# THM-M-0729 proof blocker at `062e0b53` (slot55)

Item: `S56-M-0729-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T18:41:27+08:00`

Base revision: `062e0b530c644c6d9c62556518568dd91a7374cd`

Base tree: `0879a3d554dc3011e1c5b513107c330547ea185c`

## Verdict

`blocked`. No eligible placeholder-free Lean 4 body was implemented or found for the exact root
`Stage1Instances.THM_M_0729.PCPTheorem`. The proof item stays `[ ]`; lifecycle stays `planned`; the
root vector stays `[H3, M3, R4]`; audit completion and theorem completion stay false.

The checked `root_of_directionalPackage` theorem is conditional assembly. Its premise is exactly
the conjunction of both missing class inclusions and therefore proves neither inclusion. The
immediate root cut remains:

- `M0729-D-NP-PCP`: fixed-predicate checker normalization, a robust-gap theorem, PCP composition,
  logarithmic-randomness and constant-query accounting, perfect completeness, and soundness-half;
- `M0729-D-PCP-NP`: finite oracle-bit certificates, exhaustive logarithmic-randomness enumeration
  with a polynomial-time machine proof, and the finite below-threshold branch.

The frozen checker is stricter than a generic informal PCP interface: `Checker.decide` receives
only `(input, oracleAnswers)`, not the random tape or query positions. An external PCP theorem would
still need a checked transport to this interface. Pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` contains deterministic Turing-machine,
finite-cardinality, polynomial, and logarithm support, but no NP/PCP development or terminal PCP
theorem. Even `Turing.TM2ComputableInPolyTime.comp` is only a discarded source `proof_wanted`
marker, not a declaration. The immutable anchor audit claims no compatible external terminal body.

Supplying `DirectionalPackage` as a premise, axiom, bodyless declaration, or assumed external
result would be a prohibited placeholder or conditional theorem substitution. None was added.

## Required Split

The owned path contained sixteen integrated proof-blocker/recheck JSON packets before this run.
Blueprint section 10.2 and the execution skill require splitting an item after five unresolved
execution ticks. The authoritative DAG nevertheless records `attempts: 0` and `children: []`.
The integration lane should stop assigning this monolithic item and create dependency-legal child
nodes for `M0729-D-NP-PCP` and `M0729-D-PCP-NP`, further divided by the ten frozen packages. This
worker did not edit the authoritative DAG or generated checklist.

The required predecessor `S56-M-0729-OBLIGATION_TREE` remains provisional `[_]`, not master
accepted. That independently prevents proof-node master acceptance.

## Validation

All commands ran in this worker clone. The pre-existing untracked `Formalizations/Lean/.lake`
symlink points to canonical pinned artifacts and was reused read-only. No `lake update`, `lake
build`, dependency clone/fetch/checkout, network request, or `.lake` mutation was performed. Lean
outputs were confined to disposable directories and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed all 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0729` | 0 | Rank 766; `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0729/check_anchor_audit.py` | 0 | Immutable pins and source hashes agreed; no exact root candidate is claimed; root remains M3. |
| `python3 Stage1_Instances/THM-M-0729/check_obligation_tree.py` | 0 | Passed 19 obligations and 76 typed edges; both directional packages remain open. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0729/Statement.lean` | 0 | Printed the exact `PCPTheorem` expression. |
| Disposable three-module `lake env lean --trust=0 -t0` replay | 0 | The exact statement, conditional assembly, and blocker probe elaborated; reported axioms were `propext`, `Classical.choice`, and `Quot.sound`; polynomial-time composition remained unavailable as expected. |
| Scoped repository and pinned-mathlib PCP search | 0 | Exact probabilistic-PCP declarations were confined to this dossier; no terminal inclusion or root body was found. |
| Search for `proof_wanted TM2ComputableInPolyTime.comp` | 0 | Pinned mathlib records only the discarded marker at `Computable.lean:284`. |
| Prohibited-device scan of checked local Lean files | 1 expected | No `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe/oracle device, `native_decide`, or `implemented_by` was found. |
| Frozen-input, executable, and dependency digest checks | 0 | Statement, composition, audit, registry, graph, validation, manifests, skill, Lean executable, and pinned dependency identities matched the paired JSON. |
| Scoped diff from preceding blocker base `118d66d1` | 0 | No frozen proof input, dependency pin, or proof body changed. |

`check_statement.py` was also started. Its unbounded five-elaboration recipe did not complete within
the bounded observation window under concurrent shared-environment load, so it is not claimed as a
passing command in this packet. The direct exact-statement elaboration above passed, and no
dependency repair was attempted.

## Reopen Condition

After the required split, implement both frozen directional packages and their normalization,
reduction, resource, certificate, enumeration, and boundary dependencies without placeholders.
Alternatively, integrate an immutable, license-compatible Lean 4 terminal proof of the exact
target with complete dependency and proof-body provenance, then rerun exact-type, trust,
placeholder, provenance, and composition checks.

This is current-base nonrelease blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0729-PROOF`, promote scheduler state, close an obligation or the root, or claim audit
completion, validation, release, theorem completion, receipt acceptance, or master acceptance.
Because the assigned phase is not genuinely self-tested complete, `.stage1-worker-selftest.json`
remains absent.
