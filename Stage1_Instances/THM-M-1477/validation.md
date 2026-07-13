# THM-M-1477 intake validation

## Scope

This record validates only the `planned` dossier, scope map, source-statement crosswalk, open task
DAG, bibliographic source-lead metadata, and discovery-only pinned Lean API probe. It does not
validate an exact mathematical statement, an A-stability definition, a numerical method, the
Dahlquist order barrier, a proof, an accepted receipt, audit completion, or theorem completion.

The worker tree was nonrelease-dirty throughout: the canonical `.lake` link was already untracked,
and this intake's owned artifacts plus the root self-test packet were new. No dependency content,
authority file, generated checklist, execution-DAG state, or other target path was modified.

## Environment

- Repository base: `974415b7b5b44717c9e7aacd8c838c9489ce27f4`
- Base tree: `d9e4d272bf64ef22b1ff43831862394b0135ada3`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- mathlib tree: `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- Platform: Linux `7.0.0-27-generic`, `x86_64`
- Timezone/date: Asia/Shanghai, 2026-07-13

Crossref metadata for DOI `10.1007/BF01963532` was observed with a bounded HTTP request and had
SHA-256 `0f38599bb26247fa36b8f2c3269f51f5896988dff3da3c12c4676d9797db197f`. It confirmed
Dahlquist, the article title, BIT volume 3 issue 1, March 1963, and pages 27-43. Semantic Scholar
confirmed the same bibliographic identity and reported the full text closed. No external source was
vendored; these are mutable, nonrelease discovery observations.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1477` | 0 | rank 1154, planned, L0/rework_required, no legacy slot, theorem_complete false |
| `git status --short --untracked-files=all` at preflight | 0 | only the pre-existing untracked canonical `.lake` link existed before this intake; preserved |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 10777,10782 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded Crossref and Semantic Scholar observation for DOI `10.1007/BF01963532` | 0 | matching Dahlquist 1963 primary-source lead identified; bibliographic discovery only |
| exact case-sensitive topic searches over pinned mathlib and repo-local Lean | 1 expected for every query | no `Dahlquist`, `absolute stability`, `stability function`, `stability region`, `linear multistep`, `A-stability`, or `A-stable` occurrence; not an absence proof |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1477/IntakeProbe.lean` | 0 | five adjacent pinned APIs elaborated; two axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem introduced |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1477-pycache python3 -m py_compile Stage1_Instances/THM-M-1477/check_intake.py` | 0 | scoped validator parses without writing cache files under the owned path |
| `python3 -B Stage1_Instances/THM-M-1477/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, null target, H5/M4/R4 boundary, source and pin hashes, receipt/packet agreement, exact inventory, and six open tasks agree |
| prohibited-construct `rg` over `IntakeProbe.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` token |
| `git diff --check -- Stage1_Instances/THM-M-1477 .stage1-worker-selftest.json` plus per-new-file no-index whitespace checks | 0 | no whitespace diagnostics |

The final structural and whitespace results are recorded after receipt and worker-packet creation.
The Lean probe's exact combined-output SHA-256 is
`0630a4c5230aa74b68c6b087c280d11097cfca018d870473286d9f8a5d5dfc9c`.

## Known failures and boundary

Master acceptance is pending. The catalog label still lacks a selected exact proposition. Source
admission, independent source/numerical-stability review, formal target and mutation certificate,
exhaustive anchor audit, obligation registry, typed graphs, proof, composition, trust closure,
readable reconstruction, hermetic replay, deterministic bundle, and independent verification
remain open.

Verdict: `no_state_change`. This self-tested worker proposal may be handed off as `[_]`; it remains
unfinished and unaccepted. `audit_complete=false` and `theorem_complete=false`.
