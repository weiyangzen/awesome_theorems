# Source-statement crosswalk

| Claim component | Human source anchor | Planned Lean surface | Intake assessment |
|---|---|---|---|
| Weakly convergent probability measures admit representatives converging almost surely | A. V. Skorokhod, "Limit theorems for stochastic processes," *Theory of Probability and its Applications* 1 (1956), 261-290, DOI 10.1137/1101022 | root existential coupling statement | Original primary paper located; exact theorem/page wording, translation variance, assumptions, and corrections still require audit: `H1` |
| Standard separable-metric representation formulation | P. Billingsley, *Convergence of Probability Measures*, 2nd ed., Wiley, 1999, Theorem 6.7 (representation theorem) | Polish-space specialization | Secondary theorem locator supports discovery, but its precise hypotheses and edition pagination must be checked against the physical or immutable digital edition |
| Weak convergence premise | convergence tested by bounded continuous functions / the library's weak-convergence API | planned `Tendsto` or probability weak-convergence predicate | Exact equivalence and required Borel/topological instances remain open |
| Correct marginals | each new representative has the prescribed distribution | planned `Measure.map XSeq_n P = muSeq n` and `Measure.map X P = mu` | Map measurability and probability-space binders are not yet elaborated |
| Almost-sure conclusion | representatives converge pointwise outside a null set | planned `∀ᵐ omega ∂P, Tendsto (fun n => XSeq n omega) atTop (nhds (X omega))` | Candidate shape only; no checked Lean expression |

The canonical scope is the Polish-space specialization. This avoids conflating the theorem with
broader separable-support variants or with representation results requiring exceptional-set or
support qualifications. Conversely, restricting the state space to `Real` would improperly weaken
the named claim. The statement phase must resolve mathlib's exact weak-convergence interface,
serialize the elaborated expression and context, and mutation-test Polishness, probability mass,
common-space marginal equalities, and almost-sure (rather than in-probability) convergence.

Discovery links, not immutable evidence receipts:

- Skorokhod paper: <https://doi.org/10.1137/1101022>
- Billingsley book record: <https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316962>

No `H0` or machine-closure claim is made. Primary-source file hashes, exact pinpoints, premise-to-node
mapping, errata search, and independent review remain required.
