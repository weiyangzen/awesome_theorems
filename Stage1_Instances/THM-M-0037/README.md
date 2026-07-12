# THM-M-0037 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Brauer group theorem. The
repository catalogue gives only the Chinese gloss `域上中心单代数的分类` ("classification of
central simple algebras over a field"), attributes it to Richard Brauer in 1932, and labels it
`已验证`. Under rev-5.6 that label is untrusted metadata, not an exact source statement, source
audit, Lean target, or proof receipt.

The gloss identifies a classical theorem family but does not choose among several materially
different claims: classification by stable matrix (Brauer) equivalence, construction of the
abelian group law on equivalence classes, the matrix-over-division-algebra normal form and unique
division representative, Morita classification, or an arithmetic/cohomological classification.
It also omits universes, field and central-simple-algebra conventions, quantifier order, group-law
data, and boundary cases. Selecting one of these readings at intake would invent mathematics.

Pinned mathlib provides discovery APIs in `Mathlib.Algebra.BrauerGroup.Defs`: `CSA`,
`IsBrauerEquivalent`, `Brauer.CSA_Setoid`, and the quotient type `BrauerGroup`. That module
explicitly leaves the tensor-product abelian group law, functoriality, and the Morita
characterization as TODOs. The intake probe authenticates the definitions and equivalence-relation
lemmas at the pinned revision; it does not identify the quotient definition with the catalogue
root or claim proof credit.

The separate target `THM-M-0424` and its legacy file
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_078.lean` are useful discovery evidence, but they
have separate ownership and receipts. Neither their selected statement nor their checked partial
wrappers transfer to this target. Likewise, the Artin-Wedderburn target `THM-M-0036` cannot be
substituted for a Brauer-group claim.

The provisional root vector is `[H1, M3, R4]`. Historical and modern source leads exist but no
pinpoint primary statement is accepted; pinned formal infrastructure exists but the canonical
target and transports are open; and no source-faithful readable proof reconstruction exists.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` freeze the candidate family and non-substitution boundary.
`task-dag.json` keeps all six downstream phases open. Exact commands and results are recorded in
`validation.md`. No H0, M0, R0, accepted proof state, audit completion, theorem completion, or
master acceptance is claimed.
