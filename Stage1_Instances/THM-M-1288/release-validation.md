# THM-M-1288 release decision handoff

## Exact verdict

`S56-M-1288-RELEASE` is **blocked**. Lifecycle remains `planned`; the accepted
root vector remains `[H1, M4, R3]`; `audit_complete=false`; and
`theorem_complete=false`. No receipt is accepted by this worker.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`. The validation
prerequisite is provisional `[_]` worker evidence rather than a master-accepted
receipt. Independently of that workflow failure, exact root kernel closure
fails: `M1288-T-ADMISSIBILITY` and `M1288-T-OPTIMALITY` remain explicit
unproved premises, so the best provisional machine classification is `M3`.

## Evidence reconciliation

The narrow validation supports exact statement elaboration, conditional root
composition, and bounded local bodies for domain facts, gradient transport,
and the zero-function branch. The observed axioms are `propext`,
`Classical.choice`, and `Quot.sound`; the scoped Lean sources contain no
placeholder, local axiom, or unsafe declaration. None of this supplies the
sharp analytic admissibility or least-constant optimality packages.

`AUDIT-Z` remains false because there is no accepted H0 primary-source
crosswalk or independently reviewed R0 reconstruction. Release evidence is
also absent for complete provenance/TCB closure, immutable clean input, an
empty-cache network-denied cold replay, offline restoration, SBOM/licenses,
two independent signed runner attestations, an independently implemented
minimal verifier, mutation gates, and a deterministic content-addressed
bundle. The pre-existing untracked `.lake` link classifies this worker tree as
nonrelease evidence.

## Validation record

Commands were run on 2026-07-12 from base revision
`205d13cfc35c45883410c569709a91cb34edce16`. Existing pinned `.lake` artifacts
were reused without update, build, clone, fetch, or mutation.

```text
python3 Stage1_Instances/THM-M-1288/check_release.py
  exit 0: validation replay and evidence reconciliation passed; exact root M3,
  false terminal booleans, two-obligation root cut, and blocked release verdict agree

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets at ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-1288
  exit 0: rank 459; planned; L0/rework-required; theorem_complete=false

python3 -m json.tool Stage1_Instances/THM-M-1288/release-decision.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-1288 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

Retry requires exact proof and master acceptance of both analytic packages and
the dependency chain, followed by independent H0/R0 acceptance and a separate
release lane that closes the hermetic, supply-chain, verifier, mutation,
deterministic-bundle, and master-acceptance gates. Only the integration lane
may accept the node or change authoritative task state.
