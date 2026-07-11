# THM-M-0983 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the law of large numbers entry. It treats the
legacy Stage1 module as discovery material only and assigns it no proof or acceptance credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | For IID Bernoulli trials, the empirical success frequency converges almost surely to the common success probability | Exact Lean elaboration and expression fingerprint belong to the dependent statement phase |
| Sample space | An arbitrary measurable space with a probability measure | Probability-measure and measurability obligations must be explicit in the final target |
| Random variables | A sequence of measurable `{0,1}`-valued trials with common law and joint independence | The legacy pairwise-independent package is a candidate encoding, not yet the frozen target |
| Limit | `n⁻¹ * sum_{i<n} X i` tends to `p` almost everywhere as `n -> infinity` | Indexing at `n = 0` and the empty average require a checked boundary convention |
| Alternate reading | Convergence in probability | A consequence/corollary candidate, not a substitute for the almost-sure root |
| Foundations | Lean 4 kernel and pinned mathlib probability/measure theory | Toolchain, dependency, foundation, TCB, and computation fingerprints remain open |

The canonical claim and provisional formal candidate are structured in `intake.json`. The source
genealogy and the precise gaps between the human wording and Lean candidate are recorded in
`source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact-statement gate: this intake has no elaborated expression hash, environment fingerprint,
checked transports, or mutation tests. It does not claim that the historical source, the legacy
wrapper, or the theorem is accepted or complete.

## Validation

The commands and results in `validation.md` establish manifest membership, repository-standard
consistency, JSON syntax, and dossier-local reference integrity only.
