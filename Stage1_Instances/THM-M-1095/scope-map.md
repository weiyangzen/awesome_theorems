# Scope map

## Catalog scope

The repository supplies the Chinese name `扩散过程` (diffusion processes), attributes it to many
mathematicians in the twentieth century, and gives only `扩散过程的理论` (the theory of diffusion
processes) as its content. These fields do not specify a proposition, quantifier order, hypotheses,
or conclusion.

## Candidate roots requiring a source decision

| Candidate family | Objects and likely claim | Material choices still hidden |
|---|---|---|
| Martingale problem | A process whose generator-compensated test functions are martingales; well-posedness characterizes its law | State space, test domain, generator, path regularity, existence versus uniqueness |
| Stochastic differential equation | Existence and/or uniqueness of a solution to `dX_t = b(t,X_t)dt + sigma(t,X_t)dW_t` | Weak/strong solution, uniqueness notion, coefficient regularity, explosion and horizon |
| Transition semigroup/generator | Markov transition kernels and their relation to an infinitesimal generator or evolution equation | Homogeneity, Feller assumptions, generator domain, density and boundary conditions |

## Explicit exclusions

- A bare definition, taxonomy, textbook chapter, or structure with theorem conclusions as fields.
- Brownian motion as a substitute for arbitrary diffusions.
- A finite-state or discrete-time Markov theorem as a continuous diffusion theorem.
- Silent reuse of the distinct martingale-characterization (`THM-M-1049`), Krylov-estimate
  (`THM-M-1050`), Kolmogorov-equation (`THM-M-1091`/`THM-M-1094`), or diffusion-ergodicity
  (`THM-M-1096`) targets.
- Claiming that general probability and process APIs prove any terminal diffusion theorem.

## Statement-phase blocking decision

The statement phase must not elaborate an invented signature. It may proceed only after recording
a primary edition and pinpoint locator, transcribing the exact proposition, and explaining why that
proposition resolves this catalog entry without duplicating or weakening a neighboring target.
Boundary probes must then cover time horizon, initial law, state space, coefficient degeneracy,
explosion, and the selected existence/uniqueness notion as applicable.
