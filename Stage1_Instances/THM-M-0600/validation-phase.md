# THM-M-0600 validation-phase result

Item: `S56-M-0600-VALIDATION`

Validation date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `7348dc646fd6babfe2b82c35b4c03a9ed5921f8e`

## Narrow Validation

The structured recipe re-elaborates the exact statement, the conditional
composition in `ObligationTree.lean`, the zero-dimensional proof and both
conditional declarations in `Proof.lean`, the pinned ingredient probes in
`AnchorAudit.lean`, and two separately written declarations in
`Validation.lean`. Each Lean process runs at trust level zero in a fresh
temporary output directory. Bubblewrap denies outbound network access, makes
the host filesystem read-only, and fixes locale, timezone, thread count, and
the writable output boundary.

`Validation.lean` imports only `Statement`. It reconstructs the dimension-zero
branch without using the proof implementation and separately checks the final
adapter while keeping the positive-dimensional engine as an exact premise.
The five hash-bound Lean modules pass a nested-comment-aware scan for
placeholders, bodyless declarations, unsafe/oracle devices, and backend proof
shortcuts. All six proof or differential axiom reports are exactly
`propext`, `Classical.choice`, and `Quot.sound`.

This is a truthful negative-root validation. The proof predecessor is only
worker-provisional, the dimension-zero registry fingerprint remains planned,
and no premise-free declaration inhabits `MorseNormalFormEngine` or
`MorseLemmaTarget`. The root therefore remains `[H1, M3, R3]`, with
`M0600-T-ENGINE` as its open cut and `theorem_complete=false`.

## Commands And Results

All commands ran from the repository root. The automation-provided canonical
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, or network request was performed.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0600` | 0 | Rank 638, planned hard-statement-first lane, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0600/check_obligation_tree.py` | 0 | 18 obligations and 44 typed edges passed; denominator `071b0844...f981`; root open M3. |
| `python3 -I -B Stage1_Instances/THM-M-0600/check_validation.py` | 0 | Network-isolated trust-zero narrow replay, hygiene, six exact axiom reports, and selected provenance passed; dependency, root, hermetic-release, and independent-runner gates failed closed. |
| `python3 -m json.tool Stage1_Instances/THM-M-0600/validation-spec.json` | 0 | Valid structured validation recipe. |
| `python3 -m json.tool Stage1_Instances/THM-M-0600/validation-receipt.json` | 0 | Valid provisional node receipt with `verdict=blocked`, `accepted=false`. |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | Valid seven-field worker packet proposing only `[_]`. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0600-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0600/check_validation.py` | 0 | Validator syntax checked without writing into the repository. |
| `git diff --check -- Stage1_Instances/THM-M-0600 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

## Gate Decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | provisional pass | Fresh local oleans elaborate at trust zero against the pinned warm dependency closure. |
| Placeholder and unsafe boundary | provisional pass | The source scan and kernel sorry checks found no prohibited proof device. |
| Axiom observation | provisional pass | Six declarations report exactly the selected classical trio; this does not accept a complete foundation/TCB profile. |
| Selected local provenance | provisional pass | Current local hashes, the clean pinned mathlib revision/tree/remote/license, and four source/blob/olean identities agree. |
| Proof dependency | fail closed | `S56-M-0600-PROOF` is `[_]`, its receipt is unaccepted, and it has no accepted closed obligation. |
| Exact root | fail closed | `M0600-T-ENGINE` has no premise-free proof body; every root adapter retains it explicitly. |
| Human source and readability | fail closed | Exact primary-source pages, conventions, errata, independent source review, H0, and reviewed R0 remain open. |
| Hermetic release replay | fail closed | The run reused shared warm dependencies rather than a clean checkout, empty caches, cold rebuild, offline restoration, and complete SBOM/TCB archive. |
| Independent verification | fail closed | The differential module shares this worker identity, clone, kernel, and cache; no distinct signed independently provisioned runner or minimal verifier exists. |

The validation node is self-tested only as an honest, nonrelease blocked
receipt. It grants no accepted obligation state, root closure, `M0-*`,
`E0/E1`, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or master
acceptance.
