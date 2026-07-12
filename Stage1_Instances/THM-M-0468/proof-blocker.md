# THM-M-0468 proof-phase blocker

Item: `S56-M-0468-PROOF`.

## Verdict

Blocked at the exact-target consistency gate. The frozen Lean target is not a
faithful concrete formalization of the Ullmo--Zhang theorem: it universally
quantifies over `BogomolovData`, but the structure records no laws connecting
its predicates and operations. `ProofBlocker.lean` constructs a lawful value
of that structure for which all ambient hypotheses and all density claims are
true while `isTorsionPoint` is always false. The left side of the claimed
equivalence is therefore true and `IsSpecial` is false.

Lean kernel-checks `not_bogomolovTarget : Not BogomolovTarget` without a
placeholder or target-specific axiom. Its axiom print contains only mathlib's
standard `propext`, `Classical.choice`, and `Quot.sound`. Thus implementing a proof of the exact frozen root
would make the environment inconsistent. The proof phase cannot truthfully be
self-tested or marked provisional. No `.stage1-worker-selftest.json` is
emitted.

## Required upstream repair

Replace the unconstrained semantic record with concrete pinned definitions of
abelian varieties, canonical height, subvarieties, torsion, and Zariski
density, or add and source every compatibility law needed to rule out this
countermodel. Then repeat the statement, anchor-audit, and obligation-tree
phases before attempting proof closure.

## Validation evidence

Base revision: `c9b3209d36dc2f8783831d5a946196783ef8d684`.

| Command | Exit | Result |
|---|---:|---|
| scoped `lean -o Statement.olean Statement.lean`, then `LEAN_PATH=... lean ProofBlocker.lean` via the pinned `Formalizations/Lean` Lake environment | 0 | Elaborated the countermodel and `not_bogomolovTarget`; axioms were `[propext, Classical.choice, Quot.sound]`; temporary `Statement.olean` removed |
| `git diff --check -- Stage1_Instances/THM-M-0468` | 0 | No whitespace errors |

This is real negative kernel evidence, not theorem completion. Root machine
status remains open, and the first failed proof gate is exact-target
consistency.
