# Intake validation record

Base revision: `837792d9180ab731db89c16a5cc22128a9599bc8`.
Base tree: `5c5bd784032e9859e4c88b48a886d50194be1732`.
Validation date: 2026-07-13 (Asia/Shanghai).

The initial worktree contained only the automation-provided untracked symlink
`Formalizations/Lean/.lake`, whose target is the canonical pinned artifact directory. It was used
read-only and preserved. The evidence is therefore dirty-worker, intake-only, and nonrelease.
No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was run.

## Exact commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0033` | 0 | rank 1077, planned, L0/rework-required, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | initial status had only `Formalizations/Lean/.lake`; final status adds only the owned dossier and root worker packet |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 256,261 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalogue lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error https://api.crossref.org/works/10.2307/1969915` | 0 | Serre 1955 bibliographic metadata retrieved; SHA-256 `88a626e46ae238bea3a20c855a2ca7823162f99bc7347b7d1e21a6c02b61a386`; no theorem passage admitted |
| `curl -L --fail --silent --show-error https://api.crossref.org/works/10.1007/BF01390008` | 0 | Quillen 1976 bibliographic metadata retrieved; SHA-256 `c7e501fdb9473fadc536a6a99c7b5696e3740115a5f1d60cf1392ae9e004efc4`; no theorem passage admitted |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `cd Formalizations/Lean && lake --version` | 0 | Lake 5.0.0-src+98dc76e; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package status clean |
| `rg -n -i 'Quillen.Suslin\|Serre.?s conjecture\|projective modules over polynomial rings\|projective module.*polynomial ring' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/.lake/packages/mathlib/Archive --glob '*.lean'` | 1 | expected no match: no exact-topic Lean declaration in the bounded repo-local and pinned-mathlib source search |
| `rg -n -i 'Quillen.Suslin\|Serre.?s conjecture\|projective modules over polynomial rings' Formalizations/Lean/.lake/packages/mathlib/docs` | 0 | only `docs/1000.yaml` title `Quillen-Suslin theorem`; a documentation label, not a declaration |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0033/IntakeProbe.lean` | 0 | the seven projective/free/finite/multivariate-polynomial APIs elaborated; no theorem declaration or proof body was added |
| `python3 -m json.tool` over the structured owned files and root worker packet | 0 | instance, open DAG, provisional receipt, and self-test packet are valid JSON |
| `python3 -B Stage1_Instances/THM-M-0033/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, source/dependency hashes, H1/M4/R4 null target, exact artifact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0033/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-0033` | 1 | expected no match: the API-only probe contains no prohibited proof escape or declaration |
| `git diff --check -- Stage1_Instances/THM-M-0033 .stage1-worker-selftest.json` plus per-new-file `git diff --no-index --check /dev/null FILE` | 0 | no whitespace diagnostics; expected no-index status 1 meant only that each file is new |

The two probe imports are minimal for this scoped interface check: removing the projective-module
import makes `Module.Projective` unavailable, while removing the multivariate-polynomial import
makes `MvPolynomial` unavailable. This is an API elaboration check, not a statement-gate mutation
test or root-proof check.

## Boundary and blocker

Validated scope is limited to the planned dossier, theorem-family boundary, source-statement
crosswalk, source leads, adjacent pinned Lean APIs, and the six-node open downstream task DAG.
The first failed dependent gate is `S56-M-0033-STATEMENT`: the exact source proposition is not fixed.

Retry requires a lawfully preserved and hashed primary or authoritative edition, pinpoint theorem
or problem passage, incorporated definitions, all ordered binders and assumptions, conclusion,
proof boundary, translations/corrections/errata, and independent review. The coefficient ring,
finite variable representation, finite-generation premise, projective/free transports, and boundary
cases must then be frozen in one exact Lean expression with the four required mutation classes.

`S56-M-0033-STATEMENT`, `ANCHOR_AUDIT`, `OBLIGATION_TREE`, `PROOF`, `VALIDATION`, and `RELEASE`
remain open. The provisional worker receipt is not content-addressed or master-accepted, and no
audit-complete or theorem-complete claim is made.
