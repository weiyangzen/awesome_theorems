# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation ran on 2026-07-13 in
an isolated Stage1 worker clone (Asia/Shanghai).

Validation is limited to target-set consistency, dossier structure and scope invariants,
repository-source provenance, pinned environment identity, a narrow Lean API probe, proof-escape
hygiene, and whitespace. The repository gloss is not one exact proposition, so elaborating a
purported canonical target would invent missing mathematics. `IntakeProbe.lean` checks only
adjacent singular-homology, trace, and fixed-point APIs and supplies no statement, anchor, source,
or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0641` | 0 | rank 1058, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 4748,4753 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref title/author query for Lefschetz's 1926 paper | 0 | bibliographic metadata identifies *Intersections and transformations of complexes and manifolds*, Trans. AMS 28 (1926), 1-49, DOI `10.1090/S0002-9947-1926-1501331-3`; no proposition or H0 evidence admitted |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...2d81` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0641/IntakeProbe.lean)` | 0 | six adjacent pinned singular-chain, singular-homology, topological-singular-set, trace, and fixed-point interfaces elaborated; no target declaration |
| bounded `rg` topic search over repo-local and pinned mathlib `*.lean` | 0 | only unrelated Lefschetz-principle and neighboring legacy-topic hits; no classical target declaration found; intake discovery only, not an exhaustive anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all four structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0641-pycache python3 -m py_compile Stage1_Instances/THM-M-0641/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-0641/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and execution-item identity, planned H1/M4/R4 boundary, null target, exact artifact inventory, handoff, and six open tasks agree |
| prohibited Lean proof-escape scan over `Stage1_Instances/THM-M-0641` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0641 .stage1-worker-selftest.json` plus scoped byte-level hygiene assertions | 0 | no whitespace diagnostics; all ten changed files have final LF newlines, no CR/NUL bytes, and no trailing spaces or tabs |

## Known downstream failures

- No immutable primary theorem/page and incorporated definition chain has been accepted. Space and
  map categories, (co)homology, coefficients, finiteness, alternating trace, implication versus
  fixed-point formula, translation, corrections, errata, and independent review are open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  transport, or statement mutation test exists.
- The bounded Lean search is not the required immutable anchor audit. Discovery protocol, terminal
  body provenance, trust and axiom closure, obligation registry, typed graphs, proof, composition,
  readable reconstruction, hermetic replay, deterministic bundle, and independent verification
  remain open.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose purpose is to freeze the source and scope boundary and
open DAG. Only the integration lane may accept this provisional worker receipt.
