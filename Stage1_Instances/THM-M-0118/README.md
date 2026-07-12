# THM-M-0118 rev-5.6 intake

This is the new rev-5.6 `planned` dossier for the Nakano vanishing theorem. The
Stage0 phrase "vanishing conditions for vector-bundle cohomology" does not
distinguish the original Nakano-positive vector-bundle theorem from its line-bundle
specializations, so this intake preserves the stronger named interpretation and
records the ambiguity rather than silently substituting Kodaira vanishing.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | On a compact Kahler manifold `X` of complex dimension `n`, a Nakano-positive holomorphic vector bundle `E` has `H^q(X, Omega^p_X tensor E) = 0` when `p + q > n` | Primary-source wording and Lean elaboration remain open |
| Geometric objects | compact Kahler manifold, holomorphic vector bundle, Nakano curvature positivity | No native Lean APIs are asserted at intake |
| Cohomology | sheaf/Dolbeault cohomology of holomorphic `p`-forms with coefficients in `E` | Choice of equivalent cohomology model requires checked transport |
| Boundary | strict range `p + q > n`; no claim for equality or for merely semipositive bundles | Boundary mutations belong to the statement phase |
| Specializations | positive line bundle; Kodaira-Akizuki-Nakano and Kodaira vanishing consequences | Candidates only, with no proof credit |
| Foundations | Lean 4 kernel with a versioned classical/choice/quotient policy | Exact TCB and dependency fingerprint remain open |

## Statement phase

The exact selected vector-bundle target is now elaborated as
`Stage1Instances.THMM0118.NakanoVanishingTarget` in `Statement.lean`, using only
`Mathlib.Algebra.Group.Defs`. Because the pinned library lacks native analytic
Kahler/Nakano/Dolbeault interfaces, a typed input package states those standard
notions without assuming the vanishing conclusion. `statement.json` records the
expression and environment fingerprints; `statement-validation.md` records the
kernel command and four distinguished structural mutations.

This is provisional statement evidence pending master acceptance, not proof or
theorem-completion evidence.

## Obligation-tree phase

The dependent architecture is frozen in `obligation-registry.json` and seven
separate graph families in `typed-graphs.json`. It contains 14 canonical
obligations and isolates `M0118-T-COHOMOLOGY` as the remaining root cut. The
local `ObligationTree.lean` checks only transparent conditional composition;
it does not provide the missing analytic package. See `obligation-tree.md` and
`obligation-validation.md` for the exact provisional boundary.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The source
description is too coarse for `H0`, and no exact Lean declaration is known. The
first failed theorem gate is therefore source/statement disambiguation. This
intake creates scope and an open task boundary only; it does not claim a Lean
proof, machine-checked upstream closure, or theorem completion.

Validation commands and their exact outcomes are recorded in `validation.md`.
