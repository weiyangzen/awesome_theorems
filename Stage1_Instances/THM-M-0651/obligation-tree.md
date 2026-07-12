# THM-M-0651 obligation registry and typed graphs

Registry version 1 freezes eleven obligations before proof-phase closure is credited. Proof,
refinement, provenance, evidence, trust, documentation, and workflow edges remain separate typed
graphs. Every proof dependency has a reciprocal child-to-parent composition edge.

## root
The exact frozen simultaneous countable omitting-types target. It remains open at `M4`.

## s-exact
Preserve the countable-language binders, satisfiability, varying finite arities, partiality,
nonprincipality, and omission of every type at every tuple.

## l-enum
Enumerate syntax, Henkin witnesses, family indices, and finite tuples into a fair countable schedule.

## l-dense
Prove the nonprincipality extension lemma that preserves finite consistency while adding a formula
which defeats the scheduled realization attempt.

## l-henkin
Iterate the witness and avoidance extensions, form a complete Henkin theory, and construct its
at-most-countable term model. This is the open `ConstructionInterface`.

## l-omit
Decode the fair schedule in the term model and show that each tuple falsifies a member of each
indexed type. This is the open `AvoidanceInterface`.

## t-assemble
Compose the construction and avoidance interfaces into the exact root. The checked Lean theorem
`ObligationTree.root_compose` accepts both substantive interfaces as premises and therefore assigns
no proof closure to them.

## b-arity0
Keep zero-arity types, repeated entries, and the fixed Nat index domain inside the construction.

## x-anchor
The separately implemented infinitary-logic theorem is an architecture reference only. There is no
checked transport to the pinned mathlib semantics and no terminal proof body is credited.

## x-source
A pinpointed primary human theorem/page, exact variant crosswalk, and errata review remain open.

## x-tcb
Transitive kernel, dependency, executable, and final axiom trust review remain open.

## Closure boundary

No obligation is recorded closed. The remaining machine cut set is `L-ENUM`, `L-DENSE`,
`L-HENKIN`, and `L-OMIT`. Proof work must implement these interfaces and validate the resulting
unconditional root; this phase does not claim audit or theorem completion.
