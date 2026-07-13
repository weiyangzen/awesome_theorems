# THM-M-0476 validation-phase result

Item: `S56-M-0476-VALIDATION`. Base revision:
`c45f3c7090cb4adf616d45e5414985f956e807b2` (tree
`da6f991c07f11e8608ddc090af9356558d64d360`).

## Exact validation result

The structured validation recipe replays the frozen statement, conditional obligation
composition, direct pinned root, and full expanded root. It also compiles `Validation.lean`, which
imports neither `Proof` nor `ObligationTree` and reconstructs the exact target through
`Nat.prime_iff_fac_equiv_neg_one`. That reconstruction is a same-worker differential check; the
characterization ultimately shares `ZMod.wilsons_lemma`, so it is neither a distinct terminal proof
body nor independent-runner evidence.

Lean subprocesses run in a fresh temporary directory under Bubblewrap with the host filesystem
read-only, that directory as the only writable path, fixed `LANG`, `LC_ALL`, and `TZ`, and an
unshared network namespace. The recipe fixes `LEAN_PATH` to existing pinned compiled artifacts, so
it does not resolve, update, build, clone, fetch, or mutate dependencies.

## Commands and results

Commands ran from repository root on 2026-07-14 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | The structural standard, target projection, and 1546 uniform-L0 targets pass. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 pass. |
| `python3 scripts/stage1_target.py show THM-M-0476` | 0 | Rank 1357, planned, L0/rework_required, theorem incomplete. |
| `python3 -B Stage1_Instances/THM-M-0476/check_validation.py` | 0 | Exact kernel, axiom, hygiene, selected provenance, network isolation, and fail-closed gate decisions pass. |
| `python3 -m json.tool Stage1_Instances/THM-M-0476/validation-spec.json` | 0 | Structured recipe is valid JSON. |
| `python3 -m json.tool Stage1_Instances/THM-M-0476/validation-receipt.json` | 0 | Provisional receipt is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0476 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `Validation.lean` elaborate; both proof roots and the differential root have the exact frozen type. |
| Placeholder and unsafe boundary | pass | Local checked modules and selected terminal source files contain no credited `sorry`, `admit`, bodyless axiom/constant, `opaque`, `unsafe`, `extern`, `implemented_by`, or `native_decide` route. |
| Axiom observation | provisional pass | Every checked declaration is within `{propext, Classical.choice, Quot.sound}`; the three exact roots use exactly that set. |
| Selected provenance | pass | Statement/registry hashes, mathlib revision/tree/remote/cleanliness, two source blobs, terminal body slices, compiled objects, and the mathlib license agree with the receipt. |
| Proof prerequisite | fail closed | `S56-M-0476-PROOF` is worker-provisional `[_]`, not master-accepted `[x]`. |
| Complete foundation and trust closure | fail closed | No accepted theorem-specific foundation policy, complete transitive declaration/import graph, compiler/bootstrap/plugin/native/checker TCB inventory, or complete SBOM exists. |
| Hermetic release reproduction | fail closed | The replay is network-isolated and read-only but reuses the shared warm canonical `.lake`; it is not a new clean checkout, empty-cache cold build, or offline-restorable deterministic bundle. |
| Independent verification | fail closed | The separately written Lean route ran under this worker identity, checkout, kernel, and shared cache; there is no second signed attestation or independently implemented release verifier. |
| Human/readable review | fail closed | Pinpoint primary-source `H0` and independently reviewed readable `R0` remain open. |

This is self-tested nonrelease worker evidence. It grants no accepted `E0/E1`, `M0-W`, `AUDIT-Z`,
`THEOREM-Z`, release, or master acceptance. The accepted vector stays `[H1, M3, R4]`,
`audit_complete=false`, and `theorem_complete=false`.
