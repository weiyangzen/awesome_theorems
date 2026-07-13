# THM-M-0484 validation-phase result

Item: `S56-M-0484-VALIDATION`. Base revision:
`27400857bccc93638c97e9c65859ddf5d5b5f4da`.

## Narrow validation

The exact proof root and a separately written residue-route reconstruction both kernel-elaborate
with `--trust=0` against pinned Lean 4.29.0 and mathlib `8a178386`. The differential module imports
neither `Proof` nor `ObligationTree`; it proves the residue form from the two pinned correctness
directions, then uses the statement phase's checked definitional transport to recover the unchanged
canonical target. It is same-worker differential corroboration, not a distinct proof body or
independent-runner attestation.

The validator copies `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, `Validation.lean`, and
`AnchorAudit.lean` into a temporary directory, creates only temporary statement and obligation
oleans, fixes the toolchain, locale, and timezone, and removes the directory. It observes exactly
`propext`, `Classical.choice`, and `Quot.sound` for the terminal, proof, anchor, and differential
declarations. The parser/elaborator closure walk covers 35,389 declarations in 1,243 modules and
reports no bodyless nonaxiom or unsafe declaration. Direct terminal source bodies, source blob,
compiled olean, clean mathlib revision/tree, canonical remote, and license all match the recorded
pins.

## Commands and exact results

All commands ran on 2026-07-13 in this worker clone. The scheduler-provided absolute `.lake`
symlink was reused read-only. No `lake update`, `lake build`, dependency clone/fetch, or dependency
mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0484` | 0 | rank 1365, planned, proof provisional, theorem incomplete |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `27400857...f4da`, tree `3762537e...275c` |
| `bash Stage1_Instances/THM-M-0484/check_proof.sh` | 0 | trust-zero isolated statement/tree/proof replay; one sorry-free report and six exact classical-trio axiom reports |
| `python3 -I -B Stage1_Instances/THM-M-0484/check_validation.py --worker-packet .stage1-worker-selftest.json` | 0 | exact root, differential residue route, terminal closure, direct provenance, current DAG/receipt/graph boundary, and worker packet passed; unavailable release gates failed closed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0484-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0484/check_validation.py` | 0 | checker syntax compiled outside the repository tree |
| JSON parsing, scoped prohibited-construct scan, and `git diff --check` | 0 | records parsed, scan found no prohibited code construct, and whitespace checks passed |

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | The exact proof root, frozen conditional composition, both pinned terminals, and the differential exact root elaborate at trust zero. |
| Placeholder and unsafe boundary | provisional pass | Kernel `assert_no_sorry`, supplemental comment-stripped scans, and the terminal closure traversal find no placeholder, bodyless nonaxiom, or unsafe declaration in the checked boundary. |
| Trust observation | provisional pass | Every checked declaration reports exactly the selected classical trio, and the terminal closure walk is empty for bodyless nonaxioms and unsafe declarations. The theorem-specific foundation policy and complete TCB are unaccepted. |
| Direct provenance | provisional pass | Both source-body IDs, source/olean hashes, immutable revision/tree/blob, clean tree, remote, and license agree. The sorted transitive declaration/import closure and full imported-artifact TCB are not serialized and content-addressed. |
| Structured authority | fail closed | The proof receipt is only provisional. The accepted instance/graph remain `[H1,M3,R4]`, `root_closed=false`, with no accepted receipt or obligation closure. |
| Per-node composition | fail closed | Seventeen source-body decomposition plans have no abstract-child composition certificates and receive no individual credit. |
| Hermetic replay | fail closed | The run used a shared warm `.lake` symlink; there is no clean checkout, cold empty cache, enforced network denial, offline archive restoration, or complete SBOM/TCB bundle. |
| Independent verification | fail closed | The differential route ran under the same worker identity, checkout, terminal bodies, and cache; there is no distinct signed runner, second attestation, or independently implemented minimal release verifier. |

This validation node is genuinely self-tested and records all available gate outcomes, but its first
failed gate is proof-dependency master acceptance. It grants no content-addressed `E0/E1`, accepted
`M0-W`, individual graph closure, `AUDIT-Z`, `THEOREM-Z`, release, or theorem-completion credit.
`audit_complete=false` and `theorem_complete=false` remain explicit.
