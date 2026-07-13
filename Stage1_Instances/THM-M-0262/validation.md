# Intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, catalog
and neighboring-target provenance, pinned environment identity, a narrow Lean API probe, a bounded
local source-name search, proof-escape hygiene, and whitespace. The catalog wording is not a
proposition, so elaborating a purported canonical target would invent missing mathematics.
`IntakeProbe.lean` therefore checks only possible substrate; it introduces no theorem and supplies
no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0262` | 0 | rank 1270, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 1885,1890 -- Docs/researches/math_theorems.md` and `git blame -L 10474,10479 -- Docs/researches/math_theorems.md` | 0 | both uncited catalog records originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; the latter separately names no wandering domains |
| Numdam official-record and Crossref inspection for DOI `10.24033/asens.1446` | 0 | Mañé-Sad-Sullivan, *On the dynamics of rational maps*, 16(2) (1983), 193-217, confirmed as a source-family lead; the catalog supplies no theorem locator or statement identity |
| Crossref inspection for DOI `10.1007/BFb0061443` | 0 | Sullivan, *Conformal dynamical systems*, pages 725-752, confirmed as broad source context; no root selected |
| Annals official-page and Crossref inspection for DOI `10.2307/1971308` | 0 | Sullivan's 1985 wandering-domain paper bibliography confirmed; not selected because `THM-M-1434` separately owns that root, and the official page exposes no theorem text |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0262/IntakeProbe.lean)` | 0 | eleven pinned rational-function, complex, one-point, meromorphic, component, iterate, and periodic-point APIs elaborated; complete output SHA-256 `416ae386be218d8d2bfb2725fd6c9a8407d65d4352875bd90921d08d4b931e27`; no target declaration |
| bounded Sullivan/wandering/Julia/Fatou/rational-dynamics/complex-dynamics search over repo-local and pinned mathlib `*.lean` | 1 | expected no-match result; intake discovery only, not an exhaustive formal-anchor audit |
| `python3 -m json.tool` on all owned JSON files and `.stage1-worker-selftest.json` | 0 | instance, open task DAG, provisional receipt, and worker handoff are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0262-pycache python3 -m py_compile Stage1_Instances/THM-M-0262/check_intake.py` | 0 | scoped intake validator compiles without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0262/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and authoritative-DAG identity, planned H5/M4/R4 boundary, separate no-wandering root, null target, exact inventory, hashes, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0262/check_intake.py` | 0 | public replay mode passes without requiring the scheduler-only packet |
| prohibited Lean proof-escape scan over `Stage1_Instances/THM-M-0262` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0262 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; per-file no-index checks cover untracked artifacts |

## Known downstream failures

The received catalog wording is not a stable proposition. An approved truth-valued target
correction, immutable pinpoint primary theorem, complete definition/assumption/conclusion/proof and
errata crosswalk, relationship to `THM-M-1434`, and independent source review remain open. So do the
canonical Lean target and minimal imports, expression and environment fingerprints, checked
transports, statement mutations, exhaustive anchor audit, discovery and obligation freezes, typed
graphs, proof and composition, source/readability/trust closure, hermetic replay, deterministic
evidence bundle, independent release verification, and master acceptance.

These failures block ordinary theorem execution and completion. They do not invalidate a truthful,
self-tested `planned` intake whose assigned deliverable is the dossier, scope map, and
source-statement crosswalk. Only the integration lane may accept the provisional worker receipt.
