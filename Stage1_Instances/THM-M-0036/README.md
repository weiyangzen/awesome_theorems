# THM-M-0036 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Artin-Wedderburn theorem. The
repository catalogue gives only the Chinese gloss `中心单代数的分类` ("classification of central
simple algebras"), attributes it to Emil Artin and Joseph Wedderburn, dates it to 1927, and labels
it `已验证`. Under rev-5.6 that label is untrusted metadata, not an exact statement, source audit,
or proof receipt.

The gloss identifies a classical theorem family, but it does not choose finite-dimensional central
simple algebras versus simple Artinian algebras, ring versus algebra equivalence, an existence
normal form versus existence plus uniqueness, or whether the division-algebra representative must
be explicitly central over the base field. It also leaves the base field, universe placement,
matrix-size data, and boundary conventions unstated. Selecting a familiar formulation at intake
would invent mathematics not present in the received record.

Pinned mathlib contains strong candidates in
`Mathlib.RingTheory.SimpleModule.WedderburnArtin`, notably
`IsSimpleRing.exists_algEquiv_matrix_divisionRing_finite`. A foreign legacy wrapper specializes it
to mathlib's `CSA K`, whose carrier is finite-dimensional, central, and simple. The intake probe
authenticates the pinned definitions and theorem declarations and reports their current axioms. It
does not identify the candidate with the underspecified catalogue gloss or claim proof credit.

The target is kept separate from `THM-M-0027`, the general semisimple-ring Wedderburn-Artin
structure theorem, and from the Brauer stable-classification targets `THM-M-0037` and
`THM-M-0424`. Neither a product decomposition nor equality modulo matrix stabilization may be
substituted for this target without an accepted source decision.

The provisional root vector is `[H1, M3, R4]`: the theorem family and a historical source lead are
known, pinned formal statement/proof candidates exist, but no exact source proposition, checked
source-to-Lean transport, or readable proof reconstruction is accepted.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` freeze the admissible family and non-substitution boundary.
`task-dag.json` keeps all six downstream phases open. Exact commands and results are in
`validation.md`. No H0, M0, R0, accepted execution state, audit completion, theorem completion, or
master acceptance is claimed.
