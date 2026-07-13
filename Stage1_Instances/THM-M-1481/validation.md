# THM-M-1481 intake validation

Base revision: `8a6dba9921138a63027dc802b77a4cc3a01f3f60` (tree
`1afb3440a5a33640728678de56e261f9470af1d1`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, catalog
and source-lead provenance, pinned environment identity, a narrow Lean API probe, bounded local
searches, proof-escape hygiene, JSON integrity, and whitespace. The catalog record is not a
proposition, so elaborating a purported canonical target would invent missing mathematics.
`IntakeProbe.lean` checks possible substrate only and supplies no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was preserved and used
read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was performed. This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1481` | 0 | rank 1158, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | pre-existing canonical `.lake` symlink only; preserved |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree match this record |
| `git log --all -S'**模拟退火**' -- Docs/researches/math_theorems.md`, blame, and blob/excerpt checks | 0 | the uncited six-line record originates at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; exact hashes recorded |
| `sha256sum` over manifest, blueprint, DAG, skill, guidelines, catalog, Stage0, toolchain, lockfile, and four pinned mathlib sources | 0 | exact hashes recorded in `instance.json` and the receipt |
| bounded Crossref/NLM retrieval for DOI `10.1126/science.220.4598.671` | 0 | three-author 1983 Science metadata and abstract observed; exact response hashes recorded |
| `curl -L --fail --max-time 30 --user-agent 'Mozilla/5.0' https://www2.stat.duke.edu/~scs/Courses/Stat376/Papers/TemperAnneal/KirkpatrickAnnealScience1983.pdf` | 0 | 581,070-byte, 11-page course-hosted JSTOR scan; SHA-256 `d0fedd367a09e978538839da68f32f91ec3f9713d1a7c7a2ac783e28e250b6b0`; inspected transiently, not vendored due to the scan's personal/noncommercial-use notice |
| `pdftotext -layout` plus pinpoint searches of the Science scan | 0 | 98,776 bytes, 816 lines, 10,592 words; SHA-256 `6789a7b5566f3e7e46e0029610550bdcaf0630d977f6d6cd507cd4fbe009f8d6`; pp. 671-673 and 679 support the source boundary in the crosswalk |
| bounded Crossref/publisher retrieval for DOI `10.1287/moor.13.2.311` | 0/22 | publisher-deposited abstract observed and hashed; publisher body returned HTTP 403; Hajek is a later theorem lead only |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` and status | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1481/IntakeProbe.lean)` | 0 | seven adjacent APIs elaborated and two axiom reports printed; output SHA-256 `dacfcbac542e520c30e9a1bbfb4c63517e553e3844f85092a1a016535f6848f5` |
| bounded repository and pinned-mathlib searches for simulated annealing, annealing, cooling schedule, and Metropolis | 1 | expected no-match for a source-identical Lean declaration; intake discovery only |
| `sha256sum` over eight non-self-referential owned artifacts | 0 | exact final-byte digests recorded in `intake-receipt.json`; the mutable receipt cannot contain its own raw-file digest, and the root packet is cross-checked structurally against it |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1481-pycache python3 -m py_compile Stage1_Instances/THM-M-1481/check_intake.py` | 0 | validator compiles without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1481/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, null target, H5/M4/R4 boundary, pins, receipt, packet, and six open tasks agree |
| `rg -n -i --glob '*.lean' '^\s*(sorry\|admit\|axiom\|constant\|opaque\|unsafe)\b\|sorryAx' Stage1_Instances/THM-M-1481` | 1 | expected no-match; no prohibited proof escape declaration |
| `git diff --check`, then `git diff --no-index --check /dev/null <file>` for every untracked changed file | 0 | no whitespace diagnostics |

## Known downstream failures

- The catalog method label and purpose do not select one truth-valued proposition. A target
  correction, complete source crosswalk, correction/errata audit, and independent review are open.
- The inspected 1983 article presents a heuristic framework, Metropolis rule, staged cooling, and
  numerical studies, not an exact general theorem matching the catalog gloss.
- The state and cost spaces, proposal and acceptance law, schedule and depth, process construction,
  convergence mode, quantifier order, arithmetic model, and boundary cases are open.
- Hajek's 1988 result is a later narrow theorem family and cannot silently replace the 1983 root.
- No canonical Lean expression, expression or environment hash, exact imports, checked alternate
  encoding, or statement mutation test exists.
- Discovery protocol, full anchor audit, obligation registry and typed graphs, proof, composition
  and trust checks, readable reconstruction, hermetic replay, deterministic evidence bundle,
  independent verification, audit completion, theorem completion, and master acceptance remain
  open.

These failures block ordinary theorem execution and completion. They do not invalidate a truthful,
self-tested `planned` intake whose deliverable is to preserve the ambiguity, scope boundary,
source crosswalk, and open DAG. Only the integration lane may accept the provisional worker receipt.
