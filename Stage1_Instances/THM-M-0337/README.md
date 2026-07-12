# THM-M-0337 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the metadata label "Connes cyclic
cohomology". The repository record names a cohomology theory rather than a theorem and describes
it only as "cohomology of noncommutative geometry". Intake preserves that ambiguity instead of
selecting a convenient result from the theory.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Source record | `THM-M-0337`, `康内斯循环上同调`, category functional analysis, and the untrusted status `已验证` | The status supplies neither a proposition nor proof evidence |
| Mathematical subject | Connes's cyclic cohomology as a theory associated with noncommutative algebras | Naming or defining the theory is not a theorem |
| Exact root | Not identifiable from repository source metadata | Statement work is blocked until an authoritative proposition is selected |
| Plausible but distinct roots | cyclic cocycle identities, the cyclic bicomplex, the SBI long exact sequence, Morita invariance, periodicity, or a pairing with K-theory | These claims have different domains, hypotheses, and conclusions; none is credited |
| Domain | An unspecified class of algebras, unspecified base ring or field, and unspecified algebraic/topological/bornological setting | Ordered binders, continuity/completeness assumptions, and coefficients remain open |
| Lean surface | Lean 4 plus pinned mathlib | No module, declaration, expression, or elaboration claim is made |
| Foundations and TCB | rev-5.6 Lean kernel policy | Exact toolchain fingerprint, imports, axioms, and dependency closure remain open |

## Intake verdict

Lifecycle is `planned`; the provisional root vector is `[H5, M4, R3]`. The first failed gate is
the exact human statement gate. Neither "cyclic cohomology" nor "cohomology of noncommutative
geometry" determines a proposition. Advancing by formalizing only a definition, or by silently
choosing the SBI sequence or Morita invariance, would substitute a new target.

The open follow-up tasks are recorded in `intake-tasks.json`. They require an authoritative source
decision before the statement task can freeze domains, assumptions, conclusion, and a Lean
expression. This intake claims no `H0`, Lean elaboration, proof credit, audit completion, or theorem
completion.

## Validation

The exact worker checks and their results are recorded in `validation.md`. They validate target
membership, repository-standard consistency, and this dossier's structure only; there is no Lean
proposition available to elaborate.
