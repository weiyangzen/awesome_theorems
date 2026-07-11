# THM-M-0392 Release Decision Handoff

## Exact verdict

`S56-M-0392-RELEASE` is **blocked**. The lifecycle remains `planned`, the accepted root vector
remains `[H5, M4, R4]`, `audit_complete=false`, and `theorem_complete=false`. There are no accepted
receipt IDs and no theorem-completion promotion.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the validation prerequisite is `[_]`
worker evidence with `support_state=provisional_worker_selftest`, not a master-accepted dependency.
Even after dependency acceptance, `THEOREM-Z` would fail exact-root closure because
`M0392-X-SIEGEL` has no checked terminal body.

## Reconciliation

The accepted instance remains `H5` because the source text `y^2=x^3+k` with “integer solutions”
does not uniquely specify the quantification of `k`, whether the requested result is finiteness or
effective enumeration, or the necessary `k != 0` boundary. The dossier's uniform-finiteness target
is an explicit provisional interpretation, not an accepted disambiguation of the source.

Under that candidate interpretation, the proof and validation receipts give useful local kernel
evidence for three of eight frozen root-relevant obligations: curve/equation construction,
nonzero discriminant, and injective coordinate transport. The exact root remains open, as do the
Siegel integral-points bridge, finite-transfer composition into the root, source boundary, and
release trust boundary. The observed partial axiom set is `propext`, `Classical.choice`, and
`Quot.sound`; the scoped placeholder scan passes. These facts do not close the theorem.

Release evidence is absent for authoritative statement disambiguation, H0/R0 independent review,
root provenance/axiom/TCB closure, an immutable clean snapshot, empty-cache network-denied cold
build, offline archive restoration, SBOM/licenses, protected CI and mutation gates, two separately
provisioned signed attestations, an independently implemented minimal verifier, and a deterministic
content-addressed bundle. The existing independent probe ran in this checkout with the shared
pinned dependency cache and does not satisfy section 10.7.

## Self-test

Commands ran from base revision `cc9d29a4da006a94c9896124b7ef9fe253befac3` on 2026-07-12:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups; 1546 uniform-L0 targets; execution skill present

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0392
  exit 0: rank 2; lifecycle planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0392/check_validation.py
  exit 0: eight-node identity, receipt freshness, pinned provenance, three partial
  closures, fail-closed root, independent probe, and placeholder policy verified

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0392/Proof.lean
  exit 0: four local declarations elaborated; reported axioms were propext,
  Classical.choice, and Quot.sound

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0392/Validation.lean
  exit 0: three independently reconstructed declarations elaborated with the same axiom boundary

python3 Stage1_Instances/THM-M-0392/check_release.py
  exit 0: blocked decision, unaccepted dependency, source ambiguity, five open
  obligations, false terminal booleans, and release cut set agree

python3 -m json.tool Stage1_Instances/THM-M-0392/release-decision.json
  exit 0: valid JSON

rg -n '\b(sorry|admit)\b|^[[:space:]]*(axiom|unsafe)\b' \
  Stage1_Instances/THM-M-0392/{Proof,Validation}.lean
  exit 1 with empty output: pass, no prohibited local declaration or placeholder

git diff --check -- Stage1_Instances/THM-M-0392 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

No `lake update`, `lake build`, dependency fetch, clone, or `.lake` mutation was performed. The
pre-existing untracked `.lake` symlink is excluded from changed paths and is not release evidence.

## Retry boundary

The source claim must first be authoritatively disambiguated. The proof lane must then close
`M0392-X-SIEGEL` and exact root composition, and the integration lane must master-accept the full
dependency chain. A separately provisioned release lane must close H0/R0, trust/provenance,
hermetic, supply-chain, independent-runner, CI, and deterministic-bundle gates. Only the master may
accept a terminal decision.
