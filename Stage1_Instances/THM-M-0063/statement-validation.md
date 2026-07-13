# Statement validation

Item: `S56-M-0063-STATEMENT`
Base revision: `ebd5f75831296a8a35e7b33013b964f2baf31bb9`

## Frozen target

`Stage1Instances.THM_M_0063.CayleyTheoremTarget` quantifies over an arbitrary universe-polymorphic
group `G` and says that `G` is multiplicatively equivalent to the range subgroup of its
left-regular permutation representation `MulAction.toPermHom G G`. `Nonempty` makes the existence
claim a proposition while retaining the exact `MulEquiv` conclusion. The trivial, finite, and
infinite cases remain in scope; no `Nontrivial`, `Fintype`, `Finite`, `DecidableEq`, commutativity, or
countability premise is added.

`PermutationSubgroupExistenceTarget` expresses the catalog's literal "some permutation group"
wording on the same carrier. The statement module kernel-checks only the implication from the more
specific regular range target to that existential formulation. It does not claim an unproved
equivalence or use the Cayley proof anchor.

## Minimal imports

The only direct imports are `Mathlib.Algebra.Group.Action.End` for `MulAction.toPermHom` and
permutation-action vocabulary, and `Mathlib.Algebra.Group.Subgroup.Ker` for `MonoidHom.range` and its
subgroup carrier. The validator deletes each import separately and requires elaboration to fail.
The broader `Mathlib.GroupTheory.Perm.Subgroup` module is absent, and the statement run verifies that
`Equiv.Perm.subgroupOfMulAction` is unavailable. Anchor discovery, provenance, and proof credit
therefore remain in the dependent anchor-audit phase.

## Commands and results

All commands ran in this worker clone. Lean commands used the automation-provided pinned `.lake`
symlink read-only; no dependency update, build, clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0063` | 0 | rank 1094; planned; no legacy slot; theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0063/Statement.lean)` | 0 | exact target, implication transport, removed-hypothesis rejection, three structural mutation rejections, two boundary propositions, anchor exclusion, axiom report, and explicit expression elaborated |
| `(cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0063/check_statement.py)` | 0 | expression `40929846...1a1a`; source `37e52256...f950`; Lean output `b5c7b70b...e9f1`; both import deletions fail; all four mutation classes killed |
| `python3 -B Stage1_Instances/THM-M-0063/check_intake.py` | 1 | expected historical failure: the checker binds the superseded pre-statement snapshot and is not cited as current statement evidence |
| `python3 -m json.tool <path>` separately for `instance.json`, `intake-receipt.json`, `statement.json`, `statement-receipt.json`, `task-dag.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts parse; exact argv for each path is recorded in `statement-receipt.json` |
| `rg -n '\b(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)\b\|\b(TODO\|FIXME\|placeholder)\b' Stage1_Instances/THM-M-0063 --glob '*.lean'` | 1 | expected no match; no prohibited token or marker |
| `git diff --check -- Stage1_Instances/THM-M-0063 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; `check_statement.py` also validates trailing whitespace and final newlines for every owned file and the worker packet |

## Result boundary

The statement node is self-tested and proposes `[_]` for integration review. This evidence freezes
the exact conventional target and environment only. It supplies no Cayley theorem proof, accepted
source review, anchor provenance, obligation registry, proof composition, readable reconstruction,
hermetic release evidence, independent verification, master acceptance, or theorem-completion
credit.
