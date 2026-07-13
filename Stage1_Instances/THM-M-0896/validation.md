# Intake validation

Base revision: `0c019b7194c9c43fa5f683fa82d637a0b275410d`; base tree:
`43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, scope and neighbor discrimination, JSON and scoped invariants, a narrow pinned Lean
substrate probe, a bounded repo-local and mathlib search, prohibited-construct hygiene, and
whitespace. It does not validate a canonical theorem statement or proof because the catalog
supplies no stable truth-valued proposition.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The catalog's exact six-line record has SHA-256
`1b8a930087f9113a94a3f23ade1237d1e2a829af751321617d6826e7b78eb2fb` and contains no citation.
The MathWorld finite-geometry page was inspected only to confirm that finite plane geometry already
splits into projective and affine families. Repeated responses had different bytes, so no response
digest is admitted. Two stable technical references were also inspected: Brouwer and Van
Maldeghem's 452-page *Strongly regular graphs* monograph (SHA-256 `fa73d72...fd9289d`) and van Dam,
Koolen, and Tanaka's 156-page EJC distance-regular-graphs survey (SHA-256
`ef07467d...4336de6`). They distinguish point/collinearity, point-line incidence, polar, and other
geometry-derived graph families with different conclusions. None is catalog provenance, a selected
exact theorem, an admitted primary proof packet, a complete premise/proof/errata mapping, or an
independently reviewed H0 source.

## Environment fingerprint

- Platform: Linux x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless another
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0896` | 0 | rank 1445; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6558,6563 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git rev-parse bcf3f9fa79ab8c2b6610c9875668c2589b35b74f:Docs/researches/math_theorems.md` | 0 | source-record blob `5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf` |
| repeated bounded retrieval of `https://mathworld.wolfram.com/FiniteGeometry.html` | 0 | page distinguished projective and affine finite plane geometries; response bytes varied, so no digest or immutable evidence was admitted |
| retrieval and bounded inspection of Brouwer/Van Maldeghem, *Strongly regular graphs* | 0 | 452-page, 2,902,008-byte author PDF; SHA-256 `fa73d72e...fd9289d`; family-discrimination evidence only |
| retrieval and bounded inspection of van Dam/Koolen/Tanaka, EJC DS22 | 0 | 156-page, 1,391,818-byte journal PDF; SHA-256 `ef07467d...4336de6`; family-discrimination evidence only |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, x86_64-unknown-linux-gnu, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e` (Lean 4.29.0); no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision/tree above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0896/IntakeProbe.lean)` | 0 | thirteen incidence-configuration, projective-plane, cardinality, and simple-graph APIs elaborated; output SHA-256 `fc97a4da840d8e622a69575f8127be8c2b56f163c4604f55f39a4cb7bebb063a` |
| `rg -n -i --glob '*.lean' '\b(IncidenceGraph\|LeviGraph\|CollinearityGraph\|PointGraph\|PolarityGraph\|ProjectivePlane.*(SimpleGraph\|Graph)\|SimpleGraph.*ProjectivePlane\|FiniteGeometry)\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 (expected no match) | no exact named bridge found; intake discovery only, not an exhaustive anchor audit or global absence claim |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `python3 -c "import ast, pathlib; ast.parse(pathlib.Path('Stage1_Instances/THM-M-0896/check_intake.py').read_text(encoding='utf-8')); print('ast parse: ok')"` | 0 | checker parses; no bytecode written |
| `python3 -B Stage1_Instances/THM-M-0896/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H5/M4/R4 state, null target, current source hashes, neighbor boundaries, inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0896/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --no-index --check /dev/null <path>` run separately for each of the nine owned files and `.stage1-worker-selftest.json` | 1 each (expected new-file difference) | all ten commands emitted no whitespace diagnostics |
| `git diff --check -- Stage1_Instances/THM-M-0896 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; no-index checks cover untracked files |

## Known downstream failures

- The title and gloss do not select one stable proposition. No repository-selected primary source,
  exact finite geometry, graph construction, relationship direction, theorem, incorporated
  definitions, assumptions, proof boundary, correction/errata decision, or independent review
  exists.
- Point/line/block and incidence representation, graph category, order/dimension/field parameters,
  exact conclusion, quantifier order, and boundary cases remain open.
- Reconciliation with neighboring distance-regular, strongly regular, design-theory, and
  Bose-Shrikhande-Parker targets remains open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation test exists.
- Discovery protocol, formal anchor audit, obligation registry, typed graphs, proof, composition,
  provenance and trust closure, readable reconstruction, hermetic replay, deterministic bundle,
  and independent release validation remain open.
- Master acceptance remains pending. `audit_complete` and `theorem_complete` remain false.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0896-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. All six downstream tasks remain open. No exact
statement, proof body, H0/M0/R0, audit completion, theorem completion, or release claim is made.
