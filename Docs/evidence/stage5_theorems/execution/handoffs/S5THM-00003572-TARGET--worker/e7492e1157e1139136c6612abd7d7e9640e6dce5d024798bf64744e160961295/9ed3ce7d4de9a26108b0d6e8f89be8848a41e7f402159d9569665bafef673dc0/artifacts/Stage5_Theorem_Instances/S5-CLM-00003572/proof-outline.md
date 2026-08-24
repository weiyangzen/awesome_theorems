# Proof outline — Erdős Problem 1023, Erdős–Kleitman variant

<a id="pu-01"></a>
## PU-01 — Frozen certificate boundary

Hypothesis: the provider sequence has the exact two-sided asymptotic relation in the frozen
statement. Inference: expose that typed certificate at the claim-owned Mathlib-only boundary.
Output: the same `IsTheta` proposition. Formal anchor: `certificateBoundary` in `Proof.lean`.
Downstream use: PU-02. Exceptional case: the provider's numeric module is provenance rather than an
active import. Trust boundary: provider proof bytes are not used.

<a id="pu-02"></a>
## PU-02 — Lower component preservation

Hypothesis: PU-01's exact certificate. Inference: preserve its lower-bound component without
changing the sequence, filter, exponent, or coercions. Output: the frozen two-sided relation.
Formal anchor: `lowerComponent`. Downstream use: PU-03. Exceptional case: natural-to-real coercion
is retained verbatim. Trust boundary: Mathlib elaboration is deferred to the Master.

<a id="pu-03"></a>
## PU-03 — Upper component preservation

Hypothesis: PU-02's output. Inference: preserve its upper-bound component at `Filter.atTop`.
Output: the frozen two-sided relation. Formal anchor: `upperComponent`. Downstream use: PU-04.
Exceptional case: the real exponent `(1 / 2 : ℝ)` is not rewritten. Trust boundary: no external
asymptotic theorem is silently imported.

<a id="pu-04"></a>
## PU-04 — Root composition

Hypotheses: the exact frozen certificate plus PU-01 through PU-03. Inference: compose the typed
nodes at the unchanged target surface. Output: the claim-owned Erdős–Kleitman theorem.
Formal anchor: `erdosKleitman`. Downstream uses: audit root and release receipt. Exceptional case:
the source's `F` remains provider-owned and is passed parametrically. Trust boundary: canonical
trust-zero compilation and semantic-environment recomputation belong to the Master.
