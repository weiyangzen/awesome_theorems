# Intake validation

Base revision: `c2467750f2cdb3960045c83e819d96687253303d` (tree
`0f79eb697267dc28b29d41a1e282f319d758a2ac`). Validation ran on 2026-07-13 in
an isolated Stage1 worker clone (Asia/Shanghai).

Validation is limited to target-set consistency, dossier structure and scope invariants,
repository-source provenance, pinned environment identity, a narrow Lean API probe, proof-escape
hygiene, and whitespace. The repository gloss is not one exact proposition, so elaborating a
purported canonical target would invent missing mathematics. `IntakeProbe.lean` checks only
adjacent Euclidean-space, closed-ball, continuity, maps-to, and fixed-point APIs and supplies no
statement, anchor, source, or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0640` | 0 | rank 1057, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 4741,4746 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error --max-time 30 'https://api.crossref.org/works?query.bibliographic=%C3%9Cber%20Abbildung%20von%20Mannigfaltigkeiten%20Brouwer&rows=3'` followed by JSON field selection | 0 | bibliographic metadata identifies the 1911 paper, DOI `10.1007/BF01456931`, and same-title one-page 1912/1921 records treated only as possible correction leads; no proposition or H0 evidence admitted |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...2d81` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0640/IntakeProbe.lean)` | 0 | eight adjacent pinned Euclidean-space, closed-ball, continuity, maps-to, and fixed-point interfaces elaborated; no target declaration |
| bounded `rg` topic search over repo-local and pinned mathlib `*.lean` | 0 | unrelated fixed-point and Brouwerian-logic hits; no terminal Brouwer declaration found; intake discovery only, not an exhaustive anchor audit |
| `python3 -m json.tool Stage1_Instances/THM-M-0640/instance.json` | 0 | instance manifest is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0640/task-dag.json` | 0 | open task DAG is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0640/intake-receipt.json` | 0 | provisional intake receipt is valid JSON |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | worker self-test handoff is valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0640-pycache python3 -m py_compile Stage1_Instances/THM-M-0640/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-0640/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and execution-item identity, planned H1/M4/R4 boundary, null target, exact artifact inventory, handoff, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry|admit)\b|\bsorryAx\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]' Stage1_Instances/THM-M-0640` | 1 | expected no-match result; no prohibited proof escape in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-0640 .stage1-worker-selftest.json` plus scoped byte-level hygiene assertions | 0 | no whitespace diagnostics; all ten changed files have final LF newlines, no CR/NUL bytes, and no trailing spaces or tabs |

## Known downstream failures

- No immutable primary theorem/page and incorporated definition chain has been accepted. The
  paper, correction records, exact proposition, assumptions, translation, errata, and independent
  review are open.
- Closed-ball and Euclidean models, dimension, center/radius, self-map and continuity encodings,
  conclusion, boundary cases, and the identity/transport relationship to `THM-M-0319` and
  `THM-M-0636` remain open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  transport, or statement mutation test exists.
- The bounded Lean search is not the required immutable anchor audit. Discovery protocol, terminal
  body provenance, trust and axiom closure, obligation registry, typed graphs, proof, composition,
  readable reconstruction, hermetic replay, deterministic bundle, and independent verification
  remain open.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose purpose is to freeze the source and scope boundary and
open DAG. Only the integration lane may accept this provisional worker receipt.
