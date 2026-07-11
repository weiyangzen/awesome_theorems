# THM-M-1066 rev-5.6 intake

This directory is the `planned` intake dossier for the KMT theorem. The repository source says only
"strong approximation of a random walk by Brownian motion." That identifies the Komlos-Major-
Tusnady strong-invariance-principle family, but it does not select one of the original scalar,
multidimensional, empirical-process, or quantitative-tail variants. This intake preserves that
boundary rather than silently choosing a stronger or weaker theorem. The historical `已验证` label
is untrusted metadata and supplies no proof credit.

## Scope map

| Surface | Intended scope | Boundary at intake |
|---|---|---|
| Root family | Couple partial sums of independent random variables with a Brownian motion so that their uniform discrepancy grows only logarithmically | The exact original theorem and constants must be selected from a pinned primary source |
| Random input | The classical scalar i.i.d. centered, variance-one setting with an exponential-moment condition is the leading candidate | Whether the source permits non-identical variables, vectors, or weaker moments remains open |
| Coupling | Copies of the increments and a standard Brownian motion constructed on one probability space | Equality in distribution, filtration/adaptedness, and enlargement conventions must be frozen |
| Error | A maximum over integer times, with an `O(log n)` almost-sure consequence and a stronger exponential tail estimate in common formulations | Quantifier order, constants, the range of `n` and the tail parameter are not yet canonical |
| Exclusions | Donsker weak convergence, Skorokhod embedding alone, empirical-process-only results, and a Brownian approximation assumed as input | These may be dependencies or consequences but cannot replace the root |
| Lean surface | Probability measures, independence, partial sums, Brownian motion, coupling, maxima, and asymptotics in pinned Lean 4/mathlib | No module, declaration, expression hash, or checked transport is credited at intake |
| Foundations | Lean 4 kernel plus versioned probability/measure foundations and any accepted classical-choice principles | Dependency, TCB, and computation profiles remain open |

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
The next phase must select and transcribe a pinpoint primary-source variant before elaborating Lean.
It must freeze ordered binders, all moment and normalization assumptions, the coupling semantics,
constant dependencies, and boundary cases before any formal-proof candidate is credited.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
exact source-statement identification. No Lean theorem or proof closure is claimed. Validation in
`validation.md` covers only target membership, repository consistency, JSON syntax, and local
dossier integrity.
