# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` records only the title "Krylov estimate", attribution to Nikolai
Krylov, year 1980, and statement "moment estimate for diffusion processes". The generated Stage0
entry repeats this wording and leaves definitions, hypotheses, proof route, exact source, and
machine status open. No book or paper edition, theorem number, page, or errata is attached.

No primary-source candidate is asserted at intake: Krylov's publications contain multiple estimates
for controlled and uncontrolled diffusion processes, and the supplied wording cannot distinguish
them. The `已验证` label is untrusted screening metadata, not `H0` or kernel evidence.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "Krylov estimate" | a result in a Krylov theorem family | exact proposition/declaration | unresolved |
| "diffusion process" | stochastic-process subject | probability space, filtration, coefficients, solution law | unresolved |
| "moment estimate" | some expected power/integral is bounded | integrand, exponent, norm, measure and inequality | unresolved |
| Nikolai Krylov / 1980 | attribution and approximate date | immutable bibliographic anchor | insufficient to identify theorem |
| `已验证` | repository status label | inspectable proof or kernel receipt | no credit |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_243.lean` defines an expected occupation integral
and proposes a bound by a product-measure `eLpNorm`. It also packages a martingale-problem boundary,
bounded coefficient envelope, ellipticity witnesses, and a constant. This is a plausible candidate
formalization, not a source crosswalk. It neither cites the exact human theorem nor proves the
terminal `StatementShape`; its checked projection lemmas do not close the estimate.

The statement phase must first identify and inspect a stable primary source. Before `H0`, an
independent reviewer must verify edition, theorem/page, definitions, every hypothesis, exponent and
constant dependency, boundary cases, and errata, then approve a row-by-row source-to-Lean mapping.
