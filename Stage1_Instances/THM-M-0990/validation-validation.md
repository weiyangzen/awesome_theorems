# THM-M-0990 validation-phase evidence

Item: `S56-M-0990-VALIDATION`. Base revision:
`a1a7e939e58f103f5ff5d23af51437fa8658aa04`; base tree:
`d881fd9641fa3e5f3ebe5082b35672981e90adcf`.

## Validation scope

The structured recipe copies the four `THM-M-0989` dependency modules, the
five `THM-M-0990` proof modules, and `Validation.lean` into temporary output
space. It invokes pinned Lean 4.29.0 with `--trust=0`. Every Lean subprocess
runs with a cleared fixed environment inside a Bubblewrap network namespace.
No dependency state is changed.

`Validation.lean` separately writes the exact `StatementShape` composition
from the normalization and analytic packages. It does not invoke
`lyapunovCentralLimit_exact`, but deliberately shares all substantive analytic
bodies. This is same-worker differential composition evidence, not a second
proof body or an independent-runner attestation.

The frozen `validation-specs.json` belongs to the earlier obligation-tree
phase. Its 18 recipes all share the same command, which elaborates only
`ObligationTree.lean`. The current replay compiles that dependency chain in a
stricter temporary environment and `check_obligation_tree.py` checks all 18
recipe-to-node links. Those recipes therefore pass only for their recorded
conditional architecture scope; they are not reinterpreted as later proof
closure. `validation-phase-spec.json` adds the proof-root validation surface.

All 24 proof declarations and six validation declarations report exactly
`propext`, `Classical.choice`, and `Quot.sound`. Six parser-aware
`assert_no_sorry` probes pass. A Lean environment traversal from the proof and
validation roots visits 53,310 declarations in 1,752 modules and reports no
unsafe or unexpected bodyless declaration. The validator also binds the
statement, frozen obligation denominator, stale-but-truthful typed-graph
boundary, proof receipt, cross-target `THM-M-0989` source hashes, mathlib
revision/tree/remote/license, six selected source/olean boundaries, and the
Lean, Lake, Python, Git, and Bubblewrap executable identities.

## Commands and results

Commands ran from this worker clone on 2026-07-15 (Asia/Shanghai). The
automation-provided pinned `.lake` symlink was reused without update, build,
clone, fetch, checkout, or dependency mutation.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0990
  exit 0: rank 270, planned L0/rework-required target; theorem_complete=false

python3 Stage1_Instances/THM-M-0990/check_obligation_tree.py
  exit 0: 18 frozen obligations, 43 typed edges, denominator
  fa799ae86623298ad54105d2041f7903144cc398f769b7da7a3865507a9921f6;
  the frozen pre-proof graph remains open M3

bash Stage1_Instances/THM-M-0990/check_validation.sh
  exit 0: network-isolated nine-module dependency/proof replay plus separate
  final-composition replay; 30 exact axiom reports, six sorry-free reports,
  transitive closure declarations=53310/modules=1752,
  bodyless_nonaxioms=[], unsafe=[]

python3 -I -B Stage1_Instances/THM-M-0990/check_validation.py
  exit 0: target/DAG identity, hashes, proof boundary, hygiene, selected
  trust/provenance, recipe, receipt, and worker packet passed; authority and
  release gates remained fail-closed

python3 -m json.tool Stage1_Instances/THM-M-0990/validation-phase-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0990/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-m0990-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0990/check_validation.py
  exit 0: validator compiled outside the repository tree

git diff --check -- Stage1_Instances/THM-M-0990 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics; validator text-hygiene assertions also
  covered all untracked output files
```

The proof-phase `check_proof.py` is snapshot-bound to an earlier proof worker
packet and is not a valid current validation recipe after this phase replaces
the root self-test packet. Validation instead hash-binds that checker and the
proof receipt, checks their structured boundary, and directly replays the Lean
modules under a new network-isolated runner.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel and composition replay | provisional pass | The complete dependency/proof module chain, exact frozen root, and separately written final composition elaborate with `--trust=0` and denied network. |
| Placeholder, bodyless, and unsafe boundary | provisional pass | Parser-aware sorry probes, comment-aware source scans, and the machine-derived transitive closure found no prohibited mechanism. |
| Trust observation | provisional pass | All checked declarations report exactly the three classical axioms; no accepted versioned foundation profile or complete TCB inventory exists. |
| Selected provenance | provisional pass | Frozen local/cross-target hashes and selected mathlib source/blob/olean boundaries, clean revision/tree, remote, license, and tool identities agree. The external upstream archive was not independently restored and full transitive supply-chain closure remains absent. |
| Structured authority | fail closed | `S56-M-0990-PROOF` is only `[_]`; accepted state remains H2/M3/R4, the proof receipt is not content-addressed, and the frozen graph accepts no proof obligation. |
| Canonical target fingerprint | fail closed | `statement.json` contains no serialized elaborated-expression fingerprint; validation may not invent one or rewrite an earlier phase. |
| Hermetic release replay | fail closed | Shared warm `.lake`; no separate immutable clean checkout, empty-cache cold bootstrap, offline restoration, or deterministic TCB/SBOM bundle. |
| Independent verification | fail closed | The differential composition shares analytic bodies, this worker, checkout, kernel, and cache; there is no distinct identity, independently provisioned runner, second signature, or independent minimal release verifier. |

The first failed node gate is
`dependency.S56-M-0990-PROOF.master_acceptance`; the first failed release gate
is `S56-10.6-HERMETIC-COLD-BUILD`. Primary-source H0, independently reviewed
R0, accepted foundation/trust/provenance, `AUDIT-Z`, `THEOREM-Z`, release, and
theorem completion remain false. This worker evidence claims no release-grade
`E0/E1`, accepted `M0-L`, independent verification, release, or master
acceptance.
