# Source-statement crosswalk

## Available repository record

The repository research inventory names Seifert and van Kampen, gives the year 1931, and describes
the result only as "the fundamental group of a union." Stage0 repeats that metadata without a
publication, theorem number, page, hypotheses, proof reference, or formal declaration. Its
`verified` label is explicitly untrusted under rev-5.6 and provides neither `H0` nor machine credit.

## Source candidates

- Egbert van Kampen's 1931 paper on the connection between fundamental groups of related spaces is
  the historical primary-source search anchor. The exact title, journal issue, pages, language,
  formulation, and relation to the modern two-open-set statement have not yet been inspected and
  are not asserted here.
- Herbert Seifert's early work is a second historical attribution lead. The repository metadata is
  insufficient to identify a particular publication or to decide which version its joint naming
  intends.
- Allen Hatcher, *Algebraic Topology* (2002), section 1.2, is a stable modern exposition candidate
  for the standard free-product/normal-closure formulation. It is secondary evidence and an exact
  proposition/page and errata check remain open.

These are discovery anchors only. The statement phase must use inspected stable copies and must not
manufacture bibliographic detail from the theorem's conventional name.

## Crosswalk

| Repository/source phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "space union" | `X = U union V` for two open subspaces | sets/subtypes or open embeddings plus a cover equality | included; encoding open |
| common basepoint | `x0` belongs to both cover members | based spaces and inclusion maps preserving `x0` | included |
| connected cover pieces | `U`, `V`, and their intersection are path-connected | explicit path-connected hypotheses | included; exact source conventions open |
| fundamental groups | based loop-homotopy groups of intersection, pieces, and union | concrete mathlib fundamental-group objects | included; API audit open |
| inclusion diagram | the two intersection maps agree after mapping into `X` | functorial induced group homomorphisms and commutative square | included |
| van Kampen conclusion | `pi_1(X,x0)` satisfies the group pushout universal property | concrete categorical pushout or an equivalent universal-property predicate | canonical human conclusion |
| free-product presentation | quotient by the normal closure of `i_U(g) i_V(g)^{-1}` relations | free product, normal closure, quotient, and checked equivalence to pushout | alternate encoding only |

## Fidelity gates

Before `H0`, an independent reviewer must verify the chosen primary or authoritative edition,
theorem/page, definitions, all hypotheses, conclusion, proof boundary, historical attribution, and
errata. Before statement credit, every source component must map row by row to an elaborated Lean
expression, and any modern reformulation must have a checked implication or equivalence witness.
The later anchor audit must separately inventory repo-local, pinned-mathlib, and credible external
Lean 4 candidates with immutable revisions and terminal proof provenance.
