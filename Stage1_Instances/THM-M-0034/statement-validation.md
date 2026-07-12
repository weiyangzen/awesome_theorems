# THM-M-0034 statement validation

Item: `S56-M-0034-STATEMENT`. Base revision:
`0ea006c25dcbfe400adbb084c0a3476a9b271741`; base tree:
`ff2e3bde08d7f5d6c83519160a4a6bd2cb7526db`.

## Frozen target

`Stage1Instances.THM_M_0034.QuillenSuslinTarget` quantifies over a field `k`, a positive
natural number `n`, and a module `P` over `MvPolynomial (Fin n) k`. Given finite generation and
projectivity, it concludes `Module.Free (MvPolynomial (Fin n) k) P`. The coefficient and module
universes are independent. The target includes the zero module, but not zero or infinitely many
variables.

The source root is the field specialization of the PID freeness conclusion in Suslin's Theorem
3* on journal page 1066, aligned with the field question and affirmative answer on page 1063. The
primary Russian scan was inspected and pinned by SHA-256, but independent translation, errata
review, Quillen full-text reconciliation, and master source acceptance remain open. Consequently
this statement work retains `H1` and makes no `H0` source claim.

## Commands and results

All commands ran from the repository root on 2026-07-13 (Asia/Shanghai), except where a working
directory is stated. The automation-provided canonical `.lake` symlink was reused read-only. No
update, build, dependency clone/fetch, or `.lake` mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0034` | 0 | rank 1078; planned; no legacy slot; theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0034/Statement.lean` | 0 | target, four expected identity rejections, and fully explicit expression elaborated |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0034/check_statement.py` | 0 | exact expression/source/output hashes, three deletion probes, four distinct mutation fingerprints, authority item, imports, and pins agree |
| deletion probe without `Mathlib.Algebra.Module.Projective` | 1 expected | `Module.Projective` is unknown |
| deletion probe without `Mathlib.Algebra.MvPolynomial.Basic` | 1 expected | `MvPolynomial` is unknown |
| deletion probe without `Mathlib.RingTheory.Finiteness.Defs` | 1 expected | `Module.Finite` is unknown |
| `python3 -m json.tool` over the statement JSON, receipt, and worker packet | 0 | all structured artifacts are valid JSON |
| prohibited-construct scan over owned `.lean` files | 1 expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in source |
| `git diff --check -- Stage1_Instances/THM-M-0034 .stage1-worker-selftest.json`; per-new-file `git diff --no-index --check /dev/null <file>` loop | 0 | no whitespace diagnostics |

## Mutations and boundary

The validator serializes the root and each mutation under the same explicit/universe options and
requires distinct SHA-256 fingerprints. Lean also rejects each mutation as a term of the root via
`#check_failure`: removal of finite generation, replacement of the field by an arbitrary
commutative ring, existential scoping of the variable count, and inclusion of zero variables. This
kills definitional statement identity; it does not assert that the stronger mutations have no
logical implication to the root.

No alternate encoding is credited because no equality, iff, or directional transport was needed
for the selected root. The three narrow direct imports are individually necessary under deletion.
The broader `Mathlib.RingTheory.MvPolynomial.Basic` module and any target proof module are absent.

## Status boundary

This is statement-only worker evidence pending master acceptance. It defines a proposition but no
inhabitant, and it neither audits nor credits a formal proof candidate. Source acceptance, anchor
audit, obligation registry, proof, composition, trust closure, readable reconstruction, hermetic
validation, independent verification, audit completion, and theorem completion remain open.
