# Intake validation

Item: `S56-M-0866-INTAKE`

Base revision: `748243faadc15828fb087059337fd05b7be9fdeb`

Base tree: `e46d642646f80980838b6f016f5d69b817bd464d`

Validation date: 2026-07-13 (Asia/Shanghai)

This validation covers target membership, the planned dossier and exact open task DAG, catalog and
source-lead provenance, JSON and scoped invariants, a narrow pinned Lean substrate probe, bounded
repo-local and mathlib discovery, prohibited-construct hygiene, and whitespace. It does not validate
a canonical theorem statement or proof because source-era scope, exact definitions, and the
source-faithful Lean expression remain open.

The initial working tree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

Crossref and Springer metadata identify K. Wagner, *Über eine Eigenschaft der ebenen Komplexe*,
*Mathematische Annalen* 114(1), 570-590 (1937), DOI `10.1007/BF01594196`. The zbMATH API identifies
EuDML record `159935` and a historical JFM review by Erika Pannwitz. The review describes Wagner's
edge-deletion/endpoint-identification convention, a structural basis result and four-color
connection, and flags an incorrect final sentence in the introduction. It is secondary evidence,
not a substitute for the primary theorem statement. Semantic Scholar reports no open-access PDF.

The primary full text was not lawfully available for pinpoint inspection. No complete edition was
added to the repository, no exact source proposition or incorporated definition was transcribed,
and no modern `K5`/`K3,3` graph-minor equivalence or correction boundary received independent
review. The source classification is therefore `H1`, not `H0`.

## Environment fingerprint

- Platform: Linux 7.0.0-27-generic, x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0866` | 0 | rank 1420; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6348,6353 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref DOI metadata query | 0 | article identity, German language, journal, volume, pages, date, and DOI confirmed; response SHA-256 `68b6a7...1985` |
| zbMATH API DOI search | 0 | Zbl/JFM records, EuDML locator, historical contraction/basis/four-color review, and correction warning inspected; response SHA-256 `418c57...36f7`; secondary evidence only |
| Semantic Scholar DOI lookup | 0 | bibliographic identity confirmed; open-access PDF status `CLOSED`; response SHA-256 `a84362...b6a3` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0866/IntakeProbe.lean)` | 0 | seven adjacent graph constructor/copy/induced APIs elaborated; output SHA-256 `54da59...70a3`; no graph-minor/planarity definition or target declaration |
| bounded exact-topic `rg` over pinned SimpleGraph and repo-local Lean | 0 | only a planar-graphs TODO bullet in `SimpleGraph/Coloring.lean`; no target-specific interface or theorem; intake discovery only |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `compile` of `Stage1_Instances/THM-M-0866/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0866/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, planned H1/M4/R4 boundary, null target, source and dependency pins, exact inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0866/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the API probe | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| byte/newline/trailing-whitespace check plus `git diff --check` | 0 | all ten changed files pass; no whitespace diagnostics |

## Known downstream failures

- No immutable complete primary edition, pinpoint proposition, accepted source-era definitions,
  premise/proof boundary, correction reconciliation, modern forbidden-minor transport, or
  independent source review exists.
- Graph class, abstract planarity, graph-minor deletion/contraction relation and orientation,
  `K5`/`K3,3` encodings, ordered binders, exact conclusion, and boundary cases are not frozen.
- Pinned mathlib has useful adjacent finite simple-graph APIs but no located graph-minor relation or
  planarity predicate. No canonical Lean expression, minimal-import certificate,
  expression/environment fingerprint, checked alternate encoding, or required mutation exists.
- Exhaustive formal anchor audit, discovery and obligation freezes, typed graphs, proof,
  composition, readable reconstruction, trust closure, hermetic replay, deterministic bundle,
  independent release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze scope and open the
downstream DAG. Only the integration lane may accept the provisional worker receipt.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0866-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, H0 source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.
