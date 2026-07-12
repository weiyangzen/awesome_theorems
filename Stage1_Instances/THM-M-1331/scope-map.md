# Scope map

## Received scope

The catalogue fixes only the title "existence and uniqueness theorem," the gloss "existence and
uniqueness of solutions under a Lipschitz condition," an attribution to Cauchy and Picard in 1890,
and an untrusted `已验证` label. Stage0 repeats those fields and explicitly leaves definitions,
premises, foundations, proof details, and formal artifacts open.

The received words constrain the target to an ODE existence-and-uniqueness result with a Lipschitz
condition among its hypotheses. They do not select one local or global formulation. These
words, rather than a familiar textbook theorem supplied from memory, are the intake boundary.

## Candidate mathematical boundary

An eventual exact target may concern an initial-value problem only after a reviewed source fixes:

- the time domain and state space, including completeness, dimension, norm, and scalar field;
- autonomous or time-dependent vector field and the precise local time-state region;
- continuity or measurability in time and which state variable carries the Lipschitz condition;
- local versus global Lipschitz continuity, its constant and uniformity, and any norm bound;
- the initial time and state and the condition keeping the solution inside the local region;
- a nontrivial one-sided or two-sided interval and endpoint derivative convention;
- the solution predicate, usually derivative or integral-equation form;
- uniqueness among which curves, on which fixed or overlapping domain, and with what range
  restriction.

This is a candidate inventory, not a canonical statement. Exact binders and hypotheses remain empty
in `instance.json` until a source and target identity are accepted.

## Neighboring-target collision

`THM-M-1332`, immediately adjacent in the same catalogue, is named "Picard-Lindelof theorem" and
has the gloss "existence and uniqueness of ODE solutions." The current record gives no principled
distinction beyond attribution, date, and the explicit Lipschitz phrase on `THM-M-1331`.

The statement phase must obtain one of these outcomes before elaboration:

1. an approved source crosswalk showing materially different propositions;
2. an approved alias/deduplication relationship with shared terminal-body ownership but no duplicate
   semantic coverage; or
3. an authoritative repository correction.

It must not independently select the same Picard-Lindelof proposition for both IDs and count it
twice.

## Degenerate and boundary cases

The source must decide zero-radius or zero-width intervals, zero Lipschitz and norm bounds, constant
vector fields, boundary initial data, solutions leaving the hypothesis region, derivative-within
behavior at endpoints, overlapping solutions with different declared domains, and a
zero-dimensional state space. None may be discarded merely to fit an available API.

## Explicit exclusions

- A Gronwall uniqueness theorem without existence.
- Peano's continuity-only existence theorem (`THM-M-1333`).
- Global existence derived from a merely local Lipschitz hypothesis without a source-specified
  continuation or growth condition.
- The autonomous continuously differentiable special case as a substitute for the received
  Lipschitz theorem.
- Continuous dependence, maximal continuation, stability, flows on manifolds, or numerical solver
  convergence as the root.
- A record that accepts an existing solution or the uniqueness conclusion as an input field.
- Silent substitution of `THM-M-1332`, or duplicate proof and metric credit across the two targets.

Pinned mathlib has adjacent existence and uniqueness APIs, but their composition, domains, and
source fidelity remain later statement and anchor-audit work.
