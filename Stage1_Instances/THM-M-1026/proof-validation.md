# THM-M-1026 proof-phase validation

Item: `S56-M-1026-PROOF`. Base revision:
`d3d4bc991fae237427b8ac391bbe701dca8f2af2`.

## Implemented bodies

`Proof.lean` closes the frozen converse branch. `stable_normalizers` converts the
normalizers supplied for every `n >= 2` by `IsStableLaw` into total sequences,
using positive scale `1` and center `0` at the two irrelevant initial indices.
`weaklyConverges_of_eventually_eq` proves the exact bounded-continuous-test weak
convergence predicate from eventual equality. `converseTerminal` chooses the
stable law itself as the attracting probability law and composes those bodies.

Lean checked all three bodies at trust level zero. Each declaration reports
exactly `propext`, `Classical.choice`, and `Quot.sound`. This supplies local
bodies for `M1026-C-STABLE-WITNESS`, `M1026-L-CONSTANT-WEAK-LIMIT`,
`M1026-B-CONVERSE`, and `M1026-T-CONVERSE`.

## Open boundary

The necessity direction remains open. Its first missing frozen package is
`M1026-C-BLOCK-DECOMPOSITION`; it also requires the convergence-of-types limit
comparison and the weak-convergence/characteristic-function bridge. Pinned
mathlib supplies supporting convolution and Levy-convergence APIs but no
terminal generalized central limit theorem or convergence-of-types theorem.
The remaining root cut is therefore `M1026-T-NECESSITY`.

The root is not kernel-closed, and this is partial proof-phase evidence rather
than theorem completion. The root machine classification may move from `M3` to
`M2` only after master acceptance of this receipt. Validation, release, source,
readability, hermetic, and independent-verification gates remain open.

## Validation record

Commands ran in this worker clone on 2026-07-14. The isolated Lean script wrote
only beneath a temporary directory under `/tmp` and removed it on exit. It used
the existing pinned artifacts and did not update, build, fetch, clone, or mutate
`.lake`.

| Command | Exit | Result |
|---|---:|---|
| `bash Stage1_Instances/THM-M-1026/check_proof.sh` | 0 | Isolated statement, frozen composition boundary, and converse proof elaborated at trust zero; all three proof declarations reported exactly `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-1026/check_proof.py` | 0 | Source hashes, frozen fingerprints and denominator, four claimed obligations, receipt/blocker boundary, and prohibited devices passed |
| `python3 Stage1_Instances/THM-M-1026/check_obligation_tree.py` | 0 | Frozen 16-obligation, 46-edge pre-proof architecture passed and intentionally still reported its snapshot root open at M3 |
| `python3 Stage1_Instances/THM-M-1026/check_statement.py` | 0 | Canonical expression SHA-256 `e39476697d12d054b84ab39c07251418d449ba5ea094c2bb37df9850c7caff93`; four mutations distinguished |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1026` | 0 | Rank 502; planned L0/rework-required target; theorem incomplete |
| `python3 -m json.tool` on the three proof JSON files and worker packet | 0 | All structured artifacts parsed |
| `git diff --check -- Stage1_Instances/THM-M-1026 .stage1-worker-selftest.json` | 0 | No whitespace errors |

Status boundary: provisional evidence for the full converse branch only. No
necessity body, exact root proof, accepted state, audit completion, master
acceptance, validation/release completion, or theorem completion is claimed.
