# Source-statement crosswalk

| Claim surface | Source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Repository entry | `Docs/researches/math_theorems.md`, "flat descent theorem", attributed to Grothendieck in the 1960s; statement: "descent theory under flat base change" | none exact | Secondary, non-pinpoint wording; insufficient to determine a proposition |
| Classical module descent | A. Grothendieck et al., *SGA 1*, Expose VIII, *Descente fidelement plate* | `Mathlib.Algebra.Category.ModuleCat.Descent`; legacy `S1_M_104.ModuleCategoryDescentShape` | Strong candidate genealogy, but edition/theorem/page, assumptions, errata, and exact equivalence still require audit |
| Scheme/sheaf descent | *SGA 1*, Expose VIII and later fpqc descent formulations | mathlib descent/stack and flat-descent modules | Potentially broader object class; cannot be merged into the module claim without source authority |
| Existing repo wrapper | No primary source crosswalk recorded | `AwesomeTheorems.Stage1.S1_M_104.StatementShape` in `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_104.lean` | Discovery only: packages module extension-of-scalars properties and explicitly disclaims the terminal broad theorem |
| Projectivity branch | External Lean project mentioned by the legacy artifact | `proj_faithfully_flat` | Nonterminal branch and anchor-only; statement and integration audits are later phases |

The phrase "flat descent" is not itself a unique theorem. Faithful flatness is generally essential
for the standard effective module-descent theorem, while fpqc descent of sheaves and descent of
morphism properties have different binders and conclusions. Consequently this intake does not
turn the broad phrase into a conjunction of all known branches or narrow it to the existing wrapper.

The statement phase must first select a pinpoint primary theorem and record its edition, theorem or
proposition number, pages, hypotheses, and errata. It must then freeze ordered binders and universes,
elaborate the exact Lean target, and mutation-test faithful-flatness, object category, effectiveness,
and base-change direction. Until then the source grade remains `H2` and machine grade `M4`.

Discovery links (not immutable evidence receipts):

- SGA 1 bibliographic record: <https://doi.org/10.1007/978-3-540-22407-0>
- Stacks Project, Descent chapter: <https://stacks.math.columbia.edu/tag/0238>

No `H0`, exact-statement, anchor-audit, or proof claim is made.

## Exact premise and boundary mapping

No exact premise mapping is currently possible. The source record fixes only a flat base-change
theme. It does not fix the objects, base category, topology or cover, faithful-flatness, direction of
base change, descent datum, effectiveness condition, or conclusion. Therefore every corresponding
Lean binder and proposition field remains null in `statement.json` rather than being guessed.

The pinned `Mathlib.Algebra.Category.ModuleCat.Descent` probe establishes only that the current
environment exposes extension of scalars, flat preservation of finite limits, faithfully flat
reflection of isomorphisms, and comonadicity. Those are competing module-descent ingredients, not a
source-admitted statement crosswalk. The legacy conjunction receives no statement or proof credit.

Required resolution: an immutable primary edition plus pinpoint theorem/proposition and pages must
select one branch and supply all incorporated definitions, hypotheses, conclusion, translation,
correction and errata disposition. Until then the unresolved source-fidelity debt remains visible at
`H2`, and the positive statement gate cannot close.
