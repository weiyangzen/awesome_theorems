# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Grothendieck category represented through modules and a quotient | P. Gabriel, *Des categories abeliennes*, Bulletin de la Societe Mathematique de France 90 (1962), 323-448 | no accepted exact declaration yet | Primary historical source located; theorem/page, assumptions, translation, and errata pinpoint remain open |
| Popescu representation/generalization | N. Popescu, *Abelian Categories with Applications to Rings and Modules*, Academic Press (1973) | intended root dossier claim | Book-level primary exposition located; exact theorem/page and edition audit remain open |
| `Hom(G,-)` is full and faithful | same classical theorem family | `IsGrothendieckAbelian.GabrielPopescu.full` plus `isSeparator_iff_faithful_preadditiveCoyonedaObj` | Exact pinned anchors compose locally into the frozen target; proof acceptance remains a later phase |
| left adjoint exists and is exact | same theorem family | `tensorObjPreadditiveCoyonedaObjAdjunction` and `GabrielPopescu.preservesFiniteLimits` | Exact pinned anchors compose locally into the frozen finite-limit formulation; no broader quotient claim is inferred |
| Serre quotient equivalence | classical quotient formulation | historical `gabrielPopescuLeftAdjoint_isSerreLocalization_of_exact` is conditional on finite colimits | Material scope gap: a conditional bridge is not the root theorem |

The source title, repository gloss ("characterization of Grothendieck categories"),
and historical Lean `StatementShape` are not yet proven coextensive. In particular,
the embedding/adjunction data must not be broadened into, or substituted for, the
Serre-quotient equivalence without checked transports.

No `H0` claim is made. The anchor audit in `anchor-audit.json` concerns formal
candidates, not primary mathematical-source acceptance. Later source audit must record immutable scans or editions,
pinpoint theorem/page ranges, every hypothesis and convention, corrections/errata,
and independent review.
