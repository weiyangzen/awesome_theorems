# Intake validation

Base revision: `fd0fab2ab7f4f514a5cc625bbce92879e718ba13`; base tree:
`4116d53bcf2573069e4b67205353fe3469dbe7bd`.

This validation covers target membership, the planned dossier and open task DAG, catalog and
Stage0-only duplicate boundaries, historical source disambiguation, exact owned-file invariants,
and a narrow pinned Lean substrate probe. Because the catalog does not select one proposition, no
canonical target, expression hash, mutation result, source acceptance, transport, or proof is
claimed. The automation-provided canonical `.lake` symlink and pinned artifacts were used
read-only; no dependency update, build, clone, fetch, or `.lake` mutation was performed. The
pre-existing untracked symlink makes this nonrelease worker evidence.

## Commands and results

All commands ran from the worker clone root on 2026-07-13 (Asia/Shanghai), except where a `cwd` is
shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0763` | 0 | rank 1349; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; preserved read-only |
| `git rev-parse HEAD` and `git rev-parse 'HEAD^{tree}'` | 0 each | base revision and tree recorded above |
| `git blame -L 5619,5624 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| repository crosswalk search for `THM-M-0763`, `THM-C-0151`, the literal glosses, neighboring targets, and exact-topic Lean terms | 0 | one covered target, one Stage0-only parallel record, proposition-changing variants, and neighbor exclusions confirmed; no evidence transferred |
| Crossref metadata queries for DOI `10.1109/TIT.1956.1056813` and DOI `10.1016/S0019-9958(59)90362-6` | 0 each | confirmed the 1956 and 1959 bibliographic fields; metadata only |
| author-hosted 1956 paper retrieval plus `pdfinfo` and `pdftotext -layout` | 0 | inspected journal pages 114 and 116-119, including Theorem (27) on page 118 and its continuing proof; temporary 1,532,335-byte PDF SHA-256 `a3bfc971...e1799`; no source acceptance or H0 credit |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision `8a178386...eea95`, tree `bdc39a31...c2b`; package status clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0763/IntakeProbe.lean)` | 0 | nine adjacent pinned formal-language, regular, context-free, computability, and recursive-enumerability interfaces elaborated; output SHA-256 `723b5c8d...a5417c`; no target theorem was stated |
| bounded exact-topic `rg` over pinned mathlib and repo-local Lean | 1 (expected no match) | no `Chomsky`, context-sensitive/unrestricted grammar hierarchy, or type-0/type-1 declaration found; not a global absence claim or downstream anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0763-pycache python3 -m py_compile Stage1_Instances/THM-M-0763/check_intake.py` | 0 | scoped validator compiles without writing generated files into the owned path |
| `python3 -B Stage1_Instances/THM-M-0763/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, H5/M4/R4 planned boundary, null target, source hashes, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0763/check_intake.py` | 0 | public replay mode passes without requiring the scheduler-only root packet |
| prohibited-construct `rg` over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check` loop, plus `git diff --check -- Stage1_Instances/THM-M-0763 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics; no-index exit 1 for a new file was treated as a difference, not an error |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0763-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted receipt. Exact source selection and independent review,
canonical Lean elaboration and mutation tests, formal-anchor and obligation freezes, typed graphs,
proof, composition, trust closure, source-faithful readable reconstruction, hermetic replay,
deterministic release bundling, independent verification, and master acceptance remain open. They
prevent theorem completion but do not invalidate the planned intake.
