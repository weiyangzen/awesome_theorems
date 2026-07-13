# THM-M-1456 intake validation

Base revision: `01a2c11623c3f2f021424380d1c87b42f2d7e0e8` (tree
`8d6be645c3940807dbb57edc4fbe6c1485dbf1b6`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, source
record provenance, pinned environment identity, a narrow Lean API probe, bounded local searches,
proof-escape hygiene, JSON integrity, and whitespace. The source record is not a proposition, so
elaborating a purported canonical Lean target would invent missing mathematics. `IntakeProbe.lean`
therefore checks possible substrate only and supplies no statement or proof credit.

The preflight worktree contained the automation-provided untracked `Formalizations/Lean/.lake`
symlink to canonical pinned artifacts and five in-progress files already inside this assigned owned
path. Both were preserved; the files were audited and completed rather than overwritten blindly.
The symlink was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other
`.lake` mutation was performed. This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1456` | 0 | rank 1133, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | canonical `.lake` symlink plus five owned in-progress intake files; all preserved |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree match this record |
| `git log --all -S'**预处理技术**' -- Docs/researches/math_theorems.md` and blob check | 0 | uncited catalog record originates at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over manifest, blueprint, DAG, skill, guidelines, catalog, Stage0, toolchain, lockfile, and four pinned mathlib sources | 0 | exact hashes recorded in `instance.json` and receipt |
| `curl -L --fail --max-time 30 https://www.netlib.org/templates/templates.html` | 0 | 573,161 bytes; observed SHA-256 `006eb59144d9292245c3b0f9a65d7b60b4f08f196220ebbeecb35f66036b83a3`; discovery only |
| later bounded repeat of the same Netlib retrieval | 28 | network timed out after 30 seconds and 397,040 bytes; the incomplete bytes were discarded and provide no evidence; the earlier complete observation remains provisional until integration independently reacquires or archives it |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1456/IntakeProbe.lean)` | 0 | fifteen adjacent APIs elaborated and three axiom reports printed; output SHA-256 `904accb882716517b08f977449b54da0a2d8561f41b8198ce6b3e2e56b3c2526` |
| bounded repo and pinned-mathlib searches for the target, preconditioner, preconditioning, and condition-number terms | 0/1 | no source-identical declaration; generic English uses were unrelated; bounded intake discovery only |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1456-pycache python3 -m py_compile Stage1_Instances/THM-M-1456/check_intake.py` | 0 | validator compiles without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1456/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, null target, H5/M4/R4 boundary, pins, receipt, handoff, and six open tasks agree |
| `rg -n -i --glob '*.lean' '^\s*(sorry\|admit\|axiom\|constant\|opaque\|unsafe)\b\|sorryAx' Stage1_Instances/THM-M-1456` | 1 | expected no-match; no prohibited proof escape declaration |
| `git diff --check`, then `git diff --no-index --check /dev/null <file>` for each untracked changed file | 0 | no whitespace diagnostics; expected no-index difference statuses contained no diagnostics |

## Known downstream failures

- The catalog technique label and acceleration gloss do not select one stable proposition or
  primary source. An approved correction and independent review are open.
- The problem, iterative recurrence, preconditioner object and placement, domain, assumptions,
  convergence observable, comparator, rate, cost model, arithmetic convention, and boundary cases
  are open.
- The inspected Netlib chapter is an authoritative specification lead, not an admitted primary
  proof source and not evidence that every preconditioner accelerates every iterative method.
- No canonical Lean expression, expression or environment hash, exact imports, checked alternate
  encoding, or statement mutation test exists.
- Discovery protocol, full source and anchor audits, obligation registry and typed graphs, proof,
  composition and trust checks, readable reconstruction, hermetic replay, deterministic evidence
  bundle, independent verification, audit completion, theorem completion, and master acceptance
  remain open.

These failures block ordinary theorem execution and completion. They do not invalidate a truthful,
self-tested `planned` intake whose deliverable is to preserve the ambiguity, scope boundary,
crosswalk, and open DAG. Only the integration lane may accept the provisional worker receipt.
