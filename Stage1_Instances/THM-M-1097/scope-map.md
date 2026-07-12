# Scope map

## Provisional included family

- A time-homogeneous Markov chain on a general measurable state space with transition kernel `P`.
- A source-specified irreducibility notion, commonly `psi`-irreducibility, and any required
  aperiodicity or Harris assumptions.
- A measurable Lyapunov function and a Foster-Lyapunov drift inequality outside a small or petite
  set, with the exact constants and integrability conditions taken from the selected theorem.
- A stability conclusion selected verbatim from the source: for example positive Harris
  recurrence and an invariant probability measure, or geometric convergence in a weighted norm.

This is deliberately a claim family rather than a proposition. "Meyn-Tweedie theory" covers many
non-equivalent stability results, and the repository phrase does not choose one.

## Decisions required at statement freeze

The statement phase must select the exact primary theorem and freeze whether time is discrete or
continuous; the measurable-space assumptions; the transition-kernel and iterate conventions;
`psi`-irreducibility, Harris recurrence, aperiodicity, smallness, petiteness, and accessibility;
the Lyapunov codomain and drift inequality; and whether the conclusion is existence, uniqueness,
positive Harris recurrence, total-variation convergence, a weighted-norm bound, or an equivalence.

It must also freeze binder order and universes and handle degenerate cases explicitly: empty state
spaces, zero or infinite reference measures, unreachable drift sets, constant Lyapunov functions,
zero drift constants, periodic chains, reducible chains, and invariant measures that are only
sigma-finite. Any theorem using a skeleton chain or sampled kernel must expose that construction.

## Explicit exclusions

- Treating the whole Meyn-Tweedie monograph or a collection of results as one proposition.
- Substituting the finite-state stationary-distribution theorem for a general-state-space result.
- Calling invariant-measure existence alone "stability" when the selected source concludes Harris
  recurrence or convergence.
- Substituting a drift-condition definition, a petite-set lemma, or an MCMC convergence theorem for
  the selected stability implication.
- Assuming recurrence, an invariant probability, or the desired convergence bound as a field of an
  abstract structure.
- Using the metadata label `已验证`, a citation, or a theorem-family name as Lean proof evidence.

A downstream formal target must expose the actual Markov kernel, measurability, recurrence,
minorization/petiteness, drift, and convergence interfaces. Stronger results are acceptable only
through checked specialization to the exact selected source statement.
