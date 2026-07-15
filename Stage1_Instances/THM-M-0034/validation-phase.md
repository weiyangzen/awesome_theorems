# THM-M-0034 validation-phase result

Item: `S56-M-0034-VALIDATION`

Base revision: `61f7b69093a1a921bba3b39c1c58955f9b3a4808`

Validation time: `2026-07-15T18:10:00+08:00`

## Exact result

The node-scoped validator compiled the unchanged frozen statement, all eight vendored modules, the
proof adapter, its audit, and a separately written differential adapter in fresh `/tmp` outputs.
Every Lean invocation used the pinned Lean 4.29.0 executable with `--trust=0 -t0` inside a
bubblewrap network namespace. The host was read-only except for the temporary output tree. No
`lake update`, `lake build`, dependency clone/fetch, network operation, or `.lake` mutation ran.

The terminal theorem, local exact root, and differential exact root are sorry-free and report
exactly `propext`, `Classical.choice`, and `Quot.sound`. The differential closure contains 30,764
declarations from 1,094 modules, with no unexpected bodyless or unsafe declarations. The reversible
vendor checker also reconstructed all eight upstream source files and passed its import, per-file,
compatibility-operation, semantic-diff, size, and Apache-2.0 boundary checks.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | The frozen proposition, vendored terminal body, local exact adapter, and no-`Proof` differential adapter freshly elaborate at trust zero. |
| Placeholder/unsafe/oracle | pass in observed scope | Terminal and roots pass `assert_no_sorry`; comment-aware scans found no prohibited mechanism; the differential transitive closure reports no unexpected bodyless or unsafe declarations. |
| Direct provenance | provisional pass | Local hashes, pinned upstream revision/tree/archive, eight vendored source hashes, reversible compatibility ledger, Apache notices, and clean pinned mathlib agree. |
| Proof dependency | fail closed | `S56-M-0034-PROOF` is only provisional `[_]`; it has no dependency-ordered master acceptance. |
| Frozen architecture | fail closed | Registry v1 selects `edmund-ukaisi@e8d85a6f` at `M0034-X-EXTERNAL-BODY`; the checked Apache-2.0 proof uses informational `mbkybky@51ed173b` at `M0034-X-ALT-PID`. No frozen obligation receives closure credit. |
| Authoritative state | pending master | The frozen graph remains root-open at `M3`, accepted closure is empty, and the dossier vector remains `H1/M3/R4`. |
| Hermetic release replay | fail closed | Fresh network-isolated outputs reused the shared warm canonical `.lake`; there is no clean-checkout cold empty-cache build, offline restoration, or complete TCB/SBOM archive. |
| Independent verification | fail closed | The separate Lean adapter ran in the same worker and cache. There is no distinct signed verifier, independently provisioned runner, or independent minimal verifier. |

The first failed validation gate is
`dependency.S56-M-0034-PROOF.master_acceptance_and_frozen_route_reconciliation`. The first failed
release gate is `S56-10.6-HERMETIC-COLD-BUILD`. This genuinely self-tests the blocked validation
implementation and therefore proposes worker state `[_]`; it does not complete the validation
phase or claim accepted proof, `E0/E1`, `M0-*`, `AUDIT-Z`, `THEOREM-Z`, release, or theorem
completion.

## Commands and results

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0
  All 15 assurance groups and exactly 1546 uniform-L0 targets passed.

python3 scripts/stage1_target.py check
  exit 0
  All 1546 unique ordered targets at ranks 1 through 1546 passed.

python3 scripts/stage1_target.py show THM-M-0034
  exit 0
  Rank 1078; planned; L0/rework_required; theorem_complete=false.

python3 -I -B Stage1_Instances/THM-M-0034/build_vendor_manifest.py
  exit 0
  Eight modules, 5079 lines, 260645 bytes, and both reversible port digests passed.

bash Stage1_Instances/THM-M-0034/check_proof.sh
  exit 0
  Statement, eight vendor modules, Proof, and ProofAudit compiled from fresh outputs at
  --trust=0 -t0; terminal and root are sorry-free with exactly the allowed axiom trio.

python3 -I -B Stage1_Instances/THM-M-0034/check_validation.py \
  --worker-packet .stage1-worker-selftest.json
  exit 0
  Network-isolated trust-zero replay passed the narrow kernel, trust-observation, and direct
  provenance checks while dependency, architecture, cold-hermetic, and independent gates failed
  closed.

python3 -B Stage1_Instances/THM-M-0034/check_obligation_tree.py
  exit 1
  Known stale prerequisite inventory: instance.json predates proof and validation artifacts.

python3 -B Stage1_Instances/THM-M-0034/check_proof.py
  exit 1
  Known stale proof snapshot: the proof validator is bound to base 6ac589f, not current integrated
  base 61f7b690. The direct proof replay above remains valid.

git diff --check -- Stage1_Instances/THM-M-0034 .stage1-worker-selftest.json
  exit 0
  No whitespace diagnostics; the validator also checks untracked artifact hygiene.
```

## Retry condition

After the integration lane accepts the proof dependency and publishes a master-accepted registry v2
or append-only route delta for `mbkybky/QuillenSuslin@51ed173b`, rerun this recipe against that
immutable snapshot. Release assurance additionally requires complete foundation, provenance, TCB,
SBOM, and source/readability evidence; cold offline restoration; two distinct signed runners; and an
independently implemented minimal verifier.

## Status boundary

This is self-tested nonrelease worker evidence for exact kernel replay and bounded trust/provenance
observations. It truthfully returns `blocked` while proposing only `[_]` for the validation
implementation. It is not accepted frozen-graph closure, release-grade hermetic evidence,
independent verification, audit completion, theorem completion, release, or master acceptance.
