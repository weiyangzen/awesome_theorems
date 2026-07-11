# Source-statement crosswalk

The metadata phrase "martingale characterization of diffusion processes" is
not precise enough to select one root theorem. The crosswalk therefore records
the non-negotiable components and the source pin needed to freeze each one.

| Claim component | Primary-source candidate | Lean target family | Intake assessment |
|---|---|---|---|
| Canonical path process | Stroock-Varadhan, *Multidimensional Diffusion Processes* (1979), martingale-problem setup | probability law on continuous paths, coordinate process, natural filtration | Object model not selected |
| Generator | Same source; second-order diffusion operator associated to `a` and `b` | `L f`, including first and second derivatives and coefficient pairings | Dimension, derivative API, and coefficient assumptions open |
| Martingale identity | Same source; definition and characterization chapters | `f(X_t) - f(X_0) - integral_0^t Lf(X_s) ds` is a martingale for every admitted `f` | Test class, filtration, measurability, and integrability open |
| Existence | Stroock-Varadhan (1969 I/II) and the 1979 monograph | existence of a path law solving the martingale problem | Exact theorem and assumptions not yet pinpointed |
| Uniqueness/characterization in law | 1979 monograph, uniqueness/well-posedness development | equality of solution laws or uniqueness of the martingale-problem solution | Exact direction and local/global scope unresolved |
| Initial condition | Source theorem to be selected | point start `X_0 = x` or prescribed initial law | Quantification unresolved |

## Required source decision

The statement phase must choose and record one primary theorem with edition,
chapter/theorem/page, complete assumptions, and any errata. It must then decide
whether the root is:

1. the implication from a weak SDE solution to a martingale-problem solution;
2. the converse construction;
3. equivalence of weak solutions and martingale-problem solutions; or
4. an existence-and-uniqueness theorem under specified coefficient conditions.

These formulations are related but not interchangeable. No direction may be
deleted merely because it is easier to express in current mathlib.

The 1969 article metadata and 1979 monograph are primary-source discovery
anchors, not immutable evidence receipts. Page images or an edition-stable
copy, bibliographic hashes, errata search, premise-to-node mapping, and
independent source review remain required. Consequently this intake makes no
`H0` claim.
