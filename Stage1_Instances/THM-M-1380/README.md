# THM-M-1380 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item `Jacobi定理`
(Jacobi theorem). The repository supplies only Carl Jacobi, the year 1837, and the gloss
`Hamilton-Jacobi方程的完全解` (a complete solution of the Hamilton-Jacobi equation). It gives no
bibliography, formula, definitions, hypotheses, quantified conclusion, or proof source. Its
`已验证` (verified) field is explicitly untrusted metadata.

## Intake result

The words identify a Hamilton-Jacobi theorem family, not one proposition. In standard treatments,
a "complete solution" may mean a complete integral depending on as many independent parameters as
configuration variables, a theorem that such an integral generates a canonical transformation and
integrates Hamilton's equations, a local characteristic result, or a separated solution for an
autonomous Hamiltonian. These have different domains, regularity and nondegeneracy assumptions,
parameter counts, local/global scope, and conclusions.

Jacobi's 1837 Crelle article and modern statement-family discriminators were inspected. They give
compelling context for a complete-integral reading, but the catalog cites none of them and does not
select a theorem boundary. They therefore receive no canonical-statement or `H0` credit.

## Formal boundary

`IntakeProbe.lean` elaborates only pinned generic smoothness, Frechet-derivative, product-derivative,
continuous-linear-map, and integral-curve APIs adjacent to possible future encodings. A bounded
exact-topic search found no Hamilton-Jacobi or complete-integral declaration in pinned mathlib or
repo-local Lean. These are intake discovery observations, not the downstream anchor audit.

The canonical mathematical statement and Lean expression remain null. The provisional root vector
is `[H5, M4, R4]`: `H5` records that the received wording is not yet a stable truth-valued
proposition, not that correctly stated Hamilton-Jacobi results are false; no source-identical Lean
artifact is credited; and no readable proof can attach to an unfrozen root. All six downstream
tasks remain open. No exact statement, accepted proof state, audit completion, theorem completion,
or master acceptance is claimed.
