# THM-M-0041 anchor-audit validation

Item: `S56-M-0041-ANCHOR_AUDIT`

Base revision: `540472523b6c0717ed925193071191f81f62d6eb`

Base tree: `64b0c81418ef2c97b0250188444c672b9ae885d0`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

The bounded immutable inventory has five classified candidates. The narrow Lean probe checks the
expanded determinant target, its definitional equality to `Matrix.charpoly`, an exact wrapper around
`Matrix.aeval_self_charpoly`, a validator-only equality and wrapper for the actual declaration from
`Statement.lean`, and the axiom reports for the wrapper and both mathlib candidates. The exact pinned
route can support `M0-W` only after release-grade `E1`; this provisional worker check retains root
state `[H1, M3, R3]`. Neither audit nor theorem completion is claimed.

All Lean work used the automation-provided canonical `.lake` symlink read-only. No `lake update`,
`lake build`, dependency clone/fetch, or other `.lake` mutation ran. External repositories were
inspected through immutable raw/API responses and were not installed.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0041` | 0 | rank 1081, planned, L0/rework-required, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | preflight showed only the automation-created untracked `Formalizations/Lean/.lake` symlink; it was preserved |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | revision `8a1783...ea95`, tree `bdc39a...5c2b`, clean dependency worktree |
| local `rg` searches over repo-local Lean and every non-mathlib pinned package for Cayley-Hamilton, characteristic-polynomial, `charpoly`, and `aeval_self_charpoly` aliases | 1 (expected no eligible match) | no independent local or pinned-external candidate found |
| pinned mathlib source and Git-history inspection for `Matrix.aeval_self_charpoly`, definitions, dependencies, blobs, origin commit, and license | 0 | exact terminal body and immutable provenance recorded in `anchor-audit.json` |
| Sourcegraph queries for `Matrix.aeval_self_charpoly`, `CayleyHamilton`, literal Cayley-Hamilton, and normalized equation forms, with forks/archives included | 0 | bounded results found mathlib, Atlas special-case, automath consumer, and historical mathlib3 surfaces; response hashes recorded |
| GitHub REST repository searches for Cayley-Hamilton/charpoly Lean repositories | 0 | both returned HTTP 200 with zero repository-name results; response hashes recorded |
| GitHub REST code search for `Matrix.aeval_self_charpoly language:Lean` | 0 request | HTTP 401 authentication blocker; response SHA-256 `b7dbd173...65e29e` |
| immutable raw/API inspection of `facebookresearch/atlas-lean@34ffed3...` | 0 | `Matrix.cayleyHamilton_fin_two` has a source-local strict-special-case body but was not installed or kernel-checked here; the file also has unrelated later placeholders; source/toolchain/manifest/license hashes recorded |
| immutable raw/API inspection of `the-omega-institute/automath@f76f46f...` | 0 | recurrence theorem consumes mathlib's matrix theorem at an older pin; no independent terminal body |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0041/Statement.lean)` | 0 | prerequisite exact target re-elaborated |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0041/AnchorAudit.lean)` | 0 | exact wrapper and transport checked; all three axiom reports were `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `4d6423e2...d89f7` |
| `python3 -B Stage1_Instances/THM-M-0041/check_anchor_audit.py` | 0 | immutable pins/blobs, five-candidate ledger, actual canonical declaration, exact route, external boundary, receipt, packet, and Lean replay agreed |
| `python3 -m json.tool` separately on `anchor-audit.json`, `anchor-audit-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | all structured artifacts parsed |
| prohibited-construct scan over `AnchorAudit.lean` and the exact/related pinned mathlib files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `unsafe`, or `opaque` token in the scoped proof sources |
| `git diff --check -- Stage1_Instances/THM-M-0041 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Known limitations

Search coverage is bounded rather than globally exhaustive. The statement prerequisite and this
node still require master acceptance. The obligation registry, proof composition, full transitive
declaration/provenance/trust and TCB closure, `H0`, `R0`, hermetic replay, independent validation,
`AUDIT-Z`, and theorem completion remain open.

## Exact discovery commands

The local searches were:

```bash
rg -n -i 'cayley[- _]?hamilton|aeval_self_charpoly' Formalizations/Lean/AwesomeTheorems Stage1_Instances --glob '*.lean' --glob '!Stage1_Instances/THM-M-0041/**'
rg -n -i 'cayley[- _]?hamilton|characteristic[ _-]?polynomial|aeval_self_charpoly|eval_charpoly|charpoly.*(aeval|eval)|(aeval|eval).*charpoly' Formalizations/Lean/.lake/packages/{Cli,LeanSearchClient,Qq,aesop,batteries,checkdecls,flt-regular,importGraph,plausible,proofwidgets} --glob '*.lean'
rg -n -i 'cayley[- _]?hamilton|aeval_self_charpoly|eval_self_charpoly' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'
```

The first two exited `1` with no matches. The mathlib search exited `0` and located the exact matrix
theorem, related LinearMap theorem, finitely-generated-module support, and downstream uses.

Each Sourcegraph request used the following form, substituting the exact query recorded in
`anchor-audit.json`:

```bash
curl -L --fail --silent --show-error --max-time 60 --get https://sourcegraph.com/search/stream --data-urlencode 'q=<recorded-query>' --data-urlencode v=V3
```

All four exited `0`; exact counts and response SHA-256 values are in the ledger. GitHub searches
used:

```bash
curl -L --silent --show-error --max-time 60 'https://api.github.com/search/repositories?q=%22Cayley-Hamilton%22+Lean&per_page=30'
curl -L --silent --show-error --max-time 60 'https://api.github.com/search/repositories?q=charpoly+Lean4&per_page=30'
curl -L --silent --show-error --max-time 60 'https://api.github.com/search/code?q=Matrix.aeval_self_charpoly+language%3ALean&per_page=30'
```

The transport process exited `0` for each request; HTTP responses were `200`, `200`, and `401`.
Immutable source inspection used the following URLs with
`curl -L --fail --silent --show-error --max-time 60`:

```text
https://raw.githubusercontent.com/facebookresearch/atlas-lean/34ffed396f376454c1a9b297f3fd74c5c801fb50/Atlas/EllipticCurves/code/TateModuleTrace.lean
https://raw.githubusercontent.com/facebookresearch/atlas-lean/34ffed396f376454c1a9b297f3fd74c5c801fb50/lean-toolchain
https://raw.githubusercontent.com/facebookresearch/atlas-lean/34ffed396f376454c1a9b297f3fd74c5c801fb50/lake-manifest.json
https://raw.githubusercontent.com/facebookresearch/atlas-lean/34ffed396f376454c1a9b297f3fd74c5c801fb50/LICENSE
https://raw.githubusercontent.com/the-omega-institute/automath/f76f46f07a1a48d5c12a20c2f8d366bb9df9330d/lean4/Omega/Zeta/SyntaxTraceLinearRecurrence.lean
https://raw.githubusercontent.com/the-omega-institute/automath/f76f46f07a1a48d5c12a20c2f8d366bb9df9330d/lean4/lean-toolchain
https://raw.githubusercontent.com/the-omega-institute/automath/f76f46f07a1a48d5c12a20c2f8d366bb9df9330d/lean4/lake-manifest.json
https://raw.githubusercontent.com/the-omega-institute/automath/f76f46f07a1a48d5c12a20c2f8d366bb9df9330d/LICENSE
```

All eight raw requests exited `0`. Response digests, revisions, trees, and manifest pins are recorded
per candidate. Response files existed only under `/tmp` and are not public artifacts or dependency
inputs.
