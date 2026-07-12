# Anchor audit

Item: `S56-M-1024-ANCHOR_AUDIT`  
Audit date: 2026-07-12  
Base revision: `205d13cfc35c45883410c569709a91cb34edce16`

## Verdict

The pinned mathlib revision contains the characteristic-function, convolution, Dirac, probability
bound, and characteristic-function extensionality APIs needed by the statement, but no declaration
for infinite divisibility, Levy measures, Levy-Khintchine triplets, or the representation theorem.
The repo-local artifact remains a statement interface only.

A credible public Lean 4 candidate exists at `slink/LeanLevy`, immutable commit
`93b635fba23398bfb1f0db8d220f88172f6900b6`. It proves the real one-dimensional representation,
converse, characterization, and uniqueness. It is not the canonical theorem: it is restricted to
`Real`, uses the open truncation `abs x < 1`, and represents covariance by a nonnegative scalar.
The target quantifies over every finite dimension, uses the closed truncation `norm x <= 1`, and
uses a symmetric positive-semidefinite covariance operator. No checked transport bridges these
differences. The candidate is therefore `E3` discovery evidence, not `M1` or repo-local closure.
The conservative root classification is `M3`; theorem completion remains false.

## Immutable candidate record

| Field | Value |
|---|---|
| Project | `https://github.com/slink/LeanLevy` |
| Commit | `93b635fba23398bfb1f0db8d220f88172f6900b6` (2026-07-07) |
| Downloaded source archive SHA-256 | `585b9255907bc5db4c44f010acf98f7a9d608eea1d845b93f6938ff2437e4621` |
| Toolchain | `leanprover/lean4:v4.29.0-rc3` |
| mathlib pin | `8e096f85f9401f2c359b6708199c0402a980d921` |
| License | MIT |
| Upstream build | GitHub Actions run `28901735390`, job `85739880508`, success at the exact commit |
| Main declarations | `levyKhintchine_representation`, `levyKhintchine_converse`, `isInfinitelyDivisible_iff_exists_levyKhintchineTriple`, `existsUnique_levyKhintchineTriple` |
| Local integration | None; the project is not in `Formalizations/Lean/lake-manifest.json` |

The archive scan found no Lean command occurrences of `sorry`, `admit`, `axiom`, or `unsafe`.
That scan is defense in depth only: this worker did not fetch the dependency into `.lake`, replay
its build, derive its transitive declaration closure, or run `#print axioms`. Upstream CI is not an
independent repo-local kernel receipt.

## Search ledger

The audit searched the repo-local target and historical files, then every pinned mathlib Lean source
for `LevyKhintchine`, `levyKhintchine`, `IsInfinitelyDivisible`, `infinitely divisible`, and
`IsLevyMeasure`. All exact-token mathlib searches were empty. The checked nearby mathlib anchors are
listed in `AnchorAudit.lean` and elaborate at the repository pin.

Public GitHub repository searches used `levy khintchine lean`, `levy-khintchine lean4`,
`infinitely divisible lean theorem`, `LevyKhintchine language:Lean`, and
`Levy measure language:Lean`. Commit searches used both spellings of Levy-Khintchine plus
`infinitely divisible extension:lean`, `LevyKhintchine extension:lean`, and
`LevyMeasure extension:lean`. Search was unauthenticated and limited to public GitHub surfaces.

## Validation

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1024/Statement.lean` | 0 | Frozen target and structural mutations elaborate at the pinned local environment |
| `lake env lean ../../Stage1_Instances/THM-M-1024/AnchorAudit.lean` | 0 | Six nearby pinned mathlib declarations resolve with printed types |
| `rg -l -i 'LevyKhintchine\|IsInfinitelyDivisible\|infinitely divisible\|IsLevyMeasure' .lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No exact theorem-family token occurs in pinned mathlib |
| `python3 -m json.tool Stage1_Instances/THM-M-1024/anchor-audit.json` | 0 | Structured audit is valid JSON |
| syntax-oriented forbidden-token scan of the immutable external source archive | 1 | No command occurrence found; `rg` returns 1 for no matches |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 targets pass |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique L0/rework-required targets pass |
| `git diff --check -- Stage1_Instances/THM-M-1024 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors |

The next phase must treat the external real theorem as a possible specialized branch, not as the
all-dimensional root. Integration requires an explicit immutable dependency, compatible toolchain,
checked adapter, exact statement transport, kernel axiom report, and provenance closure.
