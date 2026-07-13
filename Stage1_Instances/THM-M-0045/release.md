# THM-M-0045 release decision

Item `S56-M-0045-RELEASE` has the exact verdict **blocked**. The lifecycle remains `planned`, the
accepted root vector remains `H1/M3/R4`, and both `AUDIT-Z` and `THEOREM-Z` are blocked.
`theorem_complete` remains false and there are no accepted receipt IDs. This is a self-tested
negative release reconciliation, not theorem completion, release, or master acceptance.

## Evidence reconciliation

The current-pin `SchurPort.lean` and `Proof.lean` replay the exact finite complex Schur
triangularization target against pinned Lean 4.29.0 and mathlib `8a178386`. Both proof declarations
are sorry-free and report only `propext`, `Classical.choice`, and `Quot.sound`. A supplemental scan
finds no placeholder, bodyless axiom/constant, unsafe, opaque, native, external, or implementation
escape in the five scoped Lean modules. This is useful provisional local-proof evidence, not
accepted `M0-L` or release evidence.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the validation receipt is worker-tested,
explicitly non-release-grade, and not master accepted. The authoritative instance and typed graph
still record `H1/M3/R4`, `root_closed=false`, and no accepted obligations or receipts. The proof
receipt lists all 31 required machine IDs as closed, but its own cut set and known failures keep
`M0045-S-FOUNDATION` open. It accepts none. The weaker accepted state wins until the integration
lane re-elaborates the exact proof and reconciles this foundation and per-obligation conflict.

The validation receipt is historical phase evidence, not a current release recipe. It binds the
pre-integration revision `eb9c2192`, describes then-untracked validation files, and its validator
expects the validation-phase root packet. This release check therefore independently replays the
Lean proof and verifies the integrated receipt hashes rather than falsely claiming the old
phase-specific validator passes unchanged at this release snapshot.

`AUDIT-Z` is unavailable because accepted source, evidence, provenance, trust, readability, and
debt reconciliation does not exist. The root remains `H1` without a pinpoint source packet and
independent source review, and `R4` without a complete node-by-node reconstruction and independent
reader review. Complete transitive declaration provenance, theorem-specific foundation/axiom
policy, and executable/bootstrap TCB closure are also absent.

The first missing release-specific gate is `S56-10.6-HERMETIC-COLD-BUILD`. Existing checks reused
the canonical warm `.lake` artifacts; there is no immutable empty-cache network-denied cold build,
offline restoration, complete SBOM/license archive, two signed independently provisioned runners,
independently implemented minimal verifier, protected adversarial CI evidence, or deterministic
content-addressed release bundle.

## Validation

Commands run from base revision `0d2c3bdcd192266bc255ac3d5186da604517145a` on 2026-07-13 used
the existing pinned Lean artifacts read-only. No `lake update`, `lake build`, dependency clone/fetch,
or `.lake` mutation was run.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: all 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1 through 1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0045
  exit 0: rank 1085 remains planned and theorem_complete=false

python3 -B Stage1_Instances/THM-M-0045/check_release.py
  exit 0: exact local Schur root re-elaborated with the pinned toolchain;
  blocked verdict, unchanged H1/M3/R4 state, and complete release cut set agree

python3 -m json.tool Stage1_Instances/THM-M-0045/release-decision.json
  exit 0: release decision is valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-m0045-release-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0045/check_release.py
  exit 0: release checker compiles without writing generated files under the owned path

git diff --check -- Stage1_Instances/THM-M-0045 .stage1-worker-selftest.json
  exit 0: no tracked whitespace diagnostics; the release checker validates new-file whitespace
```

Retry requires dependency-ordered master acceptance and authoritative 31-obligation reconciliation,
including resolution of the contradictory `M0045-S-FOUNDATION` classification,
then audit closure, independent H0/R0 review, complete transitive provenance and TCB records, an
immutable cold offline-capable release build, supply-chain closure, independent verification, and
a deterministic evidence bundle accepted by the master lane.
