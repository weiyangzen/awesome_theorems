# Intake validation

Validation date: 2026-07-13 (Asia/Shanghai).
Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2`.
Base tree: `9d7c8fe49a4c859d90f3069dc47973ffc5ced768`.

The worker reused the automation-provided canonical `.lake` symlink read-only. No `lake update`,
`lake build`, dependency clone/fetch, package mutation, theorem declaration, or proof was run. This
dirty worker validation is provisional nonrelease evidence.

## Preflight and discovery

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1596` | 0 | rank 1216, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree above |
| `git blame -L 11756,11761 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref query for DOI `10.1017/CBO9780511546891` | 0 | confirmed the broad Goldreich monograph bibliography lead; response SHA-256 `9ffc5ba9f2045ca1a5a9544c0738a29f42565d468e5468170b37b08121b57688`; no target proposition selected |
| bounded exact-topic search over repo-local Lean and pinned mathlib | 0 | only unrelated lexical matches; no source-selected cryptography declaration found |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned package worktree remained clean |

## Final scoped checks

| Command | Exit | Result |
|---|---:|---|
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1596/IntakeProbe.lean)` | 0 | six adjacent uniform-probability and computability APIs elaborated; output SHA-256 `0f7c39ac3acae54d8f5b6232ce53213e48a59f8383571979e5587d36155737f9`; no target declaration checked |
| `python3 -m json.tool` on all owned JSON files and `.stage1-worker-selftest.json` | 0 | all JSON documents parse |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1596-pycache python3 -m py_compile Stage1_Instances/THM-M-1596/check_intake.py` | 0 | scoped validator compiles without adding generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-1596/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | authority identity, planned H5/M4/R4 boundary, null target, artifact inventory, source hashes, handoff, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1596/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-1596/IntakeProbe.lean` | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1596 .stage1-worker-selftest.json` plus new-file hygiene checks | 0 | no whitespace, final-newline, CR, NUL, or trailing-space defect |

## Known downstream failures

- No stable mathematical proposition is selected. Primitive/protocol syntax, algorithms, spaces,
  computational and adversarial model, security game, probability and advantage, assumptions,
  binders, exact conclusion, reduction, asymptotics, boundary cases, pinpoint primary source, and
  independent reviews remain open.
- No canonical Lean expression, expression or environment hash, minimal imports, checked alternate
  encoding, or statement mutation certificate exists.
- The API probe establishes adjacent substrate only. It does not locate or validate a
  source-identical proof and does not upgrade the root from `M4`.
- Complete anchor and proof-body audit, obligation registry and typed graphs, proof, composition
  and trust checks, readable reconstruction, hermetic replay, deterministic evidence bundle,
  independent release verification, and master acceptance remain open.

These failures block statement and theorem execution but do not invalidate a truthful,
self-tested `planned` intake. Only the integration lane may accept the provisional worker receipt.
