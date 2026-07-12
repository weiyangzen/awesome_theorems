# Anchor-audit validation

Item: `S56-M-0645-ANCHOR_AUDIT`  
Validation date: 2026-07-12  
Base revision: `5c0a4aafae91449d16f106bf558339d46b60f39b`

Commands ran in the worker clone. The existing canonical `.lake` artifacts were only read; no Lake
update, build, clone, fetch, or dependency mutation command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0645/check_anchor_audit.py` | 0 | receipt invariants, exact statement hash linkage, local bridge boundary, manifest pin, and local mathlib checkout revision accepted; receipt SHA-256 `d61ebc24f1e884f6675d0dd87bae9607d54e650e0a540475db3db5608c7e1506` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0645/Statement.lean)` | 0 | the frozen `CompletenessTarget` re-elaborated and printed |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i --glob '*.lean' 'theorem .*complete|lemma .*complete|def .*complete|satisfiable.*consistent|consistent.*satisfiable|provable' Formalizations/Lean/.lake/packages/mathlib/Mathlib/ModelTheory Formalizations/Lean/.lake/packages/mathlib/Mathlib/Logic` | 0 | only model-theoretic `IsComplete` and unrelated uses found; no syntactic completeness terminal |
| `git ls-remote https://github.com/FormalizedFormalLogic/Foundation.git HEAD` | 0 | immutable audit revision resolved as `87d4dd68835a6c1eb8448b9c392d9ca51fe08d63` |
| `curl -L --fail --silent https://raw.githubusercontent.com/FormalizedFormalLogic/Foundation/87d4dd68835a6c1eb8448b9c392d9ca51fe08d63/Foundation/FirstOrder/Completeness/CounterModel.lean \| sha256sum` | 0 | `daa486fd8f6f8adaf34972aa61ef7ccaa93aa239556ec95def5bf57af09492d5` |
| same immutable source piped to `rg -n -C 5 'theorem Proof.complete|theorem Proof.small_complete|theorem Proof.complete_iff'` | 0 | located terminal declarations at source lines 241, 251, and 253 |
| same immutable source piped to `rg -n '\\bsorry\\b|\\badmit\\b'` | 1 | no textual placeholder occurrence; this is not a transitive axiom audit |
| `python3 -m json.tool Stage1_Instances/THM-M-0645/anchor-audit.json` | 0 | valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets accepted |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `git diff --check -- Stage1_Instances/THM-M-0645` | 0 | no whitespace errors |

The GitHub unauthenticated code-search API separately returned HTTP 403 due to rate limiting. This
is recorded as a search limitation, not hidden as success. The project's immutable first-party
links and source were still inspectable. Foundation was not built because it is absent from the
pinned dependency closure and uses Lean/mathlib 4.31; fetching it would violate this worker's
dependency-mutation boundary.

Known downstream failures are the missing exact transport or local proof, Foundation dependency
integration, terminal transitive trust/provenance inspection, obligation tree, proof, hermetic
validation, and independent release review. They do not invalidate this truthful candidate audit,
but they prevent M0 and theorem completion.
