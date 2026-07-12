# Scope map

## Preserved source scope

- Subject: a discrete-time Markov chain on a general measurable state space.
- Named notion: a petite subset, in the Meyn-Tweedie sense, related to minorization of a sampled
  transition kernel.
- Stated relationship: some connection between small/petite sets and ergodic behavior.
- Historical locator: Meyn and Tweedie, 1993.

This is the complete scope justified by the repository record. It is not yet a theorem statement.

## Decisions required before statement freeze

The statement phase must select a primary-source theorem and freeze the state-space measurability
assumptions; transition kernel and its iterates; whether the chain is irreducible, aperiodic,
Harris recurrent, positive Harris recurrent, or a T-chain; the precise petite-set and small-set
definitions; the sampling distribution and minorizing measure; and the exact recurrence,
accessibility, convergence, or ergodicity conclusion. It must preserve binder order and settle
empty sets, the zero measure, support of the sampling law, indexing from zero or one, and whether
the claim concerns every petite set, existence of one, or a level set produced by a drift condition.

## Explicit exclusions

- A definition of `petite` presented as though it were a theorem.
- The theorem that every small set is petite, its converse under extra assumptions, or an
  irreducibility/aperiodicity criterion selected solely because it is convenient to formalize.
- Finite-state Markov-chain convergence as a substitute for the general-state-space claim.
- A drift condition, Harris ergodic theorem, or Meyn-Tweedie theorem from an adjacent target.
- A structure or hypothesis that assumes the desired minorization or ergodicity conclusion.
- The repository label `已验证` as human-source or kernel evidence.

No Lean target is frozen at intake. A later statement must expose concrete measurable spaces,
Markov kernels, kernel iterates/mixtures, set minorization, and the selected ergodic conclusion.
