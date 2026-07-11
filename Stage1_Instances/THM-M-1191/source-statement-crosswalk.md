# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` supplies only the title "heat kernel estimates", attribution to
multiple mathematicians, twentieth century, the statement "upper and lower bounds for the heat
kernel", importance "high", and the untrusted status `已验证`. `Docs/Stage0_Blueprint.md` repeats
that record while leaving definitions, assumptions, proof history, dependencies, axioms, and
machine artifacts open. No author, bibliography, edition, theorem/page, or errata record is given.

Accordingly, no primary-source candidate or exact theorem is asserted here. The phrase names a
large theorem family rather than a unique proposition, so choosing a standard result from memory
would broaden or substitute the source.

## Crosswalk

| Source element | Mathematical information fixed | Information still required for Lean | Intake result |
|---|---|---|---|
| "heat kernel" | a kernel for some heat evolution | space, operator, measure, kernel definition, normalization | unresolved |
| "upper bound" | one quantitative inequality | expression, quantifiers, constants, time range, hypotheses | unresolved |
| "lower bound" | a second quantitative inequality | positivity regime, expression, constants, exclusions | unresolved |
| twentieth century / multiple mathematicians | broad historical family | no unique declaration follows | insufficient to identify a theorem |
| `已验证` | untrusted inventory label | inspectable source proof and kernel receipt | no credit |

## Statement boundary

There is no repository-local legacy artifact for this target and no canonical Lean expression at
intake. In particular, a possible expression involving an explicit function on `Real × EuclideanSpace`
would commit to the Euclidean case, while a manifold or uniformly elliptic formulation would require
substantially different domains and hypotheses. None is authorized by the available source record.

The first downstream gate is primary-source identification. Before `H0`, an independent reviewer
must verify the edition, theorem/page, definitions, complete assumption list, proof and errata, then
approve a row-by-row mapping to the canonical Lean binders and conclusion. Before machine credit,
that exact expression must elaborate under pinned minimal imports and pass the remaining rev-5.6
gates.
