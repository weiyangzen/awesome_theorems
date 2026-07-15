# THM-M-0122: Faltings' theorem

This directory is the rev-5.6 planned dossier for the Mordell-conjecture
consequence of Faltings' work. `S56-M-0122-STATEMENT` has worker-local
self-tested exact-target evidence, and `S56-M-0122-ANCHOR_AUDIT` now has a
bounded immutable candidate inventory. The intake dependency, statement
receipt, and anchor-audit receipt remain provisional pending dependency-ordered
master acceptance.

## Status boundary

- Lifecycle: `planned` (`L0 / rework_required`).
- Human status: `H4`; the primary paper is identified, but its exact internal
  locator, conventions, assumptions, and errata have not been independently
  audited.
- Machine status proposed by this worker: `M3`. `FaltingsTarget` elaborates,
  but no Faltings proof body exists and the concrete H1-based genus
  normalization still lacks a pinned native K-linear comparison.
- Readability status proposed by this worker: `R3`; the exact statement and
  representation boundary are documented but not independently reviewed.
- Audit complete: no. Theorem complete: no.

The canonical formal target is
`Stage1Instances.THMM0122.FaltingsTarget` in `Statement.lean`. It uses native
`SmoothOfRelativeDimension 1`, native geometric connectedness, concrete
projectivity via a closed immersion into finite projective space, concrete
structure-sheaf `H^1`, and rational points as sections. `statement.json`
freezes its expression and environment fingerprints. `rationalPointEquivOver`
and `faltingsTarget_iff_over` check the required slice-category point
encoding.

Pinned mathlib has no native geometric-genus or K-linear cohomology finrank API
for a general curve. `HasGeometricGenus K X n` instead requires a concrete
additive equivalence between `H^1(X, O_X)` and `K^n`. This is derived from
the actual scheme, unlike a free genus parameter. The standard K-linear
comparison remains disclosed M3 normalization debt and no proof evidence.

The dated `StatementProbe.lean` and `statement-blocker.md` are historical
boundary evidence. Their conclusion that no statement artifact could be
created is superseded by the repository's explicit semantic-interface policy
used here; they remain useful evidence that a native genus API is unavailable.

The anchor inventory checks pinned mathlib representation, Northcott, and
descent support and finds no terminal Faltings declaration. Its only direct
external name match is
`facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50`;
that declaration has a materially different `Q`-only curve encoding and ends
in `by sorry`, so it receives no proof credit. `anchor-audit.json` and
`external-anchor-snapshot.json` preserve the exact bounded evidence and search
limits. The empty `dependency-reuse-ledger.json` records the authoritative v2
closure; emptiness is not a mathematical independence claim.

## Open task DAG

1. `S56-M-0122-STATEMENT`: worker-self-tested, pending master acceptance.
2. `S56-M-0122-ANCHOR_AUDIT`: bounded candidate inventory worker-self-tested,
   pending master acceptance; the separate primary-source H0 audit remains open.
3. `S56-M-0122-OBLIGATION_TREE`: freeze typed proof, provenance, trust,
   evidence, documentation, and workflow graphs.
4. `S56-M-0122-PROOF`: provide genuine terminal proof bodies or pinned imports.
5. `S56-M-0122-VALIDATION`: run exact-type, kernel, trust, provenance,
   composition, and replay checks.
6. `S56-M-0122-RELEASE`: reconcile accepted evidence and decide completion.

`statement-validation.md` records the statement checks and fingerprints.
`validation.md` remains the historical intake validation record. Neither
surface claims a proof, accepted receipt, audit completion, or theorem
completion.
