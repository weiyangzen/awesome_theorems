# THM-M-0389 frozen obligation tree

## Root and top-level composition

`M0389-ROOT` is the exact integer classification frozen in `Statement.lean`.
The first logical split asks whether any coordinate is zero. The zero branch
must prove that the solution is `(0,0,0)`. The nonzero branch must normalize
signs to a positive Markov solution and then invoke positive generation.
`root_compose` consumes exactly those three propositions and returns the root.
It checks exhaustiveness and recomposition, not the propositions themselves.

Definitions, the legacy statement transport, and the terminal composition own
separate IDs. This prevents a definition, wrapper, or conditional theorem from
being counted as another root proof. The frozen denominator is sixteen required
root-relevant obligations and has no exclusions.

## Positive descent subtree

`M0389-L-POSGEN` is the central converse: every positive solution is generated
from `(1,1,1)`. It is expanded into coordinate ordering, the ordered `x = 1`
branch, construction of a positive smaller Vieta descendant, well-founded
termination/minimality, and reversal of the finite descent chain. The graph
also exposes equation preservation and strict height decrease as bridges.

The repo-local legacy file checks mutation soundness, height decrease, one-step
reverse mutation, zero-coordinate algebra, and permutation support. It does not
check descendant positivity, strictness, termination, minimality, the complete
reverse-chain argument, sign normalization, or positive generation. Those
interfaces remain open and the legacy bodies receive only partial provenance.

## Leaf ledgers and boundaries

`proof-units.json` gives each obligation a precise claim, output, debt,
provenance boundary, validation target, substantive ledger, and explicit
non-claim. Every current ledger has at most six steps. These are architectural
ledgers, not completed proofs or an `R0` reconstruction. Any node that reveals
a hidden case split, induction, construction invariant, major imported theorem,
or ledger over 100 steps must be split in a new append-only registry version.

## Trust and source boundaries

The local composition module imports only `Init`; its axiom report is empty.
That narrow fact does not close the eventual proof's imports, terminal bodies,
automation, axioms, replay, or independent verification. `M0389-X-TRUST`
therefore remains separate and open.

The source audit found only a bibliographic lead to Markoff's 1879 paper, not a
pinpoint theorem/page crosswalk. Consequently every node remains source-eligible
but none receives `H0`. Machine closure, readable reconstruction, audit
completion, theorem completion, and master acceptance are not claimed here.
