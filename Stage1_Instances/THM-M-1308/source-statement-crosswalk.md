# Source-statement crosswalk

## Primary source anchor

Demetrios Christodoulou and Sergiu Klainerman, *The Global Nonlinear Stability of the Minkowski
Space*, Princeton Mathematical Series 41, Princeton University Press, 1993, is the identified
primary monograph. Its exact theorem/page, edition-specific wording, definitions, assumptions, and
errata have not yet been inspected and independently reviewed. It is therefore a discovery anchor,
not `H0` evidence.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| Christodoulou-Klainerman theorem | nonlinear stability of Minkowski space | one exact root theorem, not a name-only proposition | identity frozen; exact source anchor open |
| vacuum initial data | Riemannian metric and second fundamental form satisfying constraints | initial-data structure plus Hamiltonian/momentum constraints | included; encoding open |
| sufficiently small | weighted high-order closeness to Minkowski data | explicit norm and quantified threshold | included; formula open |
| maximal development | solution of `Ric(g)=0` induced by the data | maximal globally hyperbolic development predicate | included; API open |
| global stability | completeness and asymptotic decay toward Minkowski space | causal-geodesic completeness and quantitative estimates | included; exact conjunction open |

## Fidelity boundary

The popular summary "Minkowski spacetime is nonlinearly stable" is not precise enough for a Lean
target. The statement phase must transcribe a specific terminal source claim and crosswalk every
hypothesis and conclusion, including any strong asymptotic-flatness restrictions. Later variants
with different regularity or decay assumptions are candidates only after a checked implication to
the frozen claim. No public Lean candidate has been audited during intake.

Before `H0`, an independent reviewer must verify bibliographic edition, theorem/page, definitions,
all hypotheses, conclusion clauses, and errata and approve the source-to-Lean mapping.
