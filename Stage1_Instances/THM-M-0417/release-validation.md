# THM-M-0417 release decision handoff

## Exact verdict

`S56-M-0417-RELEASE` is `blocked`. Lifecycle remains `planned`, accepted root state remains
`[H1, M3, R3]`, and both `audit_complete` and `theorem_complete` are false. There are no accepted
receipt IDs. The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: validation is provisional
worker evidence (`[_]`), not a master-accepted prerequisite (`[x]`).

## Evidence reconciliation

The narrow validation receipt supports a provisional `M0-W` candidate for the exact strict
Minkowski root. The statement, three-child composition, proof root, canonical transports, and a
separately written same-workspace root elaborate without placeholders against pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. Their observed axioms are `propext`,
`Classical.choice`, and `Quot.sound`. The wrapper and composition share the audited terminal bodies
and receive no duplicate proof credit.

This does not promote accepted machine state. The structured intake and public surfaces remain
planned at `H1/M3/R3`, retain pre-proof or pre-validation fields, and the typed evidence graph does
not bind the proof and validation receipts. Reconciliation of those authoritative surfaces is a
master action.

`AUDIT-Z` is false. `M0417-X-SOURCE` remains `H1`, without an accepted primary-source edition,
theorem/page pinpoint, premise and errata crosswalk, or independent source review. Required readable
nodes remain `R3`, without a complete section-8 reconstruction or independent reader acceptance.
`M0417-X-TRUST` also remains open: the foundation profile is uninstantiated and the full transitive
declaration, imported-object, executable TCB, compiler/bootstrap, SBOM, and license closure is absent.

Even after dependency acceptance, `THEOREM-Z` fails section 10.6. Existing validation uses canonical
warm `.lake` artifacts and provides no immutable empty-cache network-denied cold build, offline
archive replay, independently provisioned clean runners, two signed attestations, independently
implemented minimal verifier, protected CI, P0 mutation/metamorphic gate evidence, or deterministic
release bundle. The pre-existing `.lake` symlink was not modified and is explicitly nonrelease input.

## Self-test

Run from repository root without dependency update, build, fetch, or clone:

```text
python3 Stage1_Instances/THM-M-0417/check_release.py
  exit 0
  ok: upstream narrow Lean validation replayed against pinned Lean/mathlib
  ok: provisional exact-root M0-W candidate evidence reconciled without promotion
  open: M0417-X-SOURCE, M0417-X-TRUST, H0/R0, and stale structured state; AUDIT-Z is false
  blocked: dependency acceptance, hermetic, supply-chain, independent-verifier, and bundle gates
  verdict: blocked; lifecycle planned; theorem_complete=false; no accepted receipts
```

The checker content-addresses the frozen release inputs and replays `check_validation.py`, whose
temporary-directory recipe invokes only `lake env lean` against the existing pinned artifacts. It
also verifies the provisional dependency and root evidence, exact open boundary, planned authority,
stale typed evidence graph, false terminal decisions, and complete negative cut set. This is a
self-tested negative release decision, not release-grade evidence or master acceptance.
