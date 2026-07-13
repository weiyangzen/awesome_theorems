# THM-M-1143 release decision

Item `S56-M-1143-RELEASE` has the exact verdict **blocked**. The authoritative lifecycle remains
`planned`; no receipt is accepted; `AUDIT-Z`, `THEOREM-Z`, and `theorem_complete` remain false. This
is a self-tested negative release reconciliation, not theorem completion or master acceptance.

## Evidence reconciliation

The first failed node gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`. The validation prerequisite is only
`[_]` worker evidence: its receipt is provisional, `accepted=false`, `release_grade=false`, and has
no dependency-ordered master acceptance. The intake-era authority therefore remains `H4/M4/R4`
with no accepted proof state. Stronger provisional proof and validation evidence classifies the
open root as `H4/M3/R4`, but cannot silently promote authoritative state.

The first failed theorem gate is exact root kernel closure. The checked proof bodies genuinely
establish bounded-range normalization, the reciprocal-radius limit, zero-derivative constancy, and
conditional composition. They do not inhabit `InteriorGradientEstimatePackage`. The missing
arbitrary-positive-dimensional interior gradient estimate `M1143-L-GRADIENT` is the minimal
mathematical root cut, so the exact root remains `M3`.

`AUDIT-Z` is unavailable independently of the proof gap. The exact statement has no primary-source
edition, theorem/page, assumptions, proof, errata crosswalk, or independent `H0` review. There is
also no accepted `R0` reconstruction, current graph reconciliation, or complete terminal-body,
foundation, computation, provenance, and TCB closure.

The first release-specific failure is immutable clean input, followed by
`S56-10.6-HERMETIC-COLD-BUILD`. The narrow replay uses the automation-provided shared warm pinned
`.lake` artifacts. No empty-cache network-denied cold build, offline restoration, complete
SBOM/license archive, two qualifying signed attestations, independently implemented minimal
verifier, protected adversarial CI, or build-twice deterministic content-addressed bundle exists.

## Validation

The release checker binds the manifest, DAG, frozen statement/registry/graphs, proof and validation
receipts, blocker records, pinned toolchain, and mathlib revision. It scans the four Lean modules for
prohibited proof devices and replays them at trust zero under bubblewrap with networking unshared.
It checks that the nine observed declarations depend only on `propext`, `Classical.choice`, and
`Quot.sound`, while preserving the open-root boundary.

```text
python3 -I -B Stage1_Instances/THM-M-1143/check_release.py
  exit 0
  release-decision: ok (blocked at validation dependency acceptance)
  narrow Lean replay: ok (warm-cache trust-zero; exact root remains open M3)
  authoritative vector: H4/M4/R4 unchanged; best provisional vector: H4/M3/R4
  AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]
  first mathematical cut: M1143-L-GRADIENT
```

No dependency update, build, clone, fetch, or `.lake` mutation is part of this check. Retry requires
a placeholder-free proof or immutable compatible exact integration for `M1143-L-GRADIENT`, primary
source identity, accepted graph/provenance reconciliation, and all independent release gates listed
in `release-decision.json`.

