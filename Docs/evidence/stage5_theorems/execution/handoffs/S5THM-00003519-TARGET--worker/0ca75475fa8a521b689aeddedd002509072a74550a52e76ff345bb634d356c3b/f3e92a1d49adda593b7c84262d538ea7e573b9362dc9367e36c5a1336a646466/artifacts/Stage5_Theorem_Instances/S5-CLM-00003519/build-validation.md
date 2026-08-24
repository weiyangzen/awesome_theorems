# Build and validation record

The frozen validator command is `complete-target-semantic-proof-debt`. It checks
the exact workset member, all 18 required files, canonical seals on the three
release-critical JSON records, exact semantic provider bindings, nonempty and
pinned transitive constants, bidirectional transports, no shadowing or semantic
substitutions, exact provider imports and declaration references, forbidden
Lean constructs, M0 closure, R0 forward/reverse coverage, strict dominance,
and trust-zero compilation of Statement, Proof, and Audit.

Lean replay uses the repository-pinned `lean-toolchain` through `elan run`, in
the canonical Lean build environment, with `LAKE_NO_CACHE=1` and `--trust=0`.
This worker records the results in `receipts/current-validation.json`; the
canonical Master must independently rerun the same frozen validator on the
integrated bytes.

Semantic-substitution negative cases cover a local definition, abbreviation,
notation, syntax, macro, namespace alias, substituted import, unqualified
source replacement, and nonempty semantic-substitution ledger. Oracle negative
cases cover `sorry`, `admit`, `axiom`, `unsafe def`, `unsafe theorem`, `opaque`,
and observed `sorryAx`. Each must be rejected before release.
