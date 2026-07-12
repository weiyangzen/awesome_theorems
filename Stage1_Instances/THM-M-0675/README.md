# THM-M-0675: Homogeneous models

This is the rev-5.6 intake dossier for `S56-M-0675-INTAKE`. The repository
source says only "properties of homogeneous models." That is a topic, not a
proposition, and it cannot truthfully determine a Lean target.

## Status boundary

- Lifecycle: `planned` (`L0 / rework_required`).
- Human status: `H4`; no proposition-level primary source is identified.
- Machine status: `M4`; there is no exact proposition to elaborate.
- Readability status: `R4`; theorem-specific reconstruction is unavailable.
- Audit complete: no. Theorem complete: no.

The historical metadata label `已验证` receives no rev-5.6 credit. The
structured record is `intake.json`; `scope.md` records the incompatible
interpretations, and `source_statement_crosswalk.md` traces the source text.

## First failed gate

The rev-5.6 theorem intake contract requires a canonical human mathematical
statement with domains, ordered quantifiers, hypotheses, and a conclusion.
The source fixes none of these. Choosing ultrahomogeneity, cardinal
homogeneity, saturation, or an existence/uniqueness result would broaden or
substitute the target. The required resolution is a pinpoint theorem source
and an explicit choice of homogeneity convention and cardinal scope.

## Open task DAG

1. `S56-M-0675-STATEMENT`: blocked until the source ambiguity is resolved.
2. `S56-M-0675-ANCHOR_AUDIT`: audit exact human and Lean candidates only after statement selection.
3. `S56-M-0675-OBLIGATION_TREE`: freeze graphs only after the statement and source gates.
4. `S56-M-0675-PROOF`: provide genuine proof bodies or pinned imports.
5. `S56-M-0675-VALIDATION`: run kernel, trust, provenance, and replay gates.
6. `S56-M-0675-RELEASE`: reconcile accepted evidence and decide completion.

Exact validation commands and their results are recorded in `validation.md`.
