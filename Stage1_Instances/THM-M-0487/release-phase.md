# THM-M-0487 release-phase reconciliation

Item: `S56-M-0487-RELEASE`

Base revision: `5134bae303d5f5104698e8c96d7af4c26306eb47`

Base tree: `54e4bd2793df37c5451b86659fbd95a83504c25a`

## Exact Verdict

The release verdict is **blocked**. The authoritative lifecycle stays `planned`, the root vector
stays `[H1, M3, R3]`, `audit_complete=false`, and `theorem_complete=false`. No receipt, obligation,
release gate, or state transition is accepted by this worker.

The first item gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`. `S56-M-0487-VALIDATION` is only
provisional `[_]` evidence: its verdict is blocked, it is neither accepted nor release-grade, and it
has no dependency-ordered master acceptance. The exact-root failure is stronger than an assurance-
only gap: neither `M0487-T-ANALYTIC` nor `M0487-T-FINITE-UPPER` has a terminal proof body. Their
conditional composers and finite-count reformulations do not discharge either premise.

## Reconciled Evidence

All target-local theorem and evidence inputs listed in `reconciled_inputs` remain byte-identical at
this base.
The receipt itself is bound to its pre-integration base, however, and its recorded checker now
correctly rejects the current authoritative snapshot. That is freshness failure, not proof input
drift. This release checker therefore does not misreport the stale predecessor recipe as passing.

Instead, the release recipe freshly rebuilds same-worker temporary outputs for `Statement.lean`,
`ObligationTree.lean`, `Proof.lean`, and `Validation.lean` with pinned `lake env lean --trust=0`.
It verifies the exact statement, seven obligation-tree interface/composition declarations, and two
sorry-free finite-count interfaces. The interfaces report exactly `propext`, `Classical.choice`,
and `Quot.sound`, but prove no count positivity and close zero accepted frozen obligations.

## Commands And Results

No `lake update`, `lake build`, dependency clone/fetch, network request, or `.lake` mutation was
performed. The automation-provided pinned `.lake` symlink was reused read-only. The checker runs in
a network namespace with the host read-only and writes fresh target outputs only under private
`/tmp`; this remains warm-cache, nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0487` | 0 | rank 1366; planned; legacy artifacts unaccepted; theorem incomplete |
| exact `argv` from `release-spec.json` | 0 | current authority, evidence hashes, open cuts, fail-closed gates, pinned tools, prohibited constructs, and fresh partial-scope Lean replay agreed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0487-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0487/check_release.py` | 0 | checker compiled without writing generated files in the owned path |
| `python3 -m json.tool` on the release spec, decision, receipt, and worker packet | 0 | all four JSON artifacts parsed |
| comment-stripped prohibited-device scan in `check_release.py` | 0 | no `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe/opaque declaration, native proof escape, external implementation, or equivalent device occurs in the four replayed Lean modules |
| `git diff --check -- Stage1_Instances/THM-M-0487 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Remaining Gates

After dependency acceptance, the minimal machine cut remains `M0487-T-ANALYTIC` and
`M0487-T-FINITE-UPPER`. Primary-source H0, independently reviewed R0, accepted exact-root M0/E1,
complete provenance/foundation/TCB and SBOM/license closure, immutable clean input, cold empty-cache
offline reproduction, two distinct signed runners, an independently implemented minimal verifier,
protected adversarial CI, a deterministic content-addressed bundle, and master reconciliation all
remain open. This negative reconciliation is not theorem completion.

## Retry Condition

Implement or immutably integrate both open range packages without placeholders, including complete
finite data, certificates, and a kernel-sound checker replay. Compose and master-accept the exact
root and refresh all recipes. Only then can the remaining source, readability, trust, hermetic,
independence, supply-chain, deterministic-bundle, and master-release gates be attempted.
