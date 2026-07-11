# THM-M-0420 release decision handoff

## Exact verdict

`S56-M-0420-RELEASE` is **blocked**. Lifecycle remains `planned`, the accepted root vector remains
`[H1, M3, R3]`, and both `audit_complete` and `theorem_complete` are false. No receipt is accepted
and this worker makes no theorem-completion promotion.

The first failed workflow gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: validation has only
provisional worker evidence (`[_]`), not master acceptance (`[x]`). Independently, the first failed
theorem gate is exact-root kernel closure. `M0420-C` and `M0420-L1` through `M0420-L4` have no proof
bodies, so the checked conditional composition does not prove the Hilbert class field theorem.

## Evidence reconciliation

The exact statement and conditional `root_composition` elaborate against pinned Lean
4.29.0/mathlib. `M0420-N1`, a normalization lemma for finite-prime unramifiedness, has a real local
placeholder-free proof body; Lean reports `propext`, `Classical.choice`, and `Quot.sound`. This is
not a construction of the field, abelian Galois proof, global Artin reciprocity proof, maximality
proof, or complete unramifiedness proof. The frozen graph also predates this leaf proof and has not
been reconciled by the master.

`AUDIT-Z` is false because the primary-source boundary remains `H1`, readability remains `R3`, and
the source, graph, provenance, and trust inventories lack accepted independent reviews and closure.
`THEOREM-Z` additionally lacks a clean immutable snapshot, empty-cache network-denied cold build,
offline archive replay, complete TCB/SBOM/license closure, two independently provisioned signed
runners, an independently implemented minimal verifier, protected CI, and a deterministic release
bundle. The untracked shared `.lake` symlink is explicitly nonrelease input.

## Self-test

Run from the repository root without update, build, clone, fetch, or dependency mutation:

```text
python3 Stage1_Instances/THM-M-0420/check_release.py
  exit 0
  ok: upstream narrow Lean validation replayed against pinned Lean/mathlib
  ok: M0420-N1 evidence and the five-obligation open root cut were reconciled without promotion
  open: exact Hilbert class field root remains M3; AUDIT-Z is false
  blocked: dependency acceptance, root closure, H0/R0, hermetic, and independent-verifier gates
  verdict: blocked; lifecycle planned; theorem_complete=false; no accepted receipts
```

The checker content-binds the inspected phase artifacts and replays `check_validation.py`, whose
temporary narrow module check invokes only `lake env lean` using the existing pinned artifacts.
This is a self-tested negative release decision, not release-grade evidence or master acceptance.
