# THM-M-0452 Release Decision Handoff

## Exact verdict

`S56-M-0452-RELEASE` is **blocked**. The lifecycle remains `planned`, the accepted root vector
remains `[H1, M4, R4]`, `audit_complete=false`, and `theorem_complete=false`. There are no accepted
receipt IDs and no theorem-completion promotion.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the validation prerequisite is only
`[_]` worker evidence with `support_state=provisional_worker_selftest`, not a master-accepted
dependency. Even after dependency acceptance, `THEOREM-Z` would fail exact-root kernel closure.

## Reconciliation

The exact statement elaborates, and the local proof descends a supplied `PolarizationCore` through
the torsion quotient and proves quotient positive definiteness. This is provisional kernel evidence
for `M0452-D-WELLDEFINED` and `M0452-D-POSITIVE`. It does not construct `CanonicalHeightCore` or
`PolarizationCore`; consequently it does not inhabit `NeronTatePairingTarget`, and the root remains
`M4`. The conditional composition declaration is not exact-root closure without those inputs.

The source state remains below `H0`: no independently reviewed exact primary-source edition,
theorem/page, assumptions, errata, and complete node crosswalk exists. The readable architecture is
below `R0`: it has no independently accepted full structured reconstruction. Therefore `AUDIT-Z`
also remains blocked.

Release evidence is absent for complete root provenance and transitive TCB closure, an immutable
clean snapshot, empty-cache network-denied cold replay, offline restoration, SBOM/licenses,
protected CI and mutation gates, two separately provisioned signed attestations, an independently
implemented minimal verifier, and a deterministic content-addressed bundle. The existing exact-type
probe ran in the same checkout and shared warm cache and is not independent release verification.

## Validation boundary

The release checker reconciles the target manifest, task DAG, statement record, frozen graph,
validation receipt digest, partial closed-obligation set, terminal booleans, and remaining release
cut set. The narrow Lean validator replays the exact available partial proof. Neither check promotes
authoritative state; only the master integration lane may accept this worker handoff.

## Self-test

Commands ran from base revision `d16846c4969f0161ce4deb072fd4ba49becebb56` on 2026-07-12:

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0452` | 0 | rank 301, lifecycle `planned`, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0452/check_validation.py` | 0 | fresh temporary kernel replay passed for the statement, conditional composition, quotient proof, and exact-type probe; observed `propext`, `Classical.choice`, and `Quot.sound`; exact root remains open |
| `python3 Stage1_Instances/THM-M-0452/check_release.py` | 0 | blocked decision, unaccepted dependency, open exact root, and false terminal booleans agree |
| `python3 -m json.tool Stage1_Instances/THM-M-0452/release-decision.json` | 0 | release decision is valid JSON |
| `! rg -n '\b(sorry\|admit)\b\|^[[:space:]]*(axiom\|unsafe)\b' Stage1_Instances/THM-M-0452/{Statement,ObligationTree,Proof,Validation}.lean` | 0 | no prohibited local declaration or placeholder matched |
| `git diff --check -- Stage1_Instances/THM-M-0452 .stage1-worker-selftest.json` | 0 | no whitespace errors |

No `lake update`, `lake build`, dependency fetch, clone, or `.lake` mutation is part of this release
decision. The pre-existing untracked `.lake` symlink is nonrelease context, not changed evidence.

## Retry boundary

The proof lane must implement the canonical-height and polarization cores and exact root
composition. The integration lane must accept the dependency chain. A separately provisioned
release lane must then close H0/R0 review, trust and provenance, hermetic and independent replay,
supply-chain and CI gates, and deterministic bundle verification. Only then can `THEOREM-Z` be
reconsidered.
