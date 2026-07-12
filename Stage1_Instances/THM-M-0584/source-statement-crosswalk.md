# Source-statement crosswalk

## Source boundary

The repository metadata comes from `Docs/researches/math_theorems.md` and says only "Donaldson
theorem" / "differential structures of four-dimensional manifolds" (1983). Its `已验证` label is
untrusted metadata, not a primary-source or machine-proof assertion. The distinct entry
`THM-M-0184` says "moduli spaces of anti-self-dual connections on four-manifolds"; that difference
is why this intake selects the intersection-form family provisionally.

## Candidate sources and component mapping

| Claim component | Human-source discovery anchor | Required Lean component | Intake status |
|---|---|---|---|
| Historical root | S. K. Donaldson, "An application of gauge theory to four-dimensional topology," *Journal of Differential Geometry* 18 (1983), 279-315, DOI `10.4310/jdg/1214437665` | no credited declaration | primary candidate identified; immutable copy, exact theorem/page, assumptions, and errata not yet accepted |
| Smooth four-manifold hypotheses | Donaldson 1983, theorem statement and its surrounding conventions | concrete compact boundaryless oriented smooth 4-manifold predicate | included provisionally; binder mapping open |
| Intersection form | integral pairing obtained from the manifold orientation and degree-two topology | `H_2(X; Z)` modulo torsion, fundamental class/cup or geometric intersection construction, symmetric bilinear form | included; concrete API and convention open |
| Definiteness | positive-definite form in the oriented version; negative-definite case commonly follows by orientation reversal | definiteness predicate plus checked orientation-reversal transport | included; exact source formulation open |
| Integral diagonalization | equivalence of the intersection lattice with the standard diagonal lattice | integral lattice isometry, or an integral basis with Kronecker-delta Gram matrix | intended conclusion; exact encoding open |
| Modern checking source | S. K. Donaldson and P. B. Kronheimer, *The Geometry of Four-Manifolds*, Oxford Mathematical Monographs (1990), intersection-form applications | none | secondary detailed candidate; exact chapter/theorem/page and edition review open |

The Project Euclid DOI landing page is a discovery link, not immutable evidence:
<https://projecteuclid.org/euclid.jdg/1214437665>. A retrieval attempt on 2026-07-12 reached the
publisher's automated-request interstitial rather than the article, so no page-level quotation or
file hash is claimed from that attempt.

## Lean crosswalk boundary

No exact repo-local Lean declaration has been identified or credited during intake. The historical
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_131.lean` module develops abstract data and ledgers
for the ASD-moduli-space target `THM-M-0184`; it explicitly lacks a terminal Donaldson proof and is
not a statement match for this diagonalization target. The later anchor-audit phase must search the
pinned dependency closure without treating nearby real quadratic-form diagonalization as integral
four-manifold diagonalization.

Before `H0`, an independent reviewer must verify the immutable primary-source edition, exact
theorem/page, every domain restriction and convention, any errata, and the row-by-row source-to-Lean
mapping. Before any `M0-*` state, the exact elaborated target and its proof closure require separate
kernel evidence.

