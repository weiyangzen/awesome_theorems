# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Grothendieck category represented through modules and a quotient | P. Gabriel, *Des categories abeliennes*, Bulletin de la Societe Mathematique de France 90 (1962), 323-448 | no accepted exact declaration yet | Primary historical source located; theorem/page, assumptions, translation, and errata pinpoint remain open |
| Popescu representation/generalization | N. Popescu, *Abelian Categories with Applications to Rings and Modules*, Academic Press (1973) | intended root dossier claim | Book-level primary exposition located; exact theorem/page and edition audit remain open |
| `Hom(G,-)` is full and faithful | same classical theorem family | `IsGrothendieckAbelian.GabrielPopescu.full` plus `isSeparator_iff_faithful_preadditiveCoyonedaObj` in the historical wrapper | Candidate upstream anchors only; no rev-5.6 environment or type evidence yet |
| left adjoint exists and is exact | same theorem family | `tensorObjPreadditiveCoyonedaObjAdjunction` and `GabrielPopescu.preservesFiniteLimits` | Candidate encoding; statement phase must check whether the hypotheses make finite-limit preservation the required exactness notion |
| Serre quotient equivalence | classical quotient formulation | historical `gabrielPopescuLeftAdjoint_isSerreLocalization_of_exact` is conditional on finite colimits | Material scope gap: a conditional bridge is not the root theorem |

The source title, repository gloss ("characterization of Grothendieck categories"),
and historical Lean `StatementShape` are not yet proven coextensive. In particular,
the embedding/adjunction data must not be broadened into, or substituted for, the
Serre-quotient equivalence without checked transports.

No `H0` claim is made. Later source audit must record immutable scans or editions,
pinpoint theorem/page ranges, every hypothesis and convention, corrections/errata,
and independent review.
