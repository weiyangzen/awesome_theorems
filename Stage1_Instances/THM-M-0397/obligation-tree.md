# THM-M-0397 frozen obligation architecture

Item: `S56-M-0397-OBLIGATION_TREE`

The registry freezes eight root-relevant semantic obligations for the exact
method-level proposition `Stage1Rev56.THMM0397.Statement`. The denominator was
chosen from the elaborated statement and bounded anchor audit, before observing
proof closure. A later split, merge, exclusion, or target correction requires
an append-only registry revision.

## Typed proof route

`M0397-ROOT` is refined by the parameterwise composition `M0397-COMP`. Its
reverse direction needs three distinct inputs: the application-specific
lower-bound-to-height bridge `M0397-REDUCE`, the exact finite enumerator
invariant `M0397-ENUM`, and pinned filter membership `M0397-FILTER`.
`M0397-REDUCE` consumes the selected lower-bound premise `M0397-BOUND`. The
forward direction uses only `M0397-FILTER` and deliberately does not invent a
boundedness premise.

`application_compose` kernel-checks this child-to-parent composition for one
specified application. `root_compose` checks the universal binder transport,
but takes all application closures as an explicit premise. These certificates
freeze architecture; they do not provide a lower bound or concrete reduction.

## Node ledger

| ID | Role | Budget | Current boundary |
|---|---|---:|---|
| `M0397-ROOT` | Exact canonical root | split required | `M0-L`, assurance gates open |
| `M0397-COMP` | Two directions of list/predicate equality | 12 | local composition checked |
| `M0397-BOUND` | Concrete Baker lower-bound input | 20 | explicit premise of the root |
| `M0397-REDUCE` | Lower bound implies height bound | split required | required field of quantified `Application` |
| `M0397-ENUM` | Exact executable height-ball enumeration | 40 | required field of quantified `Application` |
| `M0397-FILTER` | Decidable filter connective | 8 | pinned mathlib anchor checked |
| `M0397-SOURCE` | Primary application/source crosswalk | 30 | `H3`, machine not applicable |
| `M0397-TRUST` | Provenance, TCB, replay, and review | 50 | open release boundary |

Every numeric leaf budget is at most 100 semantic steps. The root and the
problem-specific reduction are explicitly `split required`; their budgets may
not be laundered through the short generic wrapper.

## Separate graph families

`typed-graphs.json` keeps proof, refinement, provenance, evidence, trust,
documentation, and workflow edges separate. In particular, source and trust
edges are not proof premises, and the mathlib filter body is not credited as a
Baker lower bound. Aliases and checked transports receive no duplicate terminal
body credit.

## Freeze boundary

The exact method-level root is kernel-closed: its lower bound is an explicit
premise, while reduction and enumeration are fields of every quantified
`Application`. This does not prove those inputs for any concrete Diophantine
problem. Human-source fidelity, readable reconstruction, terminal provenance,
hermetic replay, independent review, audit completion, theorem completion, and
master acceptance remain open.
