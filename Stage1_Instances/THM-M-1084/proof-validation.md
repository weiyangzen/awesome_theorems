# THM-M-1084 proof-phase validation

Item: `S56-M-1084-PROOF`. Base revision:
`a1a7e939e58f103f5ff5d23af51437fa8658aa04`.

## Implemented bodies

`GaussianMGFBridge.lean` extracts every process increment from the frozen finite-linear-combination
Gaussian interface, proves that the ambient measure is a probability measure, identifies a centered
real Gaussian pushforward with the Gaussian measure having its exact second moment, and derives
both the exact MGF identity and `HasSubgaussianMGF` at parameter
`Real.toNNReal (dist s t ^ 2)`. This closes the substantive frozen
`M1084-N-GAUSSIAN-MGF` leaf without changing any process, centering, or canonical-distance premise.

`CoveringNets.lean` obtains a finite positive-radius open-ball cover from total boundedness, proves
that the custom `Nat.sInf` covering number is attained, and proves it is positive for a nonempty
index type. These are exact local bodies toward `M1084-C-NETS`; the broader parent-map/cardinality
package is not claimed closed.

## Open boundary

The exact target `Stage1Instances.THM_M_1084.DudleyEntropyBoundTarget` remains open at `M3`.
The first failed completion gate and minimal terminal cut remain `M1084-T-INTEGRABLE` and
`M1084-T-ENTROPY`. In particular, no local body yet constructs chaining parent maps, supplies the
finite-maximum estimate, proves the constant-12 dyadic sum-to-integral comparison, or performs the
separability/limit passage. The external `SLT.dudley` candidate is neither in the pinned closure nor
an exact theorem match. No terminal package, root proof, validation/release decision, audit
completion, master acceptance, or theorem completion is claimed.

## Commands and results

All commands used the existing canonical pinned `.lake` artifacts. No `lake update`, `lake build`,
dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1084` | 0 | Rank 526, lifecycle `planned`, baseline L0/rework-required, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1084/check_obligation_tree.py` | 0 | Frozen 16-node, 36-edge registry passed; root remained open at M3. |
| `bash Stage1_Instances/THM-M-1084/check_proof.sh` | 0 | Disposable `--trust=0` replay elaborated `Statement.lean`, `GaussianMGFBridge.lean`, and `CoveringNets.lean`; seven gate-audited declarations were sorry-free and used only `propext`, `Classical.choice`, and `Quot.sound`. |
| `rg -n '\b(sorry\|admit\|sorryAx\|implemented_by\|native_decide)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe\|extern)[[:space:]]+' Stage1_Instances/THM-M-1084 --glob '*.lean'` | 1 | Expected no-match exit: no `sorry`, `admit`, `sorryAx`, axiom-like declaration, unsafe/opaque body, external declaration, implementation escape, or native oracle. |
| `python3 -m json.tool Stage1_Instances/THM-M-1084/proof-attempt.json` | 0 | Structured partial-attempt record is valid JSON. |
| `python3 -m json.tool Stage1_Instances/THM-M-1084/proof-receipt.json` | 0 | Provisional node receipt is valid JSON. |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | Worker handoff packet is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1084 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |

The proof script discovers Lean and `LEAN_PATH` through `lake env`, writes the local
`Statement.olean` and all logs only beneath `/tmp/stage1-m1084-proof.*`, uses
`LEAN_NUM_THREADS=1` and `--trust=0`, and deletes the directory on exit. The worker clone's
pre-existing untracked `.lake` symlink is nonrelease automation state and was left unchanged.

## Status boundary

This self-test proposes `[_]` only for substantive partial proof work. The accepted root vector
remains `[H1, M3, R3]`, and every terminal assurance gate remains open.
