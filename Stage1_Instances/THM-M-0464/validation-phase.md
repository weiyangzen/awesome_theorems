# THM-M-0464 validation-phase result

Item: `S56-M-0464-VALIDATION`  
Base revision: `797546bf2bab359f9fc5be515c3d4e8943c9d931`  
Validation time: `2026-07-12T10:27:23+08:00`

The fail-closed validator re-elaborated the frozen statement, conditional root interface, and all
seven proof-phase bodies using the pinned Lean environment. It then elaborated two separately
written boundary proofs from `Validation.lean`, which neither imports nor invokes `Proof.lean`.
The observed trust output was exactly the expected `propext`, `Classical.choice`, and `Quot.sound`,
with no `sorryAx` or prohibited local source token. Source hashes, dependency pins, the clean
pinned mathlib revision, and the 16-node/75-edge open obligation graph were also checked.

This validates only the partial proof deliverable. No unconditional declaration of type
`PilaWilkieStatement` exists. The general cell-decomposition, parameterization, determinant,
induction, counting, and source-transport work remains open, so root provenance and trust cannot
close and the authoritative machine root remains `M3`.

## Commands and exact results

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0464` | 0 | rank 310, planned, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0464/check_validation.py` | 0 | pins, hashes, clean mathlib, placeholder scan, open graph, kernel replay, trust output, and independent boundary reconstructions passed |
| `python3 -m json.tool Stage1_Instances/THM-M-0464/validation-spec.json` | 0 | structured recipe parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0464/validation-receipt.json` | 0 | structured provisional receipt parsed |
| `git diff --check -- Stage1_Instances/THM-M-0464 .stage1-worker-selftest.json` | 0 | no whitespace errors |

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` write was performed.

## Gate decisions

| Gate | Decision | Boundary |
|---|---|---|
| Narrow kernel replay | pass | Statement, conditional composition, and seven partial bodies elaborate. |
| Local trust observation | provisional pass | All printed declarations report the expected three principles and no `sorryAx`. |
| Partial provenance | pass | Local proof/probe hashes and clean pinned mathlib revision are bound in the receipt. |
| Exact root | fail closed | The general Pila-Wilkie packages remain open and no root proof body exists. |
| Hermetic release | fail closed | Shared warm cache; no cold empty-cache offline replay, SBOM, or deterministic bundle. |
| Independent release verification | fail closed | Separate proof code ran in the same checkout/cache, not on a distinct signed runner. |

`audit_complete=false` and `theorem_complete=false`. This is provisional worker validation evidence,
not release, theorem completion, or master acceptance.
