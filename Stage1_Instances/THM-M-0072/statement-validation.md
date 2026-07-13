# THM-M-0072 Statement Validation

Item: `S56-M-0072-STATEMENT`
Base revision: `b99cf0ffec59c781f8bd25309bdfa53e77372a0a` (tree
`e015394246c3919236f2c6ba1a8184c37130f1e4`)

## Frozen target

`Stage1Instances.THM_M_0072.ThompsonTransferLemmaTarget` is Thompson 1968 Lemma
5.38(a)(i) in its exact printed universal form. It quantifies over a finite group of even order with
no index-two subgroup, then over a Sylow 2-subgroup, a maximal proper subgroup, and every element of
exact order two. It concludes ambient-group conjugacy to an element of the maximal subgroup.

The sole direct import is `Mathlib.GroupTheory.Sylow`; removing it fails. The checked `iff` to
`OutsideMaximalTarget` covers Lynd's common formulation. Its reverse direction handles an involution
already in the maximal subgroup through self-conjugacy. A second checked `iff` confirms that element
order measured in the Sylow carrier equals ambient-group order. No proof of the canonical target is
invoked or credited.

## Commands and results

All commands ran inside this worker clone. Lean reused the automation-provided canonical `.lake`
symlink read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0072` | 0 | rank 1102, planned, no legacy slot, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 at `98dc76e...`; Lake 5.0.0-src at the same Lean revision |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | mathlib revision `8a178386...ea95`, tree `bdc39a31...5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0072/Statement.lean)` | 0 | canonical target, two checked `iff` transports, four expected mutation type rejections, inside-`M` boundary, axiom reports, and explicit expression elaborated |
| `(cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0072/check_statement.py)` | 0 | expression SHA-256 `c8a89538...49051`; source `0e9a35c7...57aa`; Lean output `64a08c83...81d6`; four mutations distinguished; only import necessary; pins matched |
| `python3 -B Stage1_Instances/THM-M-0072/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | reconciled planned H1/M3/R4 dossier, exact inventory, statement receipt, worker packet, and six open tasks agree |
| JSON parsing, Python compilation outside the owned path, prohibited construct scan, and scoped whitespace checks | 0 | all structured artifacts parse, validators compile, no prohibited Lean construct occurs, and no whitespace diagnostic remains |

## Mutation and boundary policy

The removed-hypothesis mutation drops the no-index-two premise. The changed-domain mutation
restricts the ambient group to commutative groups. The binder-scope mutation chooses one conjugate
before seeing the involution. The boundary mutation changes exact order two to exact order four.
Lean rejects each as a term of the canonical target, and the checker confirms distinct fully
explicit expressions. These checks establish structural target identity; they do not claim
countermodel proofs for each mutation.

The checked statement transports report `propext`, `Classical.choice`, and `Quot.sound`; the
inside-maximal boundary reports `propext` and `Quot.sound`. These are statement-level foundation
observations, not a canonical proof or full trust audit.

## Status boundary

This is provisional statement evidence pending master acceptance. The catalog's 1964/1968 conflict,
source preservation, incorporated definitions, errata, translation, complete source mapping, and
independent `H0` review remain open. So do anchor/provenance auditing, obligation and graph freezes,
proof and composition, readable reconstruction, hermetic replay, independent verification, release,
audit completion, and theorem completion.
