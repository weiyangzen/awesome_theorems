# THM-M-0415 release decision handoff

## Exact verdict

`S56-M-0415-RELEASE` is `blocked`. Lifecycle remains `planned`, accepted root state remains
`[H2, M3, R4]`, and both `audit_complete` and `theorem_complete` are false. There are no accepted
receipt IDs. The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: validation is provisional
worker evidence (`[_]`), not a master-accepted prerequisite (`[x]`).

## Evidence reconciliation

The narrow validation receipt supports a provisional `M0-W` candidate. The exact statement and
both exact-root routes elaborate without placeholders through pinned mathlib's class-number
construction; observed axioms are `propext`, `Classical.choice`, and `Quot.sound`. This does not
promote accepted machine state. The frozen graph still records root `M3`, has no proof-evidence
edges, and leaves `M0415-X-PROVENANCE` and `M0415-X-SOURCE` in the root cut set.

`AUDIT-Z` is false. There is no accepted pinpoint primary-source `H0` crosswalk with independent
source review, and required readable nodes have no accepted structured `R0` reconstruction with
independent reader review.

Even after dependency acceptance, `THEOREM-Z` fails section 10.6. Existing checks reuse the shared
warm `.lake` cache and provide no immutable empty-cache network-denied cold build, offline archive
replay, complete transitive TCB/SBOM/license closure, independently provisioned clean runners, two
signed attestations, independently implemented minimal verifier, protected CI, or deterministic
release bundle.

## Self-test

Run from repository root without dependency update, build, fetch, or clone:

```text
python3 Stage1_Instances/THM-M-0415/check_release.py
  exit 0
  ok: upstream narrow Lean validation replayed against pinned Lean/mathlib
  ok: provisional exact-root M0-W candidate evidence reconciled without promotion
  open: H0/R0 and frozen source/provenance reconciliation; AUDIT-Z is false
  blocked: dependency acceptance, hermetic, supply-chain, independent-verifier, and bundle gates
  verdict: blocked; lifecycle planned; theorem_complete=false; no accepted receipts
```

The checker replays `check_validation.py`, which invokes `lake env lean` on temporary copies of the
three narrow Lean modules. It also verifies content-addressed inputs, the provisional dependency
status, false terminal decisions, and the frozen source/provenance cut set. This is a self-tested
negative release decision, not release-grade evidence or master acceptance.
