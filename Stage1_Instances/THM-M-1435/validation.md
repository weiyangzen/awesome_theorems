# Intake validation

Base revision: `d1bb69e506d568ec4852bd68cc5bda1d61702852` (tree
`d9681ef41935162296b57b0170641d66404a53a9`). Validation ran on 2026-07-12 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, source and
duplicate provenance, pinned environment identity, a narrow Lean API probe, a bounded local name
search, proof-escape hygiene, and whitespace. The catalog wording is not a proposition, so
elaborating a purported canonical Lean target would invent missing mathematics. `IntakeProbe.lean`
therefore checks only possible substrate; it introduces no theorem and supplies no statement or
proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1435` | 0 | rank 933, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git blame -L 10481,10486 -- Docs/researches/math_theorems.md` and `git blame -L 1864,1869 -- Docs/researches/math_theorems.md` | 0 | both uncited six-line catalog records originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error https://arxiv.org/pdf/math/9410221v1 -o /tmp/mcmullen_frontiers.pdf` followed by `sha256sum`, `pdfinfo`, and `pdftotext` inspection | 0 | immutable arXiv v1 PDF, 199514 bytes and 17 pages, SHA-256 `e8f777c2bda3133b0b30241702d447410826a892d507e12d8d68c9042d0a0b81`; survey and Theorem 5.2 inspected as ambiguity evidence only |
| Crossref lookups for DOI `10.1090/S0273-0979-1994-00519-1` and DOI `10.1515/9781400882557` | 0 | confirmed the 1994 survey metadata and the identified book edition's 1995 date; neither lookup selects the catalog proposition |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| first `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1435/IntakeProbe.lean)` attempt | 1 | discovery-only identifiers `ℂ` and `OnePoint ℂ` needed an explicit `Mathlib.Data.Complex.Basic` import; corrected without adding a target declaration or proof |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1435/IntakeProbe.lean)` | 0 | ten pinned complex, one-point, meromorphic, iterate, periodic-point, closure, and frontier API checks elaborated; no target declaration |
| bounded McMullen/Julia-set/Mandelbrot/complex-dynamics/rational-dynamics/normal-family/Lattes name search over repo-local and pinned mathlib `*.lean` | 1 | expected no-match result; intake discovery only, not a complete anchor audit |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | instance, open task DAG, provisional receipt, and worker handoff are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1435-pycache python3 -m py_compile Stage1_Instances/THM-M-1435/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-1435/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/item identity, planned H5/M4/R4 boundary, duplicate freeze, null target, exact artifact inventory, handoff, and six open tasks agree |
| prohibited Lean proof-escape scan over `Stage1_Instances/THM-M-1435` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1435 .stage1-worker-selftest.json` plus no-index checks for every untracked changed file | 0 | no whitespace diagnostics |

## Known downstream failures

- The catalog wording is not a stable proposition. No approved correction selects a source,
  theorem locator, map class, Julia-set definition, quantifier order, hypotheses, conclusion, or
  boundary cases.
- The apparent semantic duplicate `THM-M-0259` remains a separate authoritative root. No approved
  disposition decides whether the records should merge, split, redirect, or name different claims.
- No independently reviewed immutable primary theorem, complete definition/assumption/proof/errata
  crosswalk, translation and publication-date review, or theorem locator is accepted.
- No canonical Lean expression, expression/environment hash, exact imports, checked alternate
  encoding, or statement mutation test exists.
- Discovery protocol, anchor audit, obligation registry and typed graphs, proof, composition and
  trust checks, readable reconstruction, hermetic replay, deterministic evidence bundle, and
  independent release verification are open.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose purpose is to freeze the honest ambiguity and duplicate
boundaries and open the downstream DAG. Only the integration lane may accept the provisional worker
receipt.
