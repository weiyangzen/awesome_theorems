# Exact-statement gate: blocked

Item: `S56-M-0537-STATEMENT`  
Theorem: `THM-M-0537`  
Base revision: `79350f6756ac2f7d72136216ef446106f56a6fb9`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
complete statement is `同调理论的公理化` ("axiomatization of homology theory"). This names a
framework, not a proposition, and the intake correctly leaves three non-equivalent roots open:

- a structure whose fields state the Eilenberg-Steenrod axioms;
- a model theorem proving that singular homology satisfies every selected axiom;
- a uniqueness or representation theorem for theories satisfying the axioms.

A structure only encodes assumed laws and is not a theorem that singular homology has them. A model
theorem has substantial construction and proof content. A uniqueness theorem has different domains,
hypotheses, and a natural-equivalence conclusion. Conjoining these choices, or selecting the most
convenient one, would broaden or substitute the source claim.

Even after selecting the root kind, the record does not fix reduced versus unreduced homology,
coefficients, integer versus nonnegative grading, the category of topological pairs, admissible
maps, exact forms of excision and exactness, the dimension and additivity conventions, naturality,
or equality versus natural isomorphism. Empty spaces, empty subspaces, point spaces, and negative
degrees are also unresolved. These choices alter domains, binders, hypotheses, and conclusions.

The identified 1945 article and 1952 monograph remain uninspected discovery candidates: the dossier
contains no immutable source copy, pinpoint definition/theorem/page, premise crosswalk, errata
disposition, or independent review. The adjacent `THM-M-0538` is a separate target and cannot supply
statement identity or proof credit. Therefore section 5 fails before minimal canonical imports, an
elaborated expression hash, checked transports, or meaningful hypothesis/domain/scope/boundary
mutations can be produced. No axiom, placeholder, assumed structure inhabitant, or substitute Lean
target was introduced. Machine status remains `M4` and theorem completion remains false.

## Lean boundary checked

`StatementProbe.lean` uses the existing pinned environment to elaborate the closest available
mathlib substrate with these imports:

```lean
import Mathlib.AlgebraicTopology.SingularHomology.HomotopyInvarianceTopCat
```

It checks `AlgebraicTopology.singularChainComplexFunctor`,
`AlgebraicTopology.singularHomologyFunctor`, and mathlib's equality of induced homology maps for
homotopic `TopCat` maps. Repository-wide pinned-mathlib source search found these
absolute singular-homology and homotopy-invariance APIs, but no complete Eilenberg-Steenrod package
on topological pairs. The probe establishes only that independent substrate elaborates; it is not
the canonical target and receives no statement or proof credit.

## Validation record

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). Lean used the existing canonical
`.lake` artifacts read-only; no update, build, clone, or fetch command was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0537` | 0 | rank 594, planned, L0/rework-required, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | SHA-256 values recorded in `statement-blocker.json` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| pinned-mathlib `rg` searches for homology-theory, Eilenberg-Steenrod, topological-pair, singular-homology, and homotopy APIs | 0/1 | found singular-homology substrate but no complete named axiom package; exit 1 searches mean no match |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0537/StatementProbe.lean` | 0 | the three substrate declarations elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0537/statement-blocker.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0537` | 0 | no output |

## Retry condition

An accountable source review must select an immutable primary-source edition and exact
definition/theorem/page, resolve every root and convention listed above, dispose of errata, and
independently approve the crosswalk. A later statement run can then encode that exact proposition,
minimize pinned imports, serialize its elaborated expression and environment, check alternate
transports, and run all four required mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
