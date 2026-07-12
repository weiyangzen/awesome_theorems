# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `多项式层次`, attributes it to Larry
Stockmeyer, gives the year 1976, and states only `复杂性类的层次结构` ("hierarchical structure of
complexity classes"). Stage0 repeats this metadata and marks the exact definitions, assumptions,
proof route, dependencies, axioms, and machine artifact as open. The rev-5.6 manifest preserves
`已验证` only as `source_status_untrusted`.

No definition, proposition, hypotheses, conclusion, theorem number, page, proof source, errata
record, or formal artifact is supplied. Thus the inventory does not support an H0 crosswalk.

## Candidate source work

Larry J. Stockmeyer's 1976 paper titled *The polynomial-time hierarchy* is a plausible primary
source locator suggested by the repository attribution and date. It is not admitted here as a
pinpoint theorem source: the edition/pagination, exact result, assumptions, proof boundary, and
errata have not been independently inspected. The source audit must perform that inspection and
select the passage matching the intended claim rather than inferring it from title metadata.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "complexity classes" | languages decided under resource bounds | `Computability.Language` plus a frozen machine/cost semantics | language carrier probed; resource semantics absent |
| "polynomial" | a polynomial time bound under a size and cost model | polynomial bounds, input length, and running-time predicate | absent from located API |
| "hierarchy" | alternating/oracle levels and their union | indexed language classes and complement/oracle/alternation operators | candidate meaning only |
| "structure" | characterization, containment, collapse, completeness, or strictness | one concrete proposition with all hypotheses | absent from source record |
| Larry Stockmeyer / 1976 | historical locator | immutable pinpoint citation and source-node mapping | candidate locator; not accepted evidence |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.Computability.Language` and checks `Language` and basic membership. A scoped
case-insensitive search of mathlib Lean sources found no `polynomial hierarchy`,
`PolynomialHierarchy`, or `ComplexityClass` declaration. This is only an intake observation, not
the later immutable anchor audit and not evidence that no external formalization exists.
