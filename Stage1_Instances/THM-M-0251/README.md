# THM-M-0251: inner-outer factorization intake

## Status

This directory is a `planned` rev-5.6 intake for `S56-M-0251-INTAKE`. It starts from the
uniform `L0 / rework_required` baseline and contains no accepted proof state. The worker-proposed
root vector is `[H5, M4, R4]`: the received catalog wording does not yet identify a stable
proposition, no usable exact formal target has been located, and no independently reviewed
reconstruction exists. `H5` classifies this catalog target as presently ill-posed; it does not
claim that standard Hardy-space factorization results are false or mathematically open.

The intake node is self-tested but remains provisional `[_]` until master acceptance. Both audit
completion and theorem completion are false. All statement, anchor-audit, obligation-tree, proof,
validation, and release tasks remain open.

## Catalog Boundary

The source corpus says only `Hardy空间的内-外分解`, attributes it to Arne Beurling in 1949, and
labels it `已验证`. It supplies no primary citation or theorem locator and does not choose a Hardy
exponent, domain, nonzero premise, boundary-value convention, definitions of the factors,
factorization components, equality convention, normalization, uniqueness statement, or boundary
cases. The status label is untrusted metadata, not human or machine proof evidence.

Selecting the familiar assertion that a nonzero `H^p` function on the unit disk factors as an
inner function times an outer function would still make several source-dependent choices. It is
recorded only as candidate scope, never as the canonical claim.

## Artifact Map

- `instance.json`: planned scope authority, source and environment pins, null canonical target,
  profiles, ownership, and status boundary.
- `scope-map.md`: proposition-changing choices, included family, exclusions, degenerate cases,
  neighboring targets, and retry condition.
- `source-statement-crosswalk.md`: line-level catalog provenance, candidate source boundary, and
  formal API crosswalk.
- `task-dag.json`: the six dependency-ordered downstream tasks, all open.
- `IntakeProbe.lean`: a discovery-only check of pinned unit-disk, Lp, and canonical-factor APIs.
- `check_intake.py`: scoped fail-closed validator for this dossier and worker packet.
- `validation.md`: exact commands, results, environment, open gates, and evidence boundary.
- `intake-receipt.json`: unsigned provisional node receipt; it is not an accepted or release-grade
  receipt.

## First Downstream Gate

An independent complex-analysis source reviewer must select and preserve an immutable exact
proposition with pinpoint definitions and assumptions, reconcile the Beurling/1949 attribution,
audit corrections, and approve the statement crosswalk. Only then may the statement phase encode,
elaborate, fingerprint, transport, and mutation-test a canonical Lean target.

The pinned mathlib module `Mathlib.Analysis.Complex.CanonicalDecomposition` supplies individual
canonical-factor lemmas but explicitly leaves formulation of canonical decomposition as a TODO.
Those APIs demonstrate nearby infrastructure only; they do not state or prove this target.
