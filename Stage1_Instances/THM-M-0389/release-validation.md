# THM-M-0389 release decision handoff

## Exact verdict

`S56-M-0389-RELEASE` is **blocked**. The lifecycle remains `planned`, the accepted root vector
remains `[H4, M3, R3]`, `audit_complete=false`, and `theorem_complete=false`. There are no accepted
receipt IDs and no theorem-completion promotion.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the validation prerequisite is only `[_]`
worker evidence with `support_state=provisional_worker_selftest`. It has not been accepted by the
master. The first additional release-assurance failure is `S56-10.6-HERMETIC-COLD-BUILD`.

## Reconciliation

The strongest provisional evidence is materially better than the accepted projection: the exact
root declaration elaborates from a repo-local proof body and reports only `propext`,
`Classical.choice`, and `Quot.sound`. The independently spelled exact-type probe agrees. This is
warm-cache, same-checkout worker evidence for provisional `M0-L`; it is not accepted release
evidence. `instance.json` and `proof-units.json` still retain pre-proof debt projections.

`AUDIT-Z` is not established. The source audit remains `H4`: its Markoff citation is only a
bibliographic lead without an accepted edition/page/theorem/assumption/errata crosswalk. The
readable surface remains `R3` and has no independent `R0` review. Full transitive provenance and TCB
closure are also absent.

`THEOREM-Z` additionally lacks an immutable clean release snapshot, empty-cache network-denied cold
build, offline archive restoration, SBOM/licenses, two separately provisioned signed attestations,
an independently implemented minimal verifier, protected CI and mutation gates, and a deterministic
content-addressed release bundle. The shared pinned `.lake` symlink was reused and not mutated; that
is valid narrow worker validation, but not section 10.6 release reproduction.

## Self-test

Commands run from base revision `304123cb0513eac404230aea1ab7c608db1cb55e` on 2026-07-12:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups; 1546 uniform-L0 targets; execution skill present

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0389
  exit 0: rank 20; lifecycle planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0389/check_release.py
  exit 0: validation replay passed; blocked dependency and all negative terminal decisions agree

python3 -m json.tool Stage1_Instances/THM-M-0389/release-decision.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-0389 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

`check_release.py` invokes the recorded narrow validator, which recompiles `Proof.lean` and the
exact-type probe with `lake env lean` against the existing pinned toolchain. No `lake update`, `lake
build`, dependency fetch, clone, or `.lake` mutation was performed.

## Retry boundary

The integration lane must first accept and reconcile the proof and validation dependency chain. A
separately provisioned release lane must then close the H0/R0 reviews, transitive trust and
provenance, hermetic and independent reproduction, supply-chain and CI gates, and deterministic
bundle verification. Only the master may accept the terminal decision.
