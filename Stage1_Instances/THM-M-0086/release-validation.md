# THM-M-0086 release decision handoff

## Exact verdict

`S56-M-0086-RELEASE` is `blocked`. The lifecycle remains `planned`, the accepted root vector
remains `[H2, M4, R4]`, and both `audit_complete` and `theorem_complete` remain false. There are no
accepted receipt IDs and no theorem-completion promotion.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the validation prerequisite is
provisional worker evidence, not a master-accepted dependency. The first release-specific failure
is `S56-10.6-HERMETIC-COLD-BUILD`; validation reused the warm canonical `.lake` artifacts rather
than performing an immutable empty-cache network-denied cold build and offline replay.

## Reconciliation

The exact three-branch statement and root re-elaborate through three pinned mathlib terminal bodies
and local composition. A separately written same-checkout implementation reaches the same target.
Both report only `propext`, `Classical.choice`, and `Quot.sound`; scoped placeholder and unsafe scans
pass. This supports a provisional `M0-W` proposal, not accepted state. The frozen graph predates the
proof and still records `root_closed=false` with the three proof leaves open, so the weaker accepted
instance state controls pending reconciliation and master acceptance.

`AUDIT-Z` is also unavailable. The dossier retains `H2` without an independently reviewed pinpoint
primary-source crosswalk and `R4` without a unique independently reviewed reconstruction. Release
evidence is absent for complete transitive trust and TCB closure, a clean immutable snapshot,
SBOM/licenses, protected CI, two independently provisioned signed runners, an independently
implemented minimal verifier, and a deterministic content-addressed bundle.

## Self-test

Commands run from base revision `be286e95464895d6966301556151584a57536a1b` on 2026-07-12:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0086
  exit 0: rank 134; lifecycle planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0086/check_release.py
  exit 0: blocked decision and input hashes agreed; exact-root validation replay passed;
  H2/M4/R4 unchanged; AUDIT-Z=false; THEOREM-Z=false

python3 -m json.tool Stage1_Instances/THM-M-0086/release-decision.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-0086 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

No `lake update`, `lake build`, dependency clone, fetch, or `.lake` mutation was performed. Retry
requires master acceptance and typed-state reconciliation, followed by independent H0/R0 review
and a separately provisioned release lane for the hermetic, supply-chain, independent-verifier,
deterministic-bundle, and master reconciliation gates.
