# Source-statement crosswalk

## Candidate primary sources

- Haim Brezis, *Functional Analysis, Sobolev Spaces and Partial Differential Equations*, Springer
  (2011), Chapter 3 (weak topologies), especially the results relating convex strong closure to
  weak closure and convex lower semicontinuity. Exact proposition/corollary and page must be
  checked against a stable edition.
- Ivar Ekeland and Roger Temam, *Convex Analysis and Variational Problems*, North-Holland (1976),
  the lower-semicontinuity and weak-topology results in the convex-analysis chapters. Exact
  theorem/page, edition conventions, and errata have not yet been inspected.

These are discovery anchors, not `H0` evidence. The statement phase must inspect one stable edition
and record verbatim hypotheses, definitions, theorem/page, and errata.

## Crosswalk

| Repository phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "convex functional" | convexity of `F` on a real vector space | concrete `ConvexOn`/functional encoding | included; encoding open |
| "weak" | topology induced by continuous linear functionals | concrete weak topology on `E` | included; API open |
| "lower semicontinuity" | closed sublevels or equivalent liminf condition | topological lower-semicontinuity predicate | included; exact predicate open |
| norm-to-weak implication | convex norm-closed sublevels are weakly closed | separation/closed-convex bridge | intended substantive bridge |
| converse | finer norm topology preserves weak-lsc toward norm-lsc | topology comparison transport | included |

## Fidelity boundary

Stage0 supplies only the Chinese name and gloss `凸泛函的弱下半连续性`; it does not specify a
source, space, codomain, topology convention, or assumptions. Consequently the dossier freezes the
standard theorem family but does not claim an exact source statement. Before `H0`, an independent
reviewer must verify the selected edition, theorem/page, all assumptions, definitions, and errata.
Before statement acceptance, Lean elaboration must also distinguish topological from sequential
lower semicontinuity and mutation-test convexity and the topology direction.
