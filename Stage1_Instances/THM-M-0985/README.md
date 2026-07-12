# THM-M-0985 rev-5.6 statement

This directory is the rev-5.6 `planned` instance for Kolmogorov's strong law of large
numbers. It freezes the intended iid, integrable, real-valued form: the arithmetic means
converge almost surely to the common expectation. The repository metadata's `已验证` label is
untrusted discovery input and supplies no proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Probability model | A probability space and a sequence of real-valued random variables | Exact Lean probability-space typeclass and measurability interfaces remain statement work |
| Hypotheses | Identical distribution, mutual independence, measurability, and finite first absolute moment | Pairwise independence is not silently substituted for mutual independence |
| Root conclusion | `n`-term averages converge almost surely to the common expectation | Index origin and the `n = 0` convention must be fixed by checked transports |
| Equivalent view | Centered partial sums divided by `n` converge almost surely to zero | Candidate equivalence only; no machine credit at intake |
| Exclusions | Weak/in-probability laws, finite-state special cases, non-iid variants, and variance-only sufficient forms | These may become lemmas but cannot replace the root |
| Foundations | Lean 4 kernel and pinned mathlib measure/probability/integration APIs | Toolchain, imports, axioms, TCB, and normalized expression hash remain open |

The canonical Lean target is now frozen in `Statement.lean` with the single direct import
`Mathlib.Probability.StrongLaw`. It fixes a universe-polymorphic sample space, an explicit
probability measure, real-valued variables, mutual independence, identical distribution,
measurability, integrability, zero-based `range n` averages, almost-everywhere convergence, and
the Bochner integral of `X 0`. `statement.json` records its environment and mutation probes.

The initial proof architecture is probability space -> random-variable interfaces -> iid and
integrability assumptions -> centering/partial sums -> almost-sure convergence -> arithmetic-mean
transport. This is a scope map, not a frozen obligation registry or a proof.

The structured claim and open task DAG are in `intake.json`; source fidelity and convention risks
are in `source_statement_crosswalk.md`.

## Statement verdict

Lifecycle remains `planned`; provisional root vector remains `[H1, M3, R3]`. The exact statement,
checked definitional expansion, boundary lemmas, and four structural mutation probes elaborate in
the pinned environment. Source acceptance, anchor audit, proof closure, trust closure, and release
evidence remain open. The theorem is not complete.
