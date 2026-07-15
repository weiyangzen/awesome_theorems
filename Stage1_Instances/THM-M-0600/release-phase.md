# THM-M-0600 release reconciliation

Item: `S56-M-0600-RELEASE`

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

## Exact verdict

`blocked`. The lifecycle remains `planned`. The accepted intake projection remains
`[H1, M4, R3]`; the best current provisional graph and validation classification is
`[H1, M3, R3]`. No accepted debt-state transition is made. Both `audit_complete` and
`theorem_complete` are false, so `AUDIT-Z` and `THEOREM-Z` are blocked. This worker accepts no
receipt and makes no release, theorem-completion, or master-acceptance claim.

The first workflow failure is `S56-10.2-DEPENDENCY-ACCEPTANCE`:
`S56-M-0600-VALIDATION` is only provisional `[_]` evidence, with `accepted=false`,
`release_grade=false`, and no dependency-ordered master acceptance. The first mathematical failure
is `M0600-T-ENGINE-KERNEL-CLOSURE`. Every exact-root adapter still consumes the unproved
positive-dimensional normal-form engine. The first release-input failure is
`S56-RELEASE-IMMUTABLE-CLEAN-FRESH-INPUT`.

## Evidence reconciliation

There is real but narrow positive evidence. A current network-isolated trust-zero replay elaborates
the exact statement, conditional final composition, zero-dimensional proof, pinned ingredient
probes, and the same-worker differential reconstruction. The final adapter and all five proof and
differential declarations are sorry-free and report exactly `propext`, `Classical.choice`, and
`Quot.sound`. The five owned Lean modules pass a nested-comment-aware scan for placeholders,
bodyless declarations, unsafe/oracle devices, and backend proof shortcuts.

That evidence does not prove the Morse lemma. `zeroDimensionBranch` handles only `n = 0`.
`morseNormalFormEngine_of_positiveDimension`, `morseLemmaTarget_of_positiveDimension`, and
`Validation.conditionalRootDirect` all retain the missing positive-dimensional engine explicitly.
The frozen graph therefore remains root-open with `M0600-T-ENGINE` as its cut set, and the proof and
validation receipts accept no closed obligation.

Accepted authority is also unreconciled. `instance.json`, `README.md`, and the theorem-local task
DAG are intake-era projections at `[H1, M4, R3]`; later artifacts describe only provisional
`[H1, M3, R3]` evidence. The graph marks definitions and a conditional adapter `M0-L` but has an
empty evidence graph and no accepted `E0` receipt. Earlier proof-recheck records that predate
`Proof.lean` are superseded as narrow observations, not rewritten. This release decision preserves
the weaker accepted vector and records all conflicts instead of silently promoting them.

`AUDIT-Z` additionally lacks a reconciled inventory and public state, pinpoint primary-source
statement/premise/convention/errata mapping, independent H0 review, complete node-specific readable
reconstruction, independent R0 review, and accepted provenance/foundation/trust records.
`THEOREM-Z` also lacks accepted exact-root M0 closure, an immutable clean source snapshot,
empty-cache network-denied cold build, offline restoration, complete TCB/SBOM/license closure, two
independent signed clean-runner attestations, an independently implemented minimal verifier,
protected adversarial CI, a deterministic content-addressed bundle, and master acceptance.

The automation-provided `.lake` link points to shared warm state. During this release run,
`packages/flt-regular/.git/HEAD` was `ref: refs/heads/.invalid`; consequently `lake env which lean`
failed because the manifest package had no resolvable `HEAD`. The worker did not repair, fetch,
clone, update, or otherwise mutate that shared state. The narrow replay instead used the pinned Lean
4.29.0 executable and the already-present compiled dependency directories explicitly. That is real
nonrelease kernel evidence, not a valid pinned Lake closure or release build.

## Commands and results

All commands ran in this worker clone on 2026-07-15 (`Asia/Shanghai`). No `lake update`,
`lake build`, dependency clone/fetch, checkout, or network request was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets and ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0600` | 0 | Rank 638 remains planned, L0/rework-required, and theorem-incomplete. |
| `python3 Stage1_Instances/THM-M-0600/check_obligation_tree.py` | 0 | Eighteen frozen obligations and 44 typed edges passed; root remains open M3 with `M0600-T-ENGINE` open. |
| `python3 -I -B Stage1_Instances/THM-M-0600/check_validation.py` | 1 (expected) | The historical validation recipe failed closed because its phase-local worker packet is absent; it is also pinned to integrated base `7348dc64` and the prior DAG state. |
| `cd Formalizations/Lean && lake env which lean` | 1 (blocked) | Shared `flt-regular` has no resolvable `HEAD`; the worker did not mutate or fetch the missing pinned checkout. |
| `python3 -I -B Stage1_Instances/THM-M-0600/check_release.py` | 0 | Hash-bound current authority and receipts, replayed the narrow Lean surface with network denied using existing artifacts, and derived the exact blocked decisions. |
| `python3 -m json.tool` on the owned release JSON artifacts and root worker packet | 0 | All structured artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0600-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0600/check_release.py` | 0 | Checker syntax compiled without adding a generated owned file. |
| `git diff --check -- Stage1_Instances/THM-M-0600 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics. |

Retry requires a usable exact pinned dependency closure, dependency-legal master acceptance, full
authority/source/readable reconciliation, a premise-free positive-dimensional Morse engine and its
registered prerequisites, and a separately provisioned hermetic and independent release lane that
closes every remaining assurance gate.

Status boundary: this artifact self-tests only the truthful negative release decision. It supplies
no accepted root proof, `M0`, `E0/E1`, `H0`, `R0`, `AUDIT-Z`, `THEOREM-Z`, release, theorem
completion, or master acceptance.
