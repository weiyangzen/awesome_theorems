# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1612-1617` supplies exactly the title `留数定理`, Augustin
Cauchy, 1831, the gloss `围道积分与留数的关系`, high importance, and status `已验证`. Git blame
attributes all six uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.
The record contains no bibliography, formula, definition, quantifier, hypothesis, proof boundary,
correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:6194-6219` repeats the gloss while explicitly leaving the target formal
system, logical foundation, precise definitions and premises, proof route, dependencies, equivalent
forms, axioms, machine status, and artifact links unresolved. Its generic claim that a closed result
is known and its leaf-budget planning text are not source or kernel evidence. Rev-5.6 therefore
preserves `已验证` only as `source_status_untrusted` and starts this target at
`L0 / rework_required`.

## Human-source boundary

The catalog identifies a classical, historically proved theorem family, so this intake assigns
provisional `H1`, not `H0`. No primary or authoritative edition has been admitted. In particular,
the catalog's Cauchy/1831 metadata does not itself provide an exact proposition or proof locator,
and this worker's network attempts did not preserve a source text. Historical attribution,
terminology, later generalized formulations, exact pages, definition chains, assumptions, proof
boundaries, translations, corrections, and errata remain for the source audit.

Before H0, accountable reviewers must preserve an immutable lawful source, identify the exact
theorem and every incorporated definition, map every binder/hypothesis/conclusion and exceptional
case, audit corrections and errata, and independently approve the mapping.

## Literal crosswalk

| Repository element | Mathematical decision required | Prospective Lean component | Intake result |
|---|---|---|---|
| `留数定理` | choose one exact classical or generalized residue theorem | one canonical `Prop`, not a theorem name | family identified; root open |
| `围道` (contour) | circle, Jordan boundary, piecewise smooth closed path, cycle, or chain; orientation and regularity | a source-selected path/cycle integral interface | contour type absent |
| `积分` | parametrized contour integral and integrability assumptions | `circleIntegral` for a specialization or another checked path integral | circle API probed; general encoding open |
| `留数` (residue) | coefficient, limit, or normalized local-integral definition | a new exact definition or checked bridge from meromorphic local data | no canonical residue API selected |
| "relation" | equality, including winding weights, pole set, sign, and `2 * pi * i` normalization | exact equality with finite sum and coercions | conclusion absent |
| Cauchy / 1831 | historical source identity | immutable edition and pinpoint locators | catalog metadata only |
| `已验证` | untrusted inventory status | inspectable human proof and kernel receipt would be required | no H or M credit |

## Pinned Lean substrate

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

| Interface | Checked role | Why it does not close the target |
|---|---|---|
| `circleIntegral` | integral around a parametrized complex circle | circle-only substrate; no pole inventory or residue sum |
| `Complex.circleIntegral_sub_center_inv_smul_eq_of_differentiable_on_annulus_off_countable` | equality of inner and outer circle integrals for an annular holomorphic integrand | useful local/annular bridge, not the global residue theorem |
| `Complex.circleIntegral_sub_center_inv_smul_of_differentiable_on_off_countable` | computes a simple Cauchy-kernel circle integral | one local coefficient formula, not a finite weighted pole sum |
| `MeromorphicAt` / `MeromorphicOn` | local and setwise meromorphicity predicates | function-class substrate only |
| `meromorphicOrderAt` | integer-or-infinity order of a meromorphic function at a point | records zero/pole order, not the coefficient of exponent `-1` |
| `meromorphicTrailingCoeffAt` | leading coefficient at the lowest Laurent order | equals the classical residue only in a source-selected simple-pole specialization, not generally |

The probe elaborates these names with the pinned toolchain. A bounded case-insensitive search for
complex-analytic residue-theorem names and integral/residue combinations found no terminal theorem
declaration. Arithmetic residue classes, local-ring residue fields, and the phrase "logarithmic
residue" were rejected as homonyms. This is bounded intake discovery, not an exhaustive external
anchor audit or proof of global absence.

## Statement gate

The next phase must select an approved exact source proposition, freeze contour/domain/function/
pole/residue conventions and every boundary case, choose minimal pinned imports, elaborate the same
claim, preserve its environment and normalized-expression fingerprints, compile each credited
alternate-form transport, and run all required mutation classes. Until then the canonical human
statement, canonical Lean target, obligation registry, proof tree, and all proof credit remain open.
