# THM-M-0400 release decision

Item: `S56-M-0400-RELEASE`

## Exact verdict

The release verdict is `blocked`. The lifecycle remains `planned`, the root
vector remains `H1/M3/R3`, and both `audit_complete` and `theorem_complete`
are false. No accepted receipt ID exists.

The evidence agrees on this boundary. The selected statement has a recorded
Lean elaboration, and six declarations validate three elementary height and
integer-to-rational encoding facts. No frozen obligation is closed, however.
The central Subspace-Theorem argument, checked terminal composition, exact
source crosswalk, accepted readable reconstruction, provenance and trust
closure, and the canonical root proof are all absent.

The first failed dependency gate is `S56-M-0400-PROOF` exact-root closure and
master acceptance. Even after that is repaired, the first currently missing
release-specific gate is `S56-10.6-HERMETIC-COLD-BUILD`. There is no empty-cache
offline replay, SBOM/license closure, deterministic evidence bundle, protected
CI attestation, or distinct independently provisioned verifier. Repetition in
this worker checkout does not satisfy independent verification.

## Self-test boundary

`check_release.py` binds the intake, statement record, anchor audit, obligation
tree, proof receipt, validation receipt, and validation specifications by
SHA-256. It rejects lifecycle advancement, terminal status, accepted receipts,
or root closure, then replays the narrow validation recipes through
`check_validation.py`.

This makes the release-phase reconciliation itself self-tested and suitable
for a provisional worker `[_]` handoff. It does not make the theorem or audit
complete, does not satisfy release assurance, and does not constitute master
acceptance.
