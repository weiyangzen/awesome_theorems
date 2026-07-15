# THM-M-0317 validation-phase result

Item: `S56-M-0317-VALIDATION`

Base revision: `e46e0735d0940bb558acaf027d8386de2579f55d`

Validation interval: `2026-07-15T09:27:00+08:00` to
`2026-07-15T09:27:41+08:00` (`Asia/Shanghai`)

The structured recipe copied `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and
`Validation.lean` into a disposable directory and created fresh local module outputs. The validator
used Elan's declared toolchain selection and the manifest-pinned Lake environment to discover and
digest-check the Lean/Lake executables and compiled dependency path. Every Lean invocation used the
digest-checked executable with `--trust=0` under Bubblewrap, with the host mounted read-only, a
private writable temporary directory, fixed locale/timezone/thread count, and outbound networking
denied. No proof content was added to `Proof.lean`, and no `lake update`, `lake build`,
dependency clone/fetch, or `.lake` mutation was performed.

## Exact result

```text
execute validation-spec.json argv without shell interpolation
exit 0
PASS S56-M-0317-VALIDATION narrow network-isolated validation
kernel: exact statement, four mutations, conditional composition, three partial proof declarations, and two differential declarations replayed with trust zero
trust: all proof-bearing declarations are sorry-free and report only propext, Classical.choice, and Quot.sound
provenance: local proof hashes, clean pinned mathlib, three selected source/blob/olean identities, license, and tool digests agree
blocked: ApproximationPackage and the exact root remain open; complete TCB/provenance, cold empty-cache replay, and distinct-runner verification fail closed
```

`Validation.lean` imports neither `Proof` nor `ObligationTree`. It independently spells the small-
displacement and compactness-limit interfaces, reimplements the compactness/closed-image argument,
and constructs the exact target only conditionally on the still-open approximation interface. This
is a useful differential check of the partial body, not an unconditional root proof or a distinct-
runner attestation.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Canonical source and mutations | provisional pass | The hash-bound canonical source and all four non-equivalence witnesses freshly elaborate with trust zero; independent expression-fingerprint acceptance remains open. |
| Partial kernel replay | provisional pass | The conditional composer, three proof declarations, and two separately written validation declarations freshly elaborate. |
| Placeholder/unsafe/oracle scan | pass | Nested-comment-aware scans plus `assert_no_sorry` and `#print sorries` find no prohibited local proof mechanism. |
| Direct axiom observation | provisional pass | Eleven checked theorem declarations report no principles beyond `propext`, `Classical.choice`, and `Quot.sound`; no accepted foundation profile exists. |
| Selected provenance | provisional pass | Local input hashes, clean pinned mathlib revision/tree/remote/license, and three selected source/blob/olean identities agree. Full transitive closure is absent. |
| Exact root closure | fail closed | `ApproximationPackage` has no proof body. The conditional roots retain it as an explicit premise, so `M0317-T-APPROX` and `M0317-ROOT` remain open. |
| Authoritative graph/state | pending master | The proof predecessor is only `[_]`. The frozen graph predates the partial proof and requires architecture-owner reconciliation; this worker changes no authoritative state. |
| Hermetic release replay | fail closed | The complete recipe and every Lean child are network-isolated with fresh outputs, but the run reuses a mutable checkout and warm compiled dependencies rather than a clean empty-cache cold build or offline restoration. |
| Independent verification | fail closed | The differential module shares the worker, checkout, toolchain, and cache; no second signed attestation, distinct runner, or independently implemented minimal release verifier exists. |

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0317` | 0 | rank 683, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0317/check_obligation_tree.py` | 0 | 17 obligations and 33 typed edges passed; frozen pre-proof root remained open |
| structured Python argv in `validation-spec.json` | 0 | every Lean child was network-isolated; four-module replay, hygiene, receipt binding, selected provenance, and fail-closed decisions passed |
| `python3 -m json.tool Stage1_Instances/THM-M-0317/validation-spec.json` | 0 | structured recipe parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0317/validation-receipt.json` | 0 | provisional node receipt parsed |
| `git diff --check -- Stage1_Instances/THM-M-0317 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is a genuinely self-tested negative root-validation result and a positive self-test of the
scoped validation implementation. It proposes only worker state `[_]` for this phase. It grants no
accepted obligation closure, `ApproximationPackage`, exact root, `M0-*`, `E0/E1`, `H0`, `R0`,
`AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or master acceptance.
