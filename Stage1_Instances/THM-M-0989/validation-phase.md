# THM-M-0989 validation-phase evidence

Item: `S56-M-0989-VALIDATION`. Base revision:
`64ac616628d97140f9ca64eff0298e51d7f4e9ff`; base tree:
`9ef0acd5b747e34cacb82c6f21fce1e1380e0cf2`.

## Validation scope

The structured recipe copies the six proof modules and `Validation.lean` into
temporary output space and invokes the pinned Lean kernel with `--trust=0`.
Every Lean subprocess runs with a cleared, fixed environment inside a
Bubblewrap network namespace. `Validation.lean` separately writes the final
`TendstoInDistribution` composition through Levy, but deliberately reuses the
proof phase's measurability and characteristic-function packages. It is a
same-worker differential composition check, not a second proof body or a
distinct-runner attestation.

All 20 proof declarations and five validation declarations report exactly
`propext`, `Classical.choice`, and `Quot.sound`. Five parser-aware
`assert_no_sorry` probes pass. A Lean environment traversal from the exact root
and validation root visits 53,251 declarations in 1,748 modules and reports no
unsafe or unexpected bodyless declarations. The validator additionally binds
the frozen local inputs, proof receipt, obligation denominator, mathlib
revision/tree/remote/license, three selected source/blob/olean boundaries, and
the Lean, Lake, Python, Git, and Bubblewrap executable hashes.

## Commands and results

Commands ran from this worker clone on 2026-07-14 (Asia/Shanghai). The
automation-provided pinned `.lake` symlink was reused without update, build,
clone, fetch, checkout, or dependency mutation.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0989
  exit 0: rank 269, planned L0/rework-required target; theorem_complete=false

python3 Stage1_Instances/THM-M-0989/check_obligation_tree.py
  exit 0: 15 frozen obligations, 32 typed edges, denominator
  c5d0b41c35c0759e11055611925021d6c2e38fc251da666e8f3afe238eccdc15;
  the frozen pre-proof graph remains open M3

bash Stage1_Instances/THM-M-0989/check_proof.sh
  exit 0: six isolated modules elaborated with --trust=0; 20 declarations
  reported exactly [propext, Classical.choice, Quot.sound]

bash Stage1_Instances/THM-M-0989/check_validation.sh
  exit 0: network-isolated six-module replay plus final-composition replay;
  25 exact axiom reports, five sorry-free reports, transitive closure
  declarations=53251/modules=1748, bodyless_nonaxioms=[], unsafe=[]; stdout
  SHA-256 47e7da7d5a35db51457fdab155597111541d9e8c4391678497b03ec81880e63a

python3 -I -B Stage1_Instances/THM-M-0989/check_validation.py
  exit 0: target/DAG identity, hashes, proof boundary, hygiene, selected
  trust/provenance, recipe, receipt, and worker packet passed; authority and
  release gates remained fail-closed

python3 -m json.tool Stage1_Instances/THM-M-0989/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0989/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-m0989-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0989/check_validation.py
  exit 0: validator compiled outside the repository tree

python3 -I -B Stage1_Instances/THM-M-0989/check_validation.py
  internal comment-aware source scan: no sorry, admit, sorryAx, native_decide,
  implemented_by, extern, axiom, constant, opaque, or unsafe construct found

git diff --check -- Stage1_Instances/THM-M-0989 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics; validator text-hygiene assertions covered
  the untracked artifacts
```

The proof-phase `check_proof.py` is snapshot-bound to the earlier proof worker
packet, so it is not a current validation recipe after this phase replaces the
root self-test packet. This validation executes the checker structurally,
binds the proof receipt by hash, and directly replays `check_proof.sh`; the
integration lane must separately bind and review the self-hash-excluded
checker. It does not misreport the stale worker-packet expectation as a proof
failure.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel and composition replay | provisional pass | The six proof modules, exact frozen root, and separately written final composition elaborate with `--trust=0` and denied network. |
| Placeholder, bodyless, and unsafe boundary | provisional pass | Parser-aware sorry probes, comment-stripped source scans, and the machine-derived transitive closure found no prohibited mechanism. |
| Trust observation | provisional pass | All checked declarations report exactly the three classical axioms; no accepted versioned foundation profile or complete TCB inventory exists. |
| Selected provenance | provisional pass | Frozen hashes and three material mathlib source/blob/olean boundaries, clean revision/tree, remote, license, and tool identities agree; full transitive supply-chain/SBOM closure remains absent. |
| Structured authority | fail closed | `S56-M-0989-PROOF` is only `[_]`; accepted state remains H2/M3/R4 and the frozen graph accepts no proof receipt. |
| Canonical target fingerprint | fail closed | `intake.json` still has a null `elaborated_expression_hash`; validation may not invent one or rewrite an earlier phase. |
| Hermetic release replay | fail closed | Shared warm `.lake`; no separate immutable clean checkout, empty-cache cold bootstrap, content-addressed offline restoration, or deterministic TCB/SBOM bundle. |
| Independent verification | fail closed | The differential composition shares analytic bodies, this worker, checkout, kernel, and cache; there is no distinct identity, independently provisioned runner, second signature, or independent minimal release verifier. |

The first failed node gate is
`dependency.S56-M-0989-PROOF.master_acceptance`; the first failed release gate
is `S56-10.6-HERMETIC-COLD-BUILD`. Primary-source H0, independently reviewed
R0, accepted foundation/trust/provenance, `AUDIT-Z`, `THEOREM-Z`, release, and
theorem completion remain false. This self-tested worker evidence claims no
release-grade `E0/E1`, accepted `M0-L`, independent verification, release, or
master acceptance.
