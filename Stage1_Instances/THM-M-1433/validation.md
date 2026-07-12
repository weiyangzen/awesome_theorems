# Intake validation

Base revision: `5ac2d33ee4b1a16fd90dca63313cd900ffc4bb50` (tree
`59b19df4105f58fc10c3e924c32320a284145b7c`). Validation ran on 2026-07-12 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, source
provenance, pinned environment identity, a narrow Lean API probe, a bounded local name search,
proof-escape hygiene, and whitespace. The source wording is not a proposition, so elaborating a
purported canonical Lean target would invent missing mathematics. `IntakeProbe.lean` therefore
checks only possible substrate; it introduces no theorem and supplies no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1433` | 0 | rank 931, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git blame -L 10467,10472 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error https://arxiv.org/pdf/math/0003105v1 -o /tmp/carletti_marmi.pdf` followed by `sha256sum`, `pdfinfo`, and `pdftotext` inspection | 0 | immutable arXiv v1 PDF, 186606 bytes and 11 pages, SHA-256 `1353dd93050660f9442db61cdfa119188874073bc80d0efbb5de64224fd5f0f3`; introduction and Appendix A distinguish candidate statements; source-selection evidence only |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1433/IntakeProbe.lean)` | 0 | ten pinned continued-fraction, Diophantine-approximation, analytic-composition, fixed-point, and semiconjugacy APIs elaborated; no target declaration |
| bounded Brjuno/Bryuno/Siegel-disk/Yoccoz/small-divisor/analytic-linearization name search over repo-local and pinned mathlib `*.lean` | 1 | expected no-match result; intake discovery only, not a complete anchor audit |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | instance, open task DAG, provisional receipt, and worker handoff are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1433-pycache python3 -m py_compile Stage1_Instances/THM-M-1433/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-1433/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/item identity, planned H5/M4/R4 boundary, null target, exact artifact inventory, handoff, and six open tasks agree |
| prohibited Lean proof-escape scan over `Stage1_Instances/THM-M-1433` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1433 .stage1-worker-selftest.json` plus no-index checks for every untracked changed file | 0 | no whitespace diagnostics |

## Known downstream failures

- The catalog wording is not a stable proposition. No approved correction selects the arithmetic
  predicate, source theorem, implication direction, map class, quantifiers, conjugacy conclusion,
  boundary cases, or separation from `THM-M-1432`.
- No independently reviewed immutable primary theorem, complete definition/assumption/proof/errata
  crosswalk, translation review, or theorem locator is accepted.
- No canonical Lean expression, expression/environment hash, exact imports, checked alternate
  encoding, or statement mutation test exists.
- Discovery protocol, anchor audit, obligation registry and typed graphs, proof, composition and
  trust checks, readable reconstruction, hermetic replay, deterministic evidence bundle, and
  independent release verification are open.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose purpose is to freeze the honest ambiguity boundary and
open DAG. Only the integration lane may accept the provisional worker receipt.
