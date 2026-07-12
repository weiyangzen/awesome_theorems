# Intake validation

Base revision: `d1bb69e506d568ec4852bd68cc5bda1d61702852` (tree
`d9681ef41935162296b57b0170641d66404a53a9`). Validation ran on 2026-07-12 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, primary-
source provenance, pinned environment identity, a narrow Lean API probe, a bounded local name
search, proof-escape hygiene, JSON integrity, and whitespace. The catalog wording does not select
one proposition from the primary source's multi-theorem suite, so elaborating a purported
canonical Lean target would invent a target choice. `IntakeProbe.lean` therefore checks only
possible substrate; it introduces no theorem and supplies no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1438` | 0 | rank 936, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git blame -L 10502,10507 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0' -sS 'https://www.ams.org/journals/bull/1982-06-03/S0273-0979-1982-15008-X/S0273-0979-1982-15008-X.pdf' -o /tmp/lanfordams.pdf`, followed with `&&` by `file`, `wc -c`, `sha256sum`, `pdfinfo`, and `pdftotext -layout` checks | 0 | PDF v1.2, 638627 bytes and 8 scan pages, SHA-256 `210cb7c561788fd8fab5fb2d5f7158619ef698a64fbb2ff0b5750185192ef045`; printed pages 427-434 and the numbered theorem suite inspected |
| `curl -L --fail --max-time 30 -sS 'https://api.crossref.org/works/10.1090/s0273-0979-1982-15008-x'` with `jq` selection | 0 | title, author, date 1982-05-01, journal, volume 6, issue 3, bibliographic pages 427-435, and DOI confirmed; relation empty and update-to null, which is not a complete errata audit |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| initial `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1438/IntakeProbe.lean)` | 1 | rejected nonexistent module `Mathlib.Analysis.Normed.Space.ContinuousLinearMap`; corrected to the public pinned module `Mathlib.Analysis.Normed.Operator.ContinuousLinearMap` rather than masking the failure |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1438/IntakeProbe.lean)` | 0 | eight pinned analytic, fixed-point, continuous-linear-map, compact-operator, and spectral APIs elaborated; no target declaration |
| `rg -n -i --glob '*.lean' '\b(Lanford\|Feigenbaum)\b\|period[- _]?doubling\|\bunimodal\b' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | expected no source-specific match; intake discovery only, not a complete anchor audit |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | instance, open task DAG, provisional receipt, and worker handoff are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1438-pycache python3 -m py_compile Stage1_Instances/THM-M-1438/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-1438/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, planned H5/M4/R4 boundary, null target, exact artifact inventory, source hashes, handoff, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-1438` | 1 | expected no-match; no prohibited proof escape in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-1438 .stage1-worker-selftest.json`, then `git diff --no-index --check /dev/null <file>` for every untracked changed file | 0 | no whitespace diagnostics; expected no-index difference statuses contained no diagnostics |

## Known downstream failures

- The catalog wording does not choose Theorem 1, Theorems 1 and 3, Theorems 1/3/4/5, or another
  exact source proposition. Accountable selection and independent review are open.
- Exact visual-source transcription, incorporated definitions, errata review, assumptions,
  conclusions, computation boundary, and source-to-root composition are open. Physical pages
  427-434 and Crossref's boundary-style 427-435 metadata are distinguished, not conflated.
- No canonical Lean expression, expression/environment hash, exact imports, checked alternate
  encoding, or statement mutation test exists.
- Discovery protocol, anchor audit, obligation registry and typed graphs, source-specific analytic
  and dynamical infrastructure, interval certificate and checker, proof, composition and trust
  checks, readable reconstruction, hermetic replay, deterministic evidence bundle, and independent
  release verification are open.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose purpose is to freeze the source-suite ambiguity and
open DAG. Only the integration lane may accept the provisional worker receipt.
