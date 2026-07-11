# THM-M-0009 frozen obligation tree

Registry version 1 freezes the architecture before proof-phase closure credit. Each entry below is
an architecture summary, not an `R0` reconstruction or an accepted proof.

## root

`M0009-ROOT` is the exact frozen conjunction: every short exact sequence in any abelian category
with `HasExt` induces both universally indexed Ext exactness branches. Its conditional assembly is
checked in `ObligationTree.root_compose`; the branch premises remain open in this phase.

## s-binders

`M0009-S-BINDERS` owns the universe-polymorphic category, instances, object, short complex,
`ShortExact` witness, natural degrees, and successor equality. Specialization or loss of either
degree quantifier changes the theorem.

## s-transport

`M0009-S-TRANSPORT` owns the checked equivalence between the canonical conjunction and the two
separately named variance propositions in `Statement.lean`.

## s-foundation

`M0009-S-FOUNDATION` owns the foundation and trust decision. Current narrow probes report
`propext`, `Classical.choice`, and `Quot.sound`; transitive release-grade trust remains open.

## n-variance

`M0009-N-VARIANCE` splits the root into exactly two branches, covariant in the second Ext argument
and contravariant in the first. The split is exhaustive because its checked parent is a conjunction.

## b-cov

`M0009-B-COV` retains every `X`, short exact sequence, and successive degree pair. It supplies the
first premise of the assembly node.

## b-contra

`M0009-B-CONTRA` retains every `Y`, short exact sequence, and successive degree pair. Its successor
equality has mathlib's contravariant orientation and it supplies the second assembly premise.

## c-cov-seq

`M0009-C-COV-SEQ` owns construction of `Abelian.Ext.covariantSequence`, including its connecting
morphisms and the six-arrow window at arbitrary successive degrees.

## c-contra-seq

`M0009-C-CONTRA-SEQ` separately owns `Abelian.Ext.contravariantSequence`; it is not an alias of the
covariant construction and therefore has its own provenance boundary.

## l-cov-exact

`M0009-L-COV-EXACT` is the material imported bridge to `Abelian.Ext.covariantSequence_exact` at
mathlib revision `8a178386`. Its deeper four-position exactness bodies remain a provenance and
readability task for later phases.

## l-contra-exact

`M0009-L-CONTRA-EXACT` is the independent bridge to
`Abelian.Ext.contravariantSequence_exact` at the same revision. The two lemma nodes form the frozen
minimal open root cut set.

## t-assemble

`M0009-T-ASSEMBLE` consumes exactly `CovariantBranch` and `ContravariantBranch` and returns `Root`.
The kernel-checked proof invokes no exactness theorem and hence cannot itself close either premise.

## x-upstream

`M0009-X-UPSTREAM` records the pinned mathlib file and terminal declarations. Wrapper identity,
terminal body identity, and transitive dependency identity remain distinct.

## x-source

`M0009-X-SOURCE` remains `H2`: no accepted edition/theorem/page/assumption/errata crosswalk or
independent source review exists yet.

## x-tcb

`M0009-X-TCB` remains open for complete compiled artifacts, executables, axioms, dependencies,
supply chain, and reproducibility closure.

## Status boundary

The registry has 15 canonical obligations and seven separate graph classes. All semantic budgets
are at most 100 steps. No obligation is credited closed; proof, H0/R0 review, transitive trust,
audit completion, theorem completion, release readiness, and master acceptance remain open.
