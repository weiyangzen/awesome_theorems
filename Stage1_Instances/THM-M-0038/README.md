# THM-M-0038 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalogue item `莫林定理`.
The repository gives only the gloss `关于中心单代数的指数与次数` ("about the index and degree of
central simple algebras"), attributes it to `Sigmund Morill` in 1937, and labels it `已验证`.
Under rev-5.6 those fields are untrusted metadata, not an exact source statement, Lean target, or
proof receipt.

The supplied wording names a subject rather than a proposition. It does not say whether the
intended result is that an index divides a degree, that they have the same prime divisors, that an
index is invariant under a Brauer-equivalent representative, an index-exponent relation, or a
field-specific bound. It also does not define either invariant. Selecting any familiar statement
at intake would silently substitute mathematics.

The author string is also unresolved. The repository contains no citation, theorem locator, or
supporting occurrence of `Sigmund Morill`, and bounded bibliographic searches performed for this
intake did not identify a matching algebraist or paper. This negative search is a blocker and a
retry guide, not evidence that no such source exists.

Pinned mathlib provides nearby central-simple-algebra infrastructure in
`Mathlib.Algebra.BrauerGroup.Defs`: `CSA`, `IsBrauerEquivalent`, `Brauer.CSA_Setoid`, and
`BrauerGroup`. The intake probe authenticates these APIs at the pinned revision and checks that no
declaration named `index`, `degree`, or `exponent` occurs in the bounded `Algebra/BrauerGroup` and
`Algebra/Central` source surfaces. It does not define the missing invariants or prove the catalogue
claim.

The provisional root vector is `[H5, M3, R4]`. `H5` classifies the received record as not yet a
stable proposition because its source identity and asserted relation are unresolved; it does not
refute any standard theorem about central simple algebras. `M3` records only adjacent checked
definitions, while the canonical target remains null. `R4` records that no source-faithful proof
route can attach to an unidentified root.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` freeze the ambiguity and non-substitution boundary. `task-dag.json`
keeps all six downstream phases open. `validation.md` records exact commands and results. No H0,
M0, R0, accepted proof state, audit completion, theorem completion, or master acceptance is
claimed.
