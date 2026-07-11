# Source-statement crosswalk

## Source boundary

The repository's source record says only "asymptotics of the renewal function," attributes the
result to David Blackwell in 1948, and labels it `verified`. That metadata identifies a theorem
family but does not state its assumptions or either limiting formula. It receives no proof credit.

The historical primary-source candidate is David Blackwell, "A renewal theorem," *Duke
Mathematical Journal* 15 (1948), 145-150. Exact issue metadata, theorem numbering, page-level
wording, assumptions, corrections, and a stable content hash have not yet been inspected in this
intake. A modern source candidate is William Feller, *An Introduction to Probability Theory and Its
Applications*, volume II, the renewal-theory chapter; edition, section, theorem number, and errata
also remain to be pinned. These are discovery anchors, not `H0` evidence.

## Crosswalk

| Source concept | Frozen repository meaning | Required Lean surface | Intake status |
|---|---|---|---|
| interarrival distribution | probability law `F` on nonnegative reals | probability measure plus support predicate | included; zero-atom convention open |
| mean | `mu = integral t dF`, finite and positive | integrability and real-valued integral | included; encoding open |
| renewal measure | `U = sum F^{*n}`, including `n = 0` provisionally | measure convolution powers and countable sum | included; endpoint normalization open |
| nonarithmetic law | support not contained in a translate of a positive lattice | precise nonlattice predicate | included; formal definition open |
| nonarithmetic conclusion | `U((x,x+h]) -> h/mu` for every `h > 0` | `Tendsto` at `atTop` | included; exact interval form open |
| arithmetic law | law with maximal span `d` | lattice-support and maximal-span predicate | included; lattice origin open |
| arithmetic conclusion | span-cell renewal mass tends to `d/mu` | sequence/filter limit on lattice cells | included; exact index form open |

## Fidelity obligations

Before `H0`, an independent reviewer must inspect the pinned primary source, record exact theorem
and pages, map every assumption and both branches row by row, and check later corrections or errata.
Before any statement credit, Lean must elaborate the exact chosen target and check the cumulative
function, renewal-measure, and lattice formulations rather than relying on their mathematical
resemblance.

The two likely nearby results are excluded as substitutes: the elementary renewal theorem gives a
global ratio asymptotic, while the key renewal theorem integrates a test function against the
renewal measure. Either may later become a dependency, but neither is the frozen Blackwell root.
