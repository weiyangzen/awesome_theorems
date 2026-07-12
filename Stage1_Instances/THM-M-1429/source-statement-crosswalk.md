# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10439-10444` supplies exactly the title `Fatou集`, the
attribution Pierre Fatou, the year 1917, the gloss `复动力学的稳定集`, importance "high," and status
`已验证`. All six lines were introduced by repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, stable source
ID, formula, definition, theorem statement, or proof.

`Docs/Stage0_Blueprint.md:38861-38886` repeats these fields and explicitly leaves the exact
definitions and premises, proof process, dependencies, equivalent forms, axioms, machine status,
and artifact links open. Its generic closed-result and leaf-audit wording is generated planning
metadata, not source evidence. The rev-5.6 manifest carries `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

## Crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `Fatou集` | a set relative to a selected complex dynamical system | ambient type, self-map/family, membership predicate, and set definition | object and map are open; not a proposition |
| "complex dynamics" | iteration of a rational, polynomial, entire, or meromorphic map | exact domain/codomain, complex-analytic structure, map hypotheses, iterate family | all open |
| "stable" | normality, equicontinuity, local-uniform subsequential behavior, or a dynamical stability property | topology/uniformity/metric, neighborhoods, filters/subsequences, limit class | meaning open |
| Pierre Fatou / 1917 | a historical pointer toward early iteration theory | source provenance only | no work, edition, stable ID, theorem/page, assumptions, proof, or errata |
| `已验证` | untrusted inventory metadata | inspectable source proof and kernel receipt would be required | no H or M credit |

## Definition and theorem boundary

The conventional phrase "Fatou set" still does not select a theorem. A source could define it as
the locus where iterates of a rational map form a normal family and then prove it open; define its
Julia-set complement; prove some flavor of invariance; or state a classification or basin result.
Those roots have different binders and obligations. Even definitionally, a rational-map/sphere
formulation, a polynomial/plane formulation, and a transcendental entire or meromorphic
formulation differ at infinity and at singularities. Normality can be encoded via subsequences,
compact convergence in the spherical metric, equicontinuity, or compact divergence only under
additional hypotheses and checked equivalences.

Accordingly, this intake does not turn a chosen definition into a tautological `x ∈ F ↔ ...`
theorem. It also does not borrow the Julia complement, openness, or invariance theorem as an
unstated conclusion.

## Historical discovery boundary

Crossref metadata locates Pierre Fatou's three-part *Sur les équations fonctionnelles* in the
*Bulletin de la Société Mathématique de France*: DOI `10.24033/bsmf.998` (1919), pages 161-271;
DOI `10.24033/bsmf.1003` (1920), pages 33-94; and DOI `10.24033/bsmf.1008` (1920), pages
208-314. Their Crossref resources point to Numdam identifiers whose volume segments are 47, 48,
and 48, while Crossref's own volume field reports 2, so even the metadata needs reconciliation.
This discovery context does not match the catalog's unexplained year 1917, and no inspected
catalog field selects a passage or proposition from these memoirs. Network retrieval of the
primary full text was incomplete during intake, so no page, theorem, proof, assumption, or errata
mapping is claimed.

The metadata therefore strengthens the need for source review rather than authorizing target
selection. It receives no H0/H1 credit and is not a primary-source crosswalk.

## Neighbor boundary

The adjacent repository roots separately own complex dynamics (`THM-M-1427`), Julia set
(`THM-M-1428`), Mandelbrot set (`THM-M-1430`), and named results by Douady-Hubbard, Yoccoz,
Sullivan, McMullen, Feigenbaum, Lanford, and Lyubich. Their definitions or conclusions cannot be
borrowed to make this root precise. Measure-theoretic Fatou's lemma is only a homonym.

## Source gate

Before an approved correction can leave `H5`, an accountable reviewer must identify and preserve
an immutable primary or authoritative source; select one exact truth-valued passage and
page/section; transcribe every dependent definition, ordered binder, hypothesis, conclusion,
normality/stability convention, and boundary case; reconcile the catalog's 1917 date; check
corrections and errata; and justify why that proposition represents `THM-M-1429` rather than a
neighboring target. A second reviewer must approve the source-to-canonical-statement mapping.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, bounded source-name
searches found no declaration for a Fatou set, Julia set, complex dynamics, or a normal family.
Pinned APIs do include the iteration notation and lemmas such as `Function.iterate_succ_apply`,
plus `Function.IsPeriodicPt`, `MeromorphicAt`, `MeromorphicOn`,
`TendstoLocallyUniformly`, `TendstoLocallyUniformlyOn`, and `IsOpen`; `IntakeProbe.lean` verifies
these representative names. The locally-uniform API's documented convention is not automatically
the classical normal-family criterion.

The canonical module, declaration or expression, elaborated expression hash, checked transports,
and statement mutations remain null. No H0, M0, or readable-proof closure is claimed.
