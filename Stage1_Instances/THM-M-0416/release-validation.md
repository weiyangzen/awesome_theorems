# THM-M-0416 release decision handoff

## Exact verdict

`S56-M-0416-RELEASE` is `blocked`. Lifecycle remains `planned`, accepted root state remains
`[H1, M3, R3]`, and both `audit_complete` and `theorem_complete` are false. There are no accepted
receipt IDs. The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: validation is provisional
worker evidence (`[_]`), not a master-accepted prerequisite (`[x]`).

## Evidence reconciliation

The narrow validation receipt supports a provisional `M0-W` candidate. The exact statement,
checked package composition, proof root, and independently reconstructed root elaborate without
placeholders through pinned mathlib's Dirichlet-unit-theorem declarations. Their observed axioms
are `propext`, `Classical.choice`, and `Quot.sound`. This does not promote accepted machine state.
The frozen graph still records root `M3`, has no proof evidence IDs, and leaves all four
mathematical packages in its machine root cut set pending integration-lane reconciliation.

`AUDIT-Z` is false. The source surface remains `H1`: it has no accepted primary-source theorem/page
pinpoint, errata audit, complete node mapping, or independent source review. Readability remains
`R3`, without a complete section-8 reconstruction and independent reader acceptance.

Even after dependency acceptance, `THEOREM-Z` fails section 10.6. Existing checks reuse the shared
warm `.lake` cache and provide no immutable empty-cache network-denied cold build, offline archive
replay, complete transitive TCB/SBOM/license closure, independently provisioned clean runners, two
signed attestations, independently implemented minimal verifier, protected CI, or deterministic
release bundle. The same-workspace independent Lean proof is useful local evidence but does not
satisfy section 10.7.

## Self-test

Run from repository root without dependency update, build, fetch, or clone:

```text
python3 Stage1_Instances/THM-M-0416/check_release.py
  exit 0
  ok: upstream narrow Lean validation replayed against pinned Lean/mathlib
  ok: provisional exact-root M0-W candidate evidence reconciled without promotion
  open: H1/R3 and frozen graph reconciliation; AUDIT-Z is false
  blocked: dependency acceptance, hermetic, supply-chain, independent-verifier, and bundle gates
  verdict: blocked; lifecycle planned; theorem_complete=false; no accepted receipts
```

The checker replays `check_validation.py`, which invokes `lake env lean` on temporary copies of the
four narrow Lean modules. It also verifies content-addressed inputs, the provisional dependency
status, false terminal decisions, and the frozen four-package cut set. This is a self-tested
negative release decision, not release-grade evidence or master acceptance.
