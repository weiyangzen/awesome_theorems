# THM-M-0593 validation-phase result

Item: `S56-M-0593-VALIDATION`  
Base revision: `799262a53af4c03d919b758421e149ffc158d472`  
Validation time: `2026-07-14T23:25:18Z` (`2026-07-15T07:25:18+08:00`)

The node-scoped validator copied `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and
`Validation.lean` to a fresh temporary directory. Every Lean invocation used the pinned executable
selected by `lake env lean`, passed `--trust=0`, fixed locale/timezone/thread count, and wrote only
fresh module outputs in that temporary directory. The recipe invoked no network-capable operation,
but outbound-network denial was not independently enforced; that gate therefore fails closed. No
proof content was added to the target or proof module during validation.

## Exact result

```text
env LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC LEAN_NUM_THREADS=1 \
  python3 -I -B Stage1_Instances/THM-M-0593/check_validation.py
  exit 0
  PASS S56-M-0593-VALIDATION narrow nonrelease validation
  kernel: exact statement, conditional composition, two partial proof bodies, and same-worker differential probes replayed from fresh outputs with trust zero
  trust: seven declarations are sorry-free and report only propext, Classical.choice, and Quot.sound
  provenance: proof hashes, clean mathlib pin, selected source blobs, oleans, license, and tool digests agree
  root open: HardDimensionBranch is an explicit premise; accepted state remains H1/M4/R4 and theorem_complete=false
  blocked: root proof, enforced network isolation, complete TCB/provenance, cold empty-cache offline replay, and distinct-runner independent verification
```

The differential module imports neither `Proof` nor `ObligationTree`. It independently spells the
exact `SardTarget`, proves the zero-codomain branch again, and reconstructs the exhaustive dimension
split. Its `conditionalExactRoot` still consumes both analytic branch interfaces, including the
unproved `HardDimensionBranch`; it is same-worker differential evidence, not an unconditional root
proof or independent-runner attestation.

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. The
existing canonical `.lake` artifacts were reused read-only.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | The exact statement, frozen branch composition, both partial proof bodies, and differential probes freshly elaborate with trust zero. |
| Placeholder/unsafe scan | pass | Comment-aware scans and Lean's `assert_no_sorry`/`#print sorries` find no prohibited local proof mechanism. |
| Direct axiom observation | provisional pass | Seven declarations report no axioms beyond `propext`, `Classical.choice`, and `Quot.sound`. An accepted foundation/TCB profile remains absent. |
| Selected provenance | provisional pass | Current proof hashes, clean pinned mathlib revision/tree/remote/license, three direct source blobs, and their oleans agree. Full transitive proof-body provenance remains open. |
| Exact root closure | fail closed | `sardTarget_of_hardDimensionBranch` and the differential composition both require the unproved hard Morse-Sard branch. The provisional cut remains `M0593-L-RANK-REDUCTION` and `M0593-L-TAYLOR`. |
| Authoritative state | pending master | The predecessor is only `[_]`; the accepted graph remains root-open at `[H1, M4, R4]` with its frozen pre-proof cut. |
| Hermetic release replay | fail closed | Network denial was not independently enforced, and the run used a mutable worker clone and shared warm dependency cache rather than a clean checkout, empty-cache cold build, or offline archive restoration. |
| Independent verification | fail closed | No distinct signed runner, independently provisioned cache, second attestation, or independently implemented minimal verifier exists. |

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0593` | 0 | rank 633, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0593/check_obligation_tree.py` | 0 | 22 obligations and 43 typed edges passed; authoritative root open at M4 |
| `env LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC LEAN_NUM_THREADS=1 python3 -I -B Stage1_Instances/THM-M-0593/check_validation.py` | 0 | four-module replay, hygiene, receipt binding, pin/provenance checks, and fail-closed decisions passed |
| `python3 -m json.tool Stage1_Instances/THM-M-0593/validation-spec.json` | 0 | structured validation recipe parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0593/validation-receipt.json` | 0 | provisional node receipt parsed |
| `git diff --check -- Stage1_Instances/THM-M-0593 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is a genuinely self-tested negative theorem-validation result and positive validation-runner
self-test. It proposes only worker state `[_]` for this phase. It grants no accepted obligation
closure, `M0-*`, `E0/E1`, `H0`, `R0`, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or master
acceptance.
