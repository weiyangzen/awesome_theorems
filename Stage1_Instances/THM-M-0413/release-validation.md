# THM-M-0413 release decision handoff

## Exact verdict

`S56-M-0413-RELEASE` is `blocked`. Lifecycle remains `planned`, accepted root state remains
`[H1, M3, R3]`, and both `audit_complete` and `theorem_complete` are false. There are no accepted
receipt IDs. The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: validation is provisional
worker evidence (`[_]`), not a master-accepted prerequisite (`[x]`).

## Evidence reconciliation

The narrow validation receipt does support a provisional `M0-W` candidate classification. The
exact statement and two exact-root routes elaborate without placeholders through pinned mathlib's
`IsIntegralClosure.isDedekindDomain`; observed axioms are `propext`, `Classical.choice`, and
`Quot.sound`. This does not promote accepted machine state. The frozen graph still records four
open prerequisite-to-component composition edges and the open `THM-M-0413-X-TRUST` release node,
which only the integration lane may reconcile against proof receipts.

`AUDIT-Z` is also false. The source surface remains `H1`, lacking an accepted primary-source
theorem/page pinpoint, errata review, complete premise-to-node mapping, and independent source
review. Readability remains `R3`, without a complete section-8 reconstruction and independent
reader acceptance.

Even after dependency acceptance, `THEOREM-Z` fails section 10.6. Existing checks reuse the shared
warm `.lake` cache and provide no immutable empty-cache network-denied cold build, offline archive
replay, complete transitive TCB/SBOM/license closure, distinct clean runners, two signed
attestations, independently implemented minimal verifier, protected CI, or deterministic release
bundle. A same-workspace independent Lean declaration is useful local evidence but does not meet
section 10.7.

## Self-test

Run from repository root without dependency update, build, fetch, or clone:

```text
python3 Stage1_Instances/THM-M-0413/check_release.py
  exit 0
  ok: upstream narrow Lean validation replayed against pinned Lean/mathlib
  ok: provisional exact-root M0-W candidate evidence reconciled without promotion
  open: H1/R3 audit and frozen composition/trust reconciliation; AUDIT-Z is false
  blocked: dependency acceptance, hermetic, supply-chain, independent-verifier, and bundle gates
  verdict: blocked; lifecycle planned; theorem_complete=false; no accepted receipts
```

The release checker replays `check_validation.py`, which uses `lake env lean` on temporary copies of
the four narrow modules. It additionally checks content-addressed inputs, provisional dependency
status, false terminal decisions, the four open frozen composition edges, and the open trust gate.
The retry boundary is recorded structurally in `release-decision.json`.
