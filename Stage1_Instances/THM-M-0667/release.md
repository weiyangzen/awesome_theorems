# THM-M-0667 release decision handoff

## Exact verdict

`S56-M-0667-RELEASE` is **blocked**. Lifecycle remains `planned`, the accepted root vector remains
`[H1, M3, R3]`, and both `audit_complete` and `theorem_complete` are false. No receipt is accepted;
neither `AUDIT-Z` nor `THEOREM-Z` is claimed.

The first release-node failure is
`dependency.S56-M-0667-VALIDATION.master_acceptance`: validation is provisional worker evidence,
explicitly `release_grade=false`, and not master accepted. Within that validation packet, proof
master acceptance is the earlier prerequisite failure. The first intrinsic release gate failure is
`S56-10.6-HERMETIC-COLD-BUILD`.

## Evidence reconciliation

The exact target `Not (Primrec2 Nat.ack)` has genuine narrow kernel evidence. `Proof.lean` wraps
`Nat.not_primrec\u2082_ack` from pinned mathlib, while `Validation.lean` independently reconstructs the
same root from `exists_lt_ack_of_nat_primrec` without importing the proof wrapper. Both routes report
exactly `propext`, `Classical.choice`, and `Quot.sound`. The scoped placeholder scan passes. This
supports a provisional `M0-W` candidate, not an accepted machine state or theorem release.

The frozen graph predates proof closure: its root is `M3`, all evidence-ID lists are empty, every
node is `R3`, and its cut remains `M0667-N-DOMINATION`, `M0667-X-FOUNDATION`, and
`M0667-X-SOURCE`. It also provisionally calls six pinned-mathlib or local nodes `M0-P`, although
rev-5.6 reserves pinned-mathlib closure for `M0-W`. Those labels have no accepted receipts and are
not inherited. The weaker structured state wins.

There is also an unresolved provenance identity conflict. `anchor-audit.json` associates mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`45f646944c0fd7714ee56066e03bb230b49c5940`; the pinned checkout reports root tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The validation checker authenticates the latter but
does not reconcile the stale anchor field.

`H0` is open: repository metadata does not fix a normalization, and the 1928 original Ackermann
function has no accepted transport to the selected two-variable Ackermann-Peter equations, pinpoint
theorem/premise/errata mapping, or independent review. `R0` is open because there is no independently
accepted node-by-node reconstruction. Complete transitive provenance/TCB closure, enforced network
denial, immutable empty-cache cold and offline replay, SBOM/licenses, two independently provisioned
signed attestations, an independent minimal verifier, protected adversarial CI, and a deterministic
release bundle are absent.

## Validation

Commands ran from base revision `c45f3c7090cb4adf616d45e5414985f956e807b2` on 2026-07-14 in
`Asia/Shanghai`, using the existing pinned Lean artifacts without mutation:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0667
  exit 0: rank 711 remains planned and theorem_complete=false

python3 -B Stage1_Instances/THM-M-0667/check_validation.py
  exit 0: exact proof and differential roots elaborated; observed axioms matched;
  structured state reported STALE and hermetic/independent gates reported BLOCKED

python3 -B Stage1_Instances/THM-M-0667/check_release.py
  exit 0: hashes, target authority, dependency boundary, stale graph/provenance blockers,
  exact-root replay, blocked verdict, and false terminal decisions agreed

python3 -m json.tool Stage1_Instances/THM-M-0667/release-decision.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-0667 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

No `lake update`, `lake build`, dependency clone/fetch, network operation, or `.lake` mutation was
performed. The pre-existing untracked `.lake` symlink is excluded from changed paths and is not
release evidence. This handoff self-tests a truthful negative decision only. Retry requires
dependency-ordered master acceptance and graph/provenance reconciliation, then accepted audit,
source, readability, trust, hermetic, supply-chain, independent-verifier, and deterministic-bundle
evidence.
