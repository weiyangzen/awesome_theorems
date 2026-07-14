# THM-M-1080 validation-phase evidence

Item: `S56-M-1080-VALIDATION`. Base revision:
`3f555cfc0879cb7c42e83d6bcf7b9e3e09997e58`; base tree:
`e8837f7e0722548e2b35e901d9d974797097635e`.

## Validation scope

The structured recipe copies `Statement.lean`, `AnchorAudit.lean`, `ObligationTree.lean`,
`Proof.lean`, `ExactRoot.lean`, and `Validation.lean` into a disposable directory. It elaborates
fresh module outputs with the pinned Lean 4.29.0 executable, `--trust=0 -t0`, one Lean thread, fixed
locale and timezone, a read-only host filesystem, and Bubblewrap's separate network namespace.
The worker did not run `lake update`, `lake build`, clone, fetch, or any dependency mutation.

`Validation.lean` imports neither `ObligationTree` nor `ExactRoot`. It separately binds
`Proof.azumaUpperTail` to the exact frozen `Statement` type, bypassing the proof phase's threshold
package composition route. That catches an exact-type/composition mismatch, but it reuses the proof
body and runs in this worker clone. It is same-worker differential corroboration, not a distinct
proof body or the independent-runner attestation required by section 10.7.

## Commands and results

```text
python3 -I -B Stage1_Instances/THM-M-1080/check_validation.py
  exit 0: exact root, frozen composition, direct proof, anchor, and differential bridge replayed
  under network isolation; selected trust/provenance observations passed; release gates failed closed

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-1080
  exit 0: rank 522, planned L0/rework-required target; theorem_complete=false

python3 -m json.tool Stage1_Instances/THM-M-1080/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-1080/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

git diff --check -- Stage1_Instances/THM-M-1080 .stage1-worker-selftest.json plus no-index
checks for every new file
  exit 0: no whitespace diagnostics
```

The older `check_proof.py` is intentionally not used as a current validation gate. It is bound to
the proof worker's historical base revision and self-test packet, so its surrounding script now
kernel-replays successfully and then rejects the integrated checkout. This phase preserves that
historical checker, hash-binds its proof receipt, and directly replays all claimed declarations
instead of weakening the old check.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow exact-root kernel replay | pass | Six copied sources elaborate with `--trust=0`; the direct root and frozen-composition root both have the exact canonical type. |
| Placeholder, bodyless, and unsafe observation | pass for checked closure | Lean's `assert_no_sorry` covers the direct and differential roots, local source scans are clean, and the selected transitive closure reports no unknown bodyless nonaxiom or unsafe declaration. |
| Foundation observation | pass for checked declarations | The anchor, composition, eight proof declarations, three exact-root declarations, and differential bridge report exactly `propext`, `Classical.choice`, and `Quot.sound`. Full TCB acceptance remains open. |
| Selected provenance and pins | pass | Frozen target and denominator hashes, local proof/composition hashes, clean mathlib revision/tree/remote, selected source/blob/object, license, toolchain, and executable identities agree. |
| Proof dependency | fail closed | `S56-M-1080-PROOF` is provisional `[_]`, not master-accepted `[x]`; accepted structured state remains open. |
| Hermetic release reproduction | fail closed | The replay denies network and creates fresh local outputs, but uses the shared warm `.lake` cache and dirty worker clone; no empty-cache cold bootstrap, content-addressed offline restoration, full SBOM/TCB, or second platform exists. |
| Independent verification | fail closed | The differential bridge runs with the same proof body, worker identity, checkout, and dependency cache; no distinct runner, second signature, or independently implemented release verifier exists. |

The proof remains a provisional `M0-L` candidate only. The authoritative accepted vector is still
`H2/M3/R3`, with no accepted proof obligation or receipt. Human-source `H0`, readable `R0`, complete
provenance/TCB closure, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, and master acceptance
remain open.

## Status boundary

This is a self-tested validation-node handoff for master inspection. It truthfully records passed
narrow gates and failed dependency/release gates. It does not claim `E0/E1`, accepted `M0-*`,
independent evidence, theorem completion, release, or master acceptance.
