# Machine-checked audit — S5-CLM-00003535

## Root and environment

The root is the Boshernitzan proposition from the frozen member record.  The
crosswalk records equal source and target elaborated-expression digests,
provider revision, source-file and declaration digests, and the complete
transitive constant census.  The census is intentionally conservative: every
non-foundation item is required to be re-bound by Master against its pinned
provider source before acceptance.

`machine-closure.json` reports `M0-L` as a worker-level closure claim.  Its
empty cut set and trust value zero describe the intended replay boundary, not
a self-attested replacement for the canonical kernel trace.  The declaration
census and dependency edges are retained so a cold from-source Master replay
can reject any omitted edge or body hash.

## Forbidden evidence

The provider's `sorryAx` is explicitly excluded from observed axioms.  The
three Lean artifacts contain no `sorry`, `admit`, `axiom`, unsafe declaration,
or opaque oracle.  The required provider-module spelling appears only in the
provenance comments; the executable import is `Mathlib`, as mandated for the
numeric FormalConjectures path.

## Replay obligations

Master must compile each artifact at trust zero from a cold source tree,
recompute the root expression and each transitive declaration's type/body,
run semantic-import and local-shadow mutations, and bind those traces to the
release receipt.  Any mismatch invalidates this worker handoff.
