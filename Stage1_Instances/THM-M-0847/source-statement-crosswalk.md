# THM-M-0847 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6215-6220` supplies exactly the title `图on理论`, attribution
László Lovász, year 2012, gloss `大图的极限理论`, importance `高`, and status `已验证`. All six
uncited lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no graphon definition, ordered binder,
hypothesis, conclusion, theorem/page locator, proof, correction record, reviewer, or formal
artifact.

`Docs/Stage0_Blueprint.md:23117-23142` repeats that metadata while explicitly leaving the formal
system, precise definitions and premises, proof route, dependencies, equivalent forms, axioms,
machine status, and artifact links open. Its generic closed-result and leaf-audit text is planning
metadata, not evidence. Rev-5.6 retains `已验证` only as untrusted metadata and starts this target at
`L0 / rework_required`.

## Literal crosswalk

| Repository component | Required mathematical component | Prospective Lean component | Intake result |
|---|---|---|---|
| graphon theory | one exact proposition within a large theory | a canonical `Prop`, not only a graphon definition | subject label only |
| large graphs | finite-graph class, size regime, density convention, and test objects | `SimpleGraph` plus explicit finiteness and asymptotic binders | all choices open |
| limit theory | convergence notion, limit object, existence/uniqueness direction, and topology | sequence, density functionals, graphon encoding, metric/quotient, exact conclusion | no direction or theorem selected |
| László Lovász, 2012 | source provenance and pinpoint result | immutable edition/chapter/page and source-to-binder map | matching monograph lead only |
| verified | catalog screening field | accepted source and kernel receipts | explicitly rejected as evidence |

The literal record cannot populate a canonical domain, ordered quantifiers, hypotheses, conclusion,
alternate encodings, excluded cases, or Lean expression fingerprint.

## Bibliographic source lead

Crossref metadata identifies László Lovász, *Large Networks and Graph Limits*, American
Mathematical Society Colloquium Publications 60, published 12 December 2012, DOI
`10.1090/coll/060`, with ISBNs `9780821890851`, `9780821894453`, and `9781470415839`. This is a
strong match for the catalog author, year, and gloss.

The same registry lists distinct chapters "Kernels and graphons" (pages 115-125, DOI
`10.1090/coll/060/07`), "The cut distance" (DOI `10.1090/coll/060/08`), "Convergence of dense
graph sequences" (pages 173-199, DOI `10.1090/coll/060/11`), "The space of graphons" (pages
239-261, DOI `10.1090/coll/060/14`), and "Algorithms for large graphs and graphons" (DOI
`10.1090/coll/060/15`). This breadth confirms ambiguity rather than selecting a root.

Only mutable bibliographic metadata was inspected; the repository does not cite the book and its
full text was not admitted. No exact numbered theorem, incorporated definitions, premise/conclusion
map, proof boundary, correction history, errata, or independent review is credited. The lead
therefore supplies neither a canonical statement nor H0 evidence.

## Confusable 2006 result

Lovász and Szegedy's *Limits of dense graph sequences*, *Journal of Combinatorial Theory, Series
B* 96 (2006), pages 933-957, DOI `10.1016/j.jctb.2006.05.002`, is an inspected primary-source
lead for the neighboring graph-limit family. ArXiv revision `math/0408173v2` states, among other
results, that convergent dense graph sequences admit symmetric measurable `[0,1]^2 -> [0,1]`
limit objects and conversely such functions arise as limits.

That paper matches `THM-M-0846`'s Lovász/Szegedy 2006 metadata more directly than this target's
Lovász 2012 metadata. It is recorded to prevent a silent substitution. No proposition from it is
assigned to `THM-M-0847`, and no source or proof credit is transferred across targets.

## Pinned Lean crosswalk

| Declaration | What it supplies | Why it is not the target |
|---|---|---|
| `SimpleGraph.edgeDensity` | rational edge density between two finite vertex sets | no graphon, homomorphism density, sequence, or limit |
| `Rel.edgeDensity` | density for a decidable binary relation on finite sets | finite relational substrate only |
| `unitInterval.volume_def` | canonical measure on the unit interval | no symmetric kernel or theorem |
| `unitInterval.measurePreserving_symm` | one measure-preserving involution of the unit interval | no general relabeling quotient or cut distance |
| `MeasureTheory.Measure.prod` | product-measure construction | no graphon measurability, density integral, or convergence result |
| `MeasureTheory.MeasurePreserving` | a bundled measure-preserving-map predicate | no weak-isomorphism or uniqueness theorem |

`IntakeProbe.lean` checks these APIs at the pinned revision. A bounded case-insensitive search over
repo-local Lean and all pinned packages found no graphon, graph-limit, cut-norm, cut-distance, or
homomorphism-density implementation. Matches for `Set.graphOn` are the ordinary graph of a
function on a set and are unrelated. The probe and search are discovery evidence only, not a
canonical target, exhaustive anchor audit, absence proof, or proof body.

## Source gate

Accountable reviewers must select one immutable source proposition and map its graphon and finite-
graph definitions, base probability space, equality or quotient, density and convergence
conventions, ordered binders, hypotheses, conclusion, boundary cases, proof passage, and
corrections. They must also reconcile ownership with `THM-M-0845` and `THM-M-0846`. A formal
reviewer must then map that same claim to a minimal-import Lean expression and checked transports.

Until that happens, `H5` records that the catalog subject wording is not a stable truth-valued
proposition, `M4` records the lack of a source-identical usable formal artifact, and `R4` records
the lack of an anchorable proof reconstruction. These classifications do not say that established
graphon theorems are false or open.
