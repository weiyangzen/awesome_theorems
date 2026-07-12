# THM-M-0508 obligation architecture

The frozen proof route uses the classical ternary circle method. It counts ordered prime triples,
rewrites that count as a Fourier integral, separates major and minor arcs, obtains a positive major
term on odd inputs, controls the minor contribution, and transports positivity to the exact target.
The registry is an architecture denominator, not evidence that these deep analytic leaves are proved.

## Proof nodes

| ID | Role | Frozen obligation | State |
|---|---|---|---|
| `M0508-ROOT` | root | Exact eventual three-primes target | M4 open |
| `M0508-S-COUNT` | definition | Finite ordered representation count | M1 defined |
| `M0508-L-COUNT-POS` | bridge | Positive count iff three-prime existence | M0-L checked |
| `M0508-N-FOURIER` | normalization | Ternary exponential-sum integral identity | M4 open |
| `M0508-B-ARCS` | branch | Major/minor partition and coverage | M4 open |
| `M0508-C-MAJOR` | construction | Uniform major-arc parameters | M4 open |
| `M0508-L-MAJOR` | core lemma | Major-arc asymptotic and error | M4 open |
| `M0508-L-SINGULAR` | core lemma | Positive lower bound for the singular series | M4 open |
| `M0508-C-MINOR` | construction | Complementary minor arcs | M4 open |
| `M0508-L-MINOR` | core lemma | Minor-arc contribution bound | M4 open |
| `M0508-L-POSITIVE` | terminal | Eventual positivity on odd inputs | M4 open |
| `M0508-T-ASSEMBLE` | transport | Conditional composition to exact root | M0-L checked |

## Overlays

`M0508-X-SOURCE`, `M0508-X-FOUNDATION`, `M0508-X-PROVENANCE`,
`M0508-X-READABLE`, and `M0508-X-WORKFLOW` independently track source fidelity, trust,
terminal-body provenance, readable reconstruction, and release workflow. None receives proof credit.
Every node has a semantic ledger of at most 24 steps and appears in all seven typed graph indexes.

## Root boundary

The first open analytic cut set is `M0508-N-FOURIER`, `M0508-B-ARCS`, `M0508-L-MAJOR`,
`M0508-L-SINGULAR`, and `M0508-L-MINOR`. `ObligationTree.lean` proves only the finite-count
equivalence and conditional child-to-root composition. Root debt remains `[H1, M4, R3]`; there is
no proof, audit completion, release, or theorem-completion claim.
