# THM-M-0822 validation-phase evidence

Item: `S56-M-0822-VALIDATION`. Base revision:
`5b35bc151522d93c7f54966ef64f1fc630371537`; base tree:
`fe77824631ab2573a4596bddc1a2534c06cd23f8`.

## Validation scope

The node recipe re-elaborates the exact frozen maximum-value statement, all
six frozen package-composition declarations, the proof root and its pinned
terminal, and a proof-free recheck of the exact root in temporary output
space. Every Lean subprocess runs with `--trust=0` in a Bubblewrap network
namespace with a cleared environment, fixed locale, timezone, and thread
count, and a read-only host filesystem except for the temporary directory.

`Validation.lean` imports `Proof` and adds no theorem, lemma, example, or other
proof body. It asks Lean's sorry and axiom utilities to recheck the existing
exact root and pinned EKR terminal. This is a same-worker validation replay,
not a distinct-runner attestation, and receives no duplicate proof credit.

All proof declarations and validation rechecks are sorry-free and report nonempty
subsets of the allowed `propext`, `Classical.choice`, and `Quot.sound` profile;
the proof root, pinned terminal, and validation root recheck report exactly that
set. The validator binds the exact target expression, registry denominator,
frozen graph and predecessor receipt hashes, mathlib revision/tree, clean
dependency source, EKR source/blob/body/compiled-object hashes, remote,
license, and tool identities. No prohibited proof or implementation mechanism
was found in the target sources or selected EKR body.

This is narrow, nonrelease validation. The proof prerequisite is only `[_]`;
accepted authority remains `[H1, M3, R4]` with no accepted receipt or closed
obligation. The selected terminal-body provenance passes, but its complete
transitive declaration/import/compiled-object closure, the compiler/bootstrap
TCB, and an SBOM are not available and therefore fail closed.

## Commands and results

Commands ran from this isolated worker clone on 2026-07-15 (Asia/Shanghai).
The automation-provided pinned `.lake` symlink was reused read-only. No
`lake update`, `lake build`, clone, fetch, checkout, dependency mutation, or
network operation ran.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0822
  exit 0: rank 1380, planned L0/rework-required target; theorem_complete=false

bash Stage1_Instances/THM-M-0822/check_validation.sh
  exit 0: network-isolated trust-0 exact proof and proof-free validation module
  elaborated; all six compositions and twelve proof assertions passed;
  stdout was 7921 bytes at SHA-256
  2de5d4df63c14cbafe24afac9f36d6f5bb1a37644e8b921ccc4f7bf363e686c4

python3 -I -B Stage1_Instances/THM-M-0822/check_validation.py
  exit 0: exact target/composition replay, hygiene, reciprocal graph, selected
  trust/provenance, frozen hashes, pin, receipt, recipe, and worker packet passed;
  authority and release gates failed closed

python3 -m json.tool Stage1_Instances/THM-M-0822/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0822/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0822-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0822/check_validation.py
  exit 0: validator compiled outside the repository tree

git diff --check -- Stage1_Instances/THM-M-0822 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics; untracked files also passed no-index checks
```

The proof-phase Python checker is intentionally not a current validation gate:
it is bound to its historical base revision and phase-specific worker packet.
This phase hash-binds its immutable artifacts and directly replays the Lean
proof rather than misreporting those expected snapshot mismatches as proof
failures.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel and composition replay | provisional pass | The exact statement, six package compositions, exact proof root, pinned terminal, and proof-free validation recheck elaborate under trust 0 and network isolation. |
| Placeholder and unsafe boundary | pass | Lean sorry reports and a comment-stripped scan found no placeholder, bodyless, unsafe/native/oracle, or external implementation construct. |
| Trust observation | provisional pass | Checked declarations use only the candidate profile; accepted foundation and complete transitive TCB closure remain open. |
| Selected provenance | provisional pass | Exact local hashes and pinned EKR source/blob/body/olean, clean revision/tree, remote, manifest, license, and tool hashes agree; complete transitive provenance and SBOM do not exist. |
| Structured authority | fail closed | `S56-M-0822-PROOF` is only `[_]`; instance and graph accept no receipt or closed obligation and remain H1/M3/R4. |
| Hermetic replay | fail closed | Shared warm `.lake`; no separate immutable clean checkout, empty-cache cold bootstrap, content-addressed offline restoration, complete TCB/SBOM, or deterministic release bundle. |
| Independent verification | fail closed | The validation replay shares this worker, checkout, kernel, and cache; no distinct identity, runner, signature, or independently implemented minimal release verifier exists. |

The first failed node gate is
`dependency.S56-M-0822-PROOF.master_acceptance`; the first failed release gate
is `S56-10.6-HERMETIC-COLD-BUILD`. The accepted vector remains
`[H1, M3, R4]`. Primary-source H0, independently reviewed R0, full transitive
trust/provenance, `AUDIT-Z`, `THEOREM-Z`, release, and theorem completion are
false. This self-tested worker evidence claims no E1, accepted M0, independent
validation, release, or master acceptance.
