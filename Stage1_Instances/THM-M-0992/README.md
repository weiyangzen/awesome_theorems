# THM-M-0992 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the probabilistic Chebyshev inequality. The
legacy labels `已验证` and `closed` are discovery metadata only and provide no proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | For a real random variable with finite second moment and every `r > 0`, the probability of deviation from its mean by at least `r` is at most its variance divided by `r^2` | Exact Lean binders, measurability/integrability predicates, event spelling, and inequality order remain for the statement phase |
| Probability model | A probability measure on a measurable space; real-valued random variable | Extended-real probability coercions and almost-everywhere conventions must be frozen before elaboration |
| Moment data | Expectation and variance exist through square-integrability (or an exactly equivalent explicit hypothesis package) | No equivalence between candidate hypothesis packages is credited yet |
| Boundary cases | Positive threshold only; zero threshold and infinite/nonexistent second moment are excluded from the canonical claim | Mutations at `r = 0`, strict versus non-strict deviation, and weakened moment assumptions remain required |
| Proof architecture | Center the variable, square the deviation, and apply Markov's inequality | Architecture only; no theorem or proof-body closure is claimed |
| Foundations | Lean 4 kernel and pinned mathlib measure/probability APIs | Toolchain, imports, declaration type, axioms, and dependency closure remain open |

The scope intentionally excludes other results also called Chebyshev's inequality, including the
deterministic sum inequality (`THM-M-0282`), Chebyshev polynomial bounds, and one-sided Cantelli
bounds. Alternate normalizations using a standard-deviation multiplier are candidate transports,
not silently substituted roots.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact Lean statement gate: there is no elaborated declaration, normalized expression hash,
environment fingerprint, checked transport, or mutation evidence. The theorem is not complete.

The structured intake claim is in `intake.json`, source correspondence and ambiguities are in
`source_statement_crosswalk.md`, and exact intake checks are recorded in `validation.md`.

The dependent statement phase is now self-tested pending master acceptance. `Statement.lean`
freezes `Stage1Instances.THM_M_0992.ChebyshevTarget` over a probability measure with `MemLp X 2 P`,
a strictly positive real threshold, and the closed two-sided deviation event. `statement.json` and
`statement-validation.md` bind its expression, imports, environment, mutations, and status boundary.
No proof or theorem-completion claim follows from statement elaboration.
