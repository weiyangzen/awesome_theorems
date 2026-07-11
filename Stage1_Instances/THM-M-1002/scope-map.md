# Scope map

## Included claim

- Discrete time indexed by natural numbers on a probability (or finite-measure, if source-equivalent)
  space with an increasing filtration.
- Real-valued adapted, integrable submartingales and the order-dual supermartingale branch.
- Almost-sure convergence to a finite random variable under the classical uniform one-sided
  expectation bound; integrability of the limit is included only to the extent stated by the
  inspected source.

## Decisions reserved for statement freeze

The statement phase must inspect a fixed source edition and settle whether the hypothesis is
`sup n E[X_n^+] < infinity`, uniform `L1` boundedness, or a separately named variant; whether the
limit is merely finite almost surely or integrable; and whether the supermartingale result is a
separate theorem or transport through negation. It must also freeze completeness of the probability
space, filtration measurability conventions, binder order, null-set formulation, and degenerate
cases. These choices must follow the source, not the convenient existing API.

## Explicit exclusions

- Continuous-time, local-martingale, vector/Banach-valued, and extended-real variants.
- Doob's `L^p` convergence theorem (the separate `THM-M-1003` target), optional stopping, and the
  martingale representation theorem.
- Substitution of uniform `L1` boundedness for a weaker one-sided hypothesis without a checked
  equivalence or an explicit narrowing decision.
- Treating the existing `StatementShape` wrapper or the manifest label `已验证` as accepted proof.

The downstream statement must map each source hypothesis to concrete mathlib objects and must
either express the exact one-sided theorem or record the first missing API/bridge precisely.
