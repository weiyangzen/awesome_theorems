# THM-M-0985 rev-5.6 intake

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

The initial proof architecture is probability space -> random-variable interfaces -> iid and
integrability assumptions -> centering/partial sums -> almost-sure convergence -> arithmetic-mean
transport. This is a scope map, not a frozen obligation registry or a proof.

The structured claim and open task DAG are in `intake.json`; source fidelity and convention risks
are in `source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact Lean statement gate. No elaborated target, environment fingerprint, checked transport,
mutation suite, source acceptance, or proof closure is claimed. The theorem is not complete.

