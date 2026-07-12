# Scope map

## Root boundary

| Component | Included | Excluded or deferred |
|---|---|---|
| Programs | a fixed acceptable enumeration of unary partial-recursive `Nat ->. Nat` functions | arbitrary programming-language syntax without an effective semantics bridge |
| Property | `S : (Nat ->. Nat) -> Prop`, invariant under equality of partial functions | code length, instruction set, execution time, and other intensional/syntactic predicates |
| Nontriviality | one represented function satisfies `S` and one represented function does not | empty and universal properties, both of which have constant decision procedures |
| Decision claim | no total computable Boolean/predicate decider for `e |-> S(phi_e)` | semidecidability classification, complexity lower bounds, or promise-problem claims |
| Equality | extensional equality of partial functions, including domain and returned values | equality only on a finite test set or observational approximation |

## Ordered logical shape

1. Freeze an acceptable effective numbering `e |-> phi_e` of unary partial-recursive functions.
2. Quantify over a semantic property `S` of those partial functions.
3. Assume extensionality: `phi_e = phi_d` implies `S(phi_e) <-> S(phi_d)`.
4. Assume nontriviality by represented witnesses on both sides of `S`.
5. Conclude that membership of `e` in the induced index set is not computable.

The witness formulation avoids silently quantifying over partial functions outside the chosen
enumeration. Whether Lean packages `S` directly on `Nat ->. Nat`, on `Nat.Partrec.Code` plus an
extensionality hypothesis, or on recursively enumerable graph/range sets is a statement-phase
choice; any alternate form needs a checked transport.

## Boundary probes for the statement phase

| Probe | Required outcome |
|---|---|
| remove nontriviality | must not be equivalent: constant properties are counterexamples |
| remove extensionality | must not be equivalent: decidable syntactic code properties become admissible |
| change partial to total functions | must not be silently accepted; the classical proof and numbering assumptions change |
| restrict to a finite code domain | must not be equivalent: every predicate on a finite domain is decidable |
| use language semantics | requires a machine-to-language semantic bridge rather than name-level substitution |

No probe has been Lean-checked during intake. They are frozen tests for `S56-M-0708-STATEMENT`.
