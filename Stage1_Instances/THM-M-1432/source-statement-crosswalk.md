# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10460-10465` supplies exactly the title `Yoccoz定理`, attribution
to Jean-Christophe Yoccoz, year 1988, gloss `Siegel盘的线性化`, importance "high", and status
`已验证`. All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no citation, definition,
formula, theorem statement, assumptions, conclusion, or proof.

`Docs/Stage0_Blueprint.md:38942-38967` repeats the gloss while explicitly leaving the formal system,
logical foundation, exact definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine status, and artifact links open. Its generic planning claim that a closed result is
known is not primary-source evidence. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

There is a second repository record at `Docs/researches/math_theorems.md:1871-1876`, projected as
the distinct target `THM-M-0260`, with the Chinese title `约科兹定理` but the same attribution,
year, and gloss. It does not explain whether the records are intended to denote the same precise
claim or different variants. Rev-5.6 assigns them separate IDs, so intake records the collision but
does not merge scope or evidence.

## Primary-source discovery lead

The publisher, Societe Mathematique de France, identifies Jean-Christophe Yoccoz,
*Petits diviseurs en dimension 1*, Asterisque 231 (1995), 242 pages, ISSN `0303-1179`, DOI
`10.24033/ast.306`. The publisher's abstract says that the first article studies one-variable
holomorphic diffeomorphism germs near a fixed point. It distinguishes an earlier sufficiency result
under the Bruno arithmetic condition from Yoccoz's converse: when the Bruno condition fails, the
corresponding quadratic polynomial is not linearizable.

This is strong source-selection and ambiguity evidence, but not H0 evidence for this catalog item.
The catalog gives the year 1988 rather than the monograph's 1995 publication year and cites no
article, theorem, section, or page. The full primary statement, incorporated definitions, premise
and proof boundaries, corrections or errata, immutable inspected-copy hash, catalog identity, and
independent source review have not been frozen. The lead therefore does not choose between the
sufficiency, converse, quadratic biconditional, or Siegel-disk formulations.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `Yoccoz定理` | one named result from Yoccoz's small-divisor work | one exact canonical `Prop` | theorem name is ambiguous |
| `Siegel盘` | maximal invariant domain analytically conjugate to an irrational rotation, or shorthand for local linearization | complex domain/germ, fixed point, rotation, conjugacy, maximality predicates | object and convention not defined |
| `线性化` | local analytic conjugacy to the multiplier map | analytic/biholomorphic conjugator, neighborhood, functional equation, normalization | direction, regularity, and locality open |
| Yoccoz / 1988 | historical attribution and date | documentation and immutable source identity | no edition, theorem/page, or proof locator |
| `已验证` | untrusted inventory metadata | reviewed human-source packet or kernel receipt | no H or M credit |

## Candidate-source variant crosswalk

| Candidate variant | Material binders and hypotheses | Material conclusion | Why it is not canonical at intake |
|---|---|---|---|
| Brjuno sufficiency for germs | irrational rotation number satisfying a chosen Brjuno predicate; holomorphic germ with that multiplier | existence of a local analytic conjugacy to the linear rotation | publisher abstract attributes the sufficiency lineage to Siegel/Bruno; catalog does not give an exact formulation |
| Yoccoz quadratic converse | rotation number failing the chosen Brjuno predicate; corresponding normalized quadratic polynomial | no local analytic linearization | a converse/counterexample-family result, not interchangeable with universal sufficiency |
| Quadratic iff | normalized quadratic family and exact arithmetic convention | linearizable or has a Siegel disk iff the number is Brjuno | combines directions and definition bridges not stated by the catalog |
| Siegel-disk geometry | an already existing disk plus extra arithmetic or dynamical hypotheses | a boundary, critical-point, size, or regularity property | changes the conclusion from existence/linearization to geometry |

## Source gate

Before the target can leave `H5`, an accountable reviewer must justify the catalog-to-source
identity, preserve and hash an immutable primary source, select one exact truth-valued theorem,
record edition and theorem/section/page, transcribe every incorporated definition, ordered binder,
hypothesis and conclusion, map proof dependencies and corrections or errata, reconcile the 1988
catalog date and the duplicate `THM-M-0260` record, and obtain independent source review. The
corrected proposition's H status must then be classified afresh.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks `Complex.UnitDisc`, its complex coercion, `AnalyticAt`, analytic composition, and
`Function.Semiconj`. These are generic substrate for one possible encoding. They provide no
holomorphic-germ quotient, Brjuno predicate, Siegel-disk definition, quadratic-family theorem, or
Yoccoz conclusion.

A bounded exact-topic search found no target-specific declaration. The canonical module,
declaration/expression, elaborated-expression hash, checked transports, and statement mutations
remain null. The probe and search are intake feasibility evidence only, not H0, M0, readable-proof
closure, audit completion, or theorem completion.
