# THM-M-1059 rev-5.6 intake

This directory is the `planned` intake for Cramer's theorem on large deviations of sums of
independent random variables. The repository source supplies only the phrase "large deviations of
sums of independent random variables". That phrase does not uniquely determine a theorem: it omits
i.i.d. versus merely independent variables, the state space, normalization, moment assumptions,
and whether the conclusion is an LDP or a one-sided tail limit.

## Scope map

| Node | Provisional scope | Intake boundary |
|---|---|---|
| `CR-ROOT` | Cramer's large-deviation theorem for normalized sums | Exact formulation is deliberately open |
| `CR-RV` | Real-valued i.i.d. random variables and partial sums | Probability-space and measurability binders remain to be frozen |
| `CR-LMGF` | Log moment-generating function and effective domain | Extended-real encoding and finiteness assumptions remain open |
| `CR-RATE` | Legendre-Fenchel transform as rate function | Goodness and lower-semicontinuity are not yet credited |
| `CR-UPPER` | Closed-set upper large-deviation bound | Topological and extended-real conventions remain open |
| `CR-LOWER` | Open-set lower large-deviation bound | Exponential tilting hypotheses remain open |
| `CR-TAIL` | One-sided scalar tail formulation | Candidate consequence or alternate root, not silently identified with the LDP |

Excluded from the root unless a source audit requires them are non-i.i.d. triangular arrays,
Banach-space versions, dependent sequences, moderate deviations, and Cramer-Wold. Degenerate laws,
empty/open/closed sets, infinite rate values, and moment-generating functions finite only at zero
are boundary probes, not exclusions.

## Intake verdict

Lifecycle is `planned`; root vector is `[H2, M4, R3]`. The first failed gate is exact-statement
selection. No Lean declaration, proof closure, or source-fidelity acceptance is claimed. The
dependent statement phase must choose a source-backed formulation before elaboration.

