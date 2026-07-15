# THM-M-0673 validation-phase evidence

Item: `S56-M-0673-VALIDATION`. Base revision:
`c887c8e5d7afe589d4b90386654421a60e998f51`; base tree:
`7a1298612a32286e2a542ffc410cf4de9bb1fabd`.

## Validation scope

The node-scoped recipe copies `Statement.lean`, `ObligationTree.lean`,
`Proof.lean`, and `Validation.lean` into a fresh disposable directory. Every
Lean process runs with `--trust=0 -t0` inside Bubblewrap with outbound network
disabled, a cleared environment, a read-only host root, fixed locale/timezone,
and only the disposable directory writable. The replay uses existing pinned
compiled dependencies and is therefore warm nonrelease evidence, not a cold
empty-cache build.

`Validation.lean` imports neither `Proof` nor `ObligationTree`. It separately
adapts `FirstOrder.Language.Ultraproduct.sentence_realize` to the exact frozen
`LosSentenceTarget`. This checks the target boundary without reusing either
local proof root, but terminates at the same mathlib proof body. It is not a
second proof body or distinct-runner independent verification.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | pass, provisional | The statement, frozen conditional composition, both proof roots, and the separate exact adapter elaborate at trust zero. |
| Statement mutation boundary | pass | Removed nonemptiness, `Nat`-only index, existential sentence, and principal-only ultrafilter mutations remain distinct from the canonical target. |
| Placeholder/bodyless/unsafe | pass, scoped | Local source hygiene, `assert_no_sorry`, `#print sorries`, and two environment traversals find no placeholder, unexpected bodyless nonaxiom, or unsafe declaration. |
| Axiom observation | pass, provisional | Every covered proof and validation declaration reports exactly `propext`, `Classical.choice`, and `Quot.sound`; no accepted foundation profile exists. |
| Selected provenance | pass | All 11 manifest packages are at clean exact revisions; the mathlib remote/tree/blob/source/body/olean/license and tool executable hashes agree. |
| Recorded obligation recipes | fail closed / stale | The 28 frozen recipe IDs all invoke the same obligation-tree checker, which is intentionally bound to its historical phase base and exits at that assertion on current `HEAD`. |
| Dependency/state legality | fail closed | The proof receipt remains unaccepted. The authoritative instance and graph remain pre-proof at `H1/M3/R4`, with no accepted closed obligation. |
| Complete trust/provenance | fail closed | No accepted foundation policy, complete transitive provenance hash, compiler/bootstrap and compiled-artifact inventory, TCB, SBOM, or offline archive exists. |
| Hermetic release replay | fail closed | The checkout is dirty and the shared `.lake` cache is warm; there is no clean cold empty-cache offline restoration replay. |
| Independent verification | fail closed | The no-import adapter shares this worker, source snapshot, toolchain, and cache; there is no second signed independently provisioned runner or minimal release verifier. |

The narrow replay observes proof closure `5088` declarations / `192` modules
and validation closure `5086` declarations / `191` modules. Both have empty
bodyless-nonaxiom and unsafe reports. Only the five interfaces
`M0673-ROOT`, `M0673-T-ADAPTER`, `M0673-A-SENTENCE`, `M0673-A-FORMULA`, and
`M0673-A-BOUNDED` receive kernel-inhabitant observations. The 15 deeper
bounded-formula branches are source-mapped to one terminal body and are not
claimed as individually closed.

## Commands and results

All commands ran on 2026-07-15 (`Asia/Shanghai`). No `lake update`, `lake
build`, dependency clone/fetch, or `.lake` mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups; exactly 1546 uniform-L0 targets

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets at ranks 1 through 1546

python3 scripts/stage1_target.py show THM-M-0673
  exit 0: rank 717, planned, L0/rework_required, theorem_complete false

python3 -B Stage1_Instances/THM-M-0673/check_statement.py
  exit 0: exact expression matched; four structural mutations distinguished

bash Stage1_Instances/THM-M-0673/check_proof.sh
  exit 0: exact roots and frozen composition passed; exact allowed axioms;
  closure 5088/192, bodyless_nonaxioms=[], unsafe=[]

python3 -B Stage1_Instances/THM-M-0673/check_obligation_tree.py
  exit 1: expected current-HEAD freshness failure at the immutable historical
  base-revision assertion shared by all 28 recorded recipes

python3 -I -B Stage1_Instances/THM-M-0673/check_validation.py \
  --worker-packet .stage1-worker-selftest.json
  exit 0: isolated narrow replay, selected provenance, fail-closed historical
  recipe/state/trust/hermetic/independence decisions, receipt, and handoff passed

python3 -m json.tool Stage1_Instances/THM-M-0673/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0673/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

git diff --check -- Stage1_Instances/THM-M-0673 \
  .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

The first dependency-ordered failure is proof master acceptance. The first
validation-specific failure is the current-snapshot binding of the historical
obligation recipes. The first release failure is cold empty-cache offline
replay. The accepted vector remains `H1/M3/R4`; `audit_complete=false` and
`theorem_complete=false`. This packet claims no `M0-W`, `E0/E1`, `AUDIT-Z`,
`THEOREM-Z`, release, or master acceptance.
