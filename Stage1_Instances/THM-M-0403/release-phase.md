# THM-M-0403 release reconciliation

Item `S56-M-0403-RELEASE` reconciles the dossier's current provisional
receipts. The exact verdict is `blocked`: lifecycle remains `planned`, the
root remains `[H1, M4, R3]`, and both `audit_complete` and
`theorem_complete` are false. This is a tested negative release decision, not
a theorem-completion or master-acceptance claim.

## Evidence reconciliation

The validation receipt records a successful narrow replay only for the
statement and six partial or conditional declarations. It records no closed
obligation and no composition certificate. In particular,
`statement_of_finiteZeroSet` consumes the desired finite-zero-set result as a
premise; it does not close the canonical root. The frozen graph therefore
retains `M0403-L-ESS-FINITE` as the minimal open root cut.

The same receipt explicitly fails the cold empty-cache hermetic replay and
independent-verification gates. No complete TCB/SBOM/license archive, offline
restoration, deterministic release bundle, two signed attestations, distinct
clean runner, independently implemented verifier, accepted `H0`/`R0` review,
or master receipt exists. The prerequisite validation item is provisional
`[_]`, not master-accepted `[x]`.

## Exact command and result

Run from repository root with no dependency update, build, fetch, or clone:

```text
python3 Stage1_Instances/THM-M-0403/validate_release.py
  exit 0
  ok: upstream node-scoped validation replayed against pinned Lean/mathlib
  open: exact root M4; no closed obligation or composition certificate
  open: audit H1/R3; AUDIT-Z is not established
  blocked: hermetic, supply-chain, independent-verifier, and master-acceptance gates
  verdict: blocked; lifecycle planned; theorem_complete=false; cut M0403-L-ESS-FINITE
```

The release validator reruns the recorded narrow validation recipe and checks
the content hashes and negative gate fields in the proof, validation,
registry, graph, and release records. The first failed theorem-completion gate
is exact root kernel closure. Retry requires a proof of the exact frozen root
and checked composition; later release also requires accepted audit evidence,
hermetic supply-chain replay, independent verification, a deterministic
bundle, and master acceptance.
