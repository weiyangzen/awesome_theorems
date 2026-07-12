# THM-M-1058 obligation tree

Item: `S56-M-1058-OBLIGATION_TREE`  
Freeze date: 2026-07-12  
Canonical statement SHA-256: `60a04b08693660e1b050384acab58541f1a768cc7dfa32da65ac587e47876a33`

## Frozen architecture

The registry contains 16 unique obligations: 12 mathematical obligations and
four informational assurance overlays. The combined proof/refinement graph is
acyclic and reaches every mathematical obligation from `M1058-ROOT`. All
obligations are open; the checked `Iff.rfl` transport freezes statement shape
only and is not an LDP proof.

| ID | Kind | Required output | Current vector |
|---|---|---|---|
| `M1058-ROOT` | root | exact frozen LDP predicate | `H1/M3/R3` |
| `M1058-TARGET` | definition | domain and binder boundary | `H1/M4/R3` |
| `M1058-DATA` | definition | measures, speed, and rate contract | `H1/M4/R3` |
| `M1058-MEASURES` | definition | probability-measure sequence | `H1/M4/R3` |
| `M1058-SPEED` | definition | positivity and divergence of speed | `H1/M4/R3` |
| `M1058-RATE` | definition | nonnegative lower-semicontinuous rate | `H1/M4/R3` |
| `M1058-SCALED-LOG` | definition | normalized logarithmic probability | `H1/M4/R3` |
| `M1058-RATE-INF` | definition | event rate infimum | `H1/M4/R3` |
| `M1058-UPPER` | semantic leaf | all-closed-set limsup upper bound | `H1/M3/R3` |
| `M1058-LOWER` | semantic leaf | all-open-set liminf lower bound | `H1/M3/R3` |
| `M1058-COMPOSE` | composition | exact conjunction of both bounds | `H1/M3/R3` |
| `M1058-TRANSPORT` | transport | checked direct-expansion equivalence | `H1/M4/R3` |
| `M1058-SOURCE` | source overlay | pinpoint node source and errata review | `H1/M4/R3` |
| `M1058-PROVENANCE` | provenance overlay | terminal-body and dependency provenance | `H1/M3/R3` |
| `M1058-TRUST` | trust overlay | axiom, unsafe, TCB, and computation audit | `H1/M3/R3` |
| `M1058-IMPORTS` | import overlay | pinned minimal statement substrate | `H1/M4/R3` |

The two irreducible mathematical leaves at this architecture level are
`M1058-UPPER` and `M1058-LOWER`. Each ledger has fewer than 100 semantic steps.
A future proof phase must either implement these exact branches for specified
data or classify why no such instance theorem is being claimed. It may not
replace closed sets by compact sets, add a good-rate hypothesis silently, or
turn this property definition into a universal assertion.

## Typed graphs

`typed-graphs.json` keeps proof, refinement, provenance, evidence, trust,
documentation, and workflow edges separate. Proof edges compose the two bound
branches. Refinement edges expose every definition on which their expressions
depend. The assurance overlays cannot contribute mathematical coverage.

The frozen machine denominator is the ordered list of 12 mathematical nodes;
all 16 nodes require readable classification, and the six source-critical
nodes have a separate human-source denominator. The denominator digest is
`603b6a62d345eb0be098c815ee9b1d743faad5f11a5c7bd503fb58a3318973f2`.

## Status boundary

This artifact completes only the architecture freeze and its local structural
self-test. There is no terminal LDP body, composition receipt, H0/R0 review,
audit completion, or theorem completion. The root remains `M3`, with
`M1058-UPPER` and `M1058-LOWER` as the current mathematical cut set. Master
acceptance is required before the scheduler item can advance from `[ ]`.
