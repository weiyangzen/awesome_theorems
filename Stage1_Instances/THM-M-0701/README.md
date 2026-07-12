# THM-M-0701: Resolution principle

This is the rev-5.6 intake dossier for `S56-M-0701-INTAKE`. The repository
describes the target only as an automated theorem-proving method. That is not
a proposition and does not determine one exact Lean theorem.

## Status boundary

- Lifecycle: `planned` (`L0 / rework_required`).
- Human status: `H4`; Robinson's 1965 paper is a discovery anchor, but no
  proposition-level statement and premise crosswalk has been selected.
- Machine status: `M4`; there is no exact proposition to elaborate.
- Readability status: `R4`; theorem-specific reconstruction cannot begin.
- Audit complete: no. Theorem complete: no.

The historical metadata label `已验证` receives no rev-5.6 credit. The
structured authority for this intake is `intake.json`. `scope.md` records the
incompatible theorem choices, and `source_statement_crosswalk.md` traces each
available source phrase without silently strengthening it.

## First failed gate

Section 5 of the rev-5.6 blueprint requires a canonical mathematical claim
with domains, ordered quantifiers, hypotheses, and an exact conclusion. The
source does not say whether the root is resolution-step soundness,
propositional refutation completeness, first-order refutation completeness, or
the lifting lemma. Selecting one would substitute mathematics not fixed by
the target record.

Resolution requires a source owner to select a pinpoint primary theorem and
freeze clause syntax and semantics, the derivability rules (including whether
factoring is present), equality treatment, and all compactness/finiteness
assumptions.

## Open task DAG

1. `S56-M-0701-STATEMENT`: blocked until the source ambiguity is resolved.
2. `S56-M-0701-ANCHOR_AUDIT`: audit the selected source and formal candidates.
3. `S56-M-0701-OBLIGATION_TREE`: freeze typed graphs after statement and source gates.
4. `S56-M-0701-PROOF`: provide genuine exact proof bodies or pinned imports.
5. `S56-M-0701-VALIDATION`: run kernel, trust, provenance, and replay gates.
6. `S56-M-0701-RELEASE`: reconcile accepted evidence and decide completion.

The exact intake validation commands and results are recorded in
`validation.md`.
