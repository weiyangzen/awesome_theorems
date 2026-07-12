# Intake validation

Base revision: `ffe94ac84965dc19f4923f88b7566072ddee37ae` (tree
`876a17f277d84dcf06ca672e5cd351edaa294495`). Validation ran on 2026-07-12 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, pinned
environment identity, a narrow Lean API probe, bounded local name searches, proof-escape hygiene,
and whitespace. The source record is not a proposition, so elaborating a purported canonical Lean
target would invent missing mathematics. `IntakeProbe.lean` therefore checks only possible
substrate; it introduces no theorem and supplies no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1429` | 0 | rank 927, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short` | 0 | preflight listed only the pre-existing untracked `Formalizations/Lean/.lake` symlink |
| `git blame -L 10439,10444 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `for doi in bsmf.998 bsmf.1003 bsmf.1008; do curl -L --fail --silent --show-error -H 'Accept: application/vnd.citationstyles.csl+json' "https://doi.org/10.24033/$doi" \| jq -r '[.DOI,.issued["date-parts"][0][0],.volume,.page,.resource.primary.URL] \| @tsv'; done` | 0 | located inconsistent 1919/1920 historical metadata only; Crossref volume fields disagree with resource identifiers, no source-selected proposition or primary full-text crosswalk exists, and the catalog's 1917 date remains unresolved |
| `python3 -m json.tool Stage1_Instances/THM-M-1429/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1429/task-dag.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1429/intake-receipt.json` | 0 | valid JSON after receipt finalization |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | valid JSON after worker-manifest finalization |
| `python3 Stage1_Instances/THM-M-1429/check_intake.py` | 0 | target identity, H5/M4/R4 planned boundary, null target, empty accepted state, exact artifact inventory, and six open tasks agree |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1429-pycache python3 -m py_compile Stage1_Instances/THM-M-1429/check_intake.py` | 0 | intake validator compiles without adding generated files to the owned path |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| initial `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1429/IntakeProbe.lean)` | 1 | rejected the non-public identifier `Function.iterate`; that check was removed rather than masked |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1429/IntakeProbe.lean)` | 0 | seven adjacent pinned iteration, periodic-point, meromorphic, locally-uniform convergence, and topology APIs elaborated; no target theorem is stated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; package status clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...2d81`, respectively |
| `rg -n -i '\b(Fatou[ _-]?set\|Julia[ _-]?set)\b\|\bJulia set\b\|\bcomplex dynamics\b\|\bnormal famil(y\|ies)\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | expected no-match exit; intake discovery only, not an exhaustive anchor audit |
| `rg -n -i '\bFatou\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | three hits, all measure-theoretic Fatou's lemma references; no complex-dynamics candidate |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b' Stage1_Instances/THM-M-1429` | 1 | expected no-match exit; no prohibited proof-escape declaration |
| `git diff --check -- Stage1_Instances/THM-M-1429 .stage1-worker-selftest.json` plus owned-file invariants | 0 | no whitespace diagnostics; the scoped validator checks every untracked owned file |
| `git diff --no-index --check /dev/null .stage1-worker-selftest.json; for f in Stage1_Instances/THM-M-1429/*; do git diff --no-index --check /dev/null "$f" \|\| exit; done` | 1 | expected difference status and no diagnostics; all untracked new files passed Git's whitespace checker |

Known downstream failures remain deliberately open: an approved target correction with immutable
primary-source theorem identity and independent review; exact dynamical map, ambient space,
normality/stability, binder, hypothesis, conclusion, and boundary choices; canonical Lean
elaboration, expression/environment fingerprints, checked transports, and mutations; immutable
formal anchor audit; discovery and obligation freezes; proof and composition; hermetic replay;
deterministic evidence bundling; independent release verification; and master acceptance. These
block ordinary theorem execution and completion but do not invalidate a truthful, self-tested
`planned` intake.
