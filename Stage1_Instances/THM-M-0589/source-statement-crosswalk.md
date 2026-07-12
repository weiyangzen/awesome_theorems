# Source-statement crosswalk

## Repository record

The repository supplies only the Chinese label "surgery theory", the date "1960s", the attribution
"many mathematicians", and the gloss "classification of manifolds by surgery". Its `已验证` field
is untrusted under rev-5.6. It provides no theorem number, exact wording, manifold category,
dimension, fundamental-group assumptions, or conclusion form, so it does not identify a unique
proposition.

## Candidate primary sources

- C. T. C. Wall, *Surgery on Compact Manifolds*, Academic Press (1970), is a primary monograph
  candidate for surgery obstruction and classification results. The later second edition edited by
  A. A. Ranicki is a distinct edition and must not silently supply wording for the 1960s/1970
  record.
- William Browder, *Surgery on Simply-Connected Manifolds*, Ergebnisse der Mathematik und ihrer
  Grenzgebiete 65, Springer (1972), is a primary monograph candidate for the simply-connected
  branch, not evidence that the repository intended that restriction.
- Dennis Sullivan's 1960s work on the homotopy theory of manifolds is a genealogy lead for the
  localization and normal-invariant viewpoint, but no exact publication or theorem is selected by
  the repository record.

These entries are discovery anchors only. No stable copy was inspected theorem by theorem during
this intake. Exact edition, theorem/page, definitions, assumptions, corrections, errata, and
source-to-node review remain open; consequently none supplies `H0` evidence.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "manifolds" | category, dimension, compactness, boundary, orientation | concrete manifold and boundary structures | family identified; domains open |
| "surgery" | normal map, embedded surgery data, below/middle-dimensional moves | normal bundle/map and surgery construction interfaces | intended method identified; encoding open |
| "classification" | structure set and its equivalence relation | bundled structures modulo the selected relation | conclusion family identified; exact form open |
| normal invariant | map to the source's normal-invariant object | normal data and comparison map | candidate intermediate object; conventions open |
| surgery obstruction | obstruction in a decorated `L`-group | quadratic/symmetric form or formation and obstruction map | group, decoration, and coefficient involution open |
| exact sequence | exactness in pointed sets/groups with actions where applicable | typed maps, actions, and the source's exactness predicate | possible root form; not selected |
| "1960s / many mathematicians" | historical disambiguation | no machine-proof credit | too broad to select a theorem |

## Human and machine boundary

A repository search found no theorem-specific artifact for `THM-M-0589`. The adjacent legacy
high-dimensional Poincare file mentions surgery exact sequences only as missing proof
infrastructure and explicitly provides no surgery/transversality API. A narrow text search of the
pinned mathlib source likewise found no theorem-specific surgery-classification interface. These
are local discovery observations, not the exhaustive immutable-revision anchor audit assigned to a
later phase.

Before `H0`, an independent reviewer must select a primary edition and exact theorem, verify its
definitions and errata, and approve every row of a source-to-formal mapping. Before statement
credit, that reviewed claim must be elaborated without changing category, dimension, fundamental
group, decoration, boundary convention, equivalence relation, or exactness strength.
