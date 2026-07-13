# Intake validation

Base revision: `be8701e88e791545c16a262edd1909486d5cef4b` (tree
`78b0a751473bf6d71f453a6aad18b130268a3428`).

Validation covers manifest membership, the exact intake-node contract, repository and source
provenance, the nine-file planned dossier, JSON integrity, scoped invariants, a bounded exact-topic
search, and a narrow pinned Lean API probe. The canonical proposition is deliberately still open,
so this record does not claim statement elaboration, target or environment hashes, statement
mutations, proof closure, audit completion, or release evidence.

The worker reused the automation-provided canonical `.lake` symlink and pinned artifacts read-only.
No `lake update`, `lake build`, dependency clone/fetch, or other `.lake` mutation ran. The initial
worktree contained only that pre-existing untracked symlink, so all worker evidence is nonrelease.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0836` | 0 | rank 1393; planned; L0/rework_required; no legacy slot; theorem_complete false |
| `git status --short --untracked-files=all` before editing | 0 | only pre-existing `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree above |
| `git blame -L 6138,6143 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9f...` |
| AMS publisher PDF download plus `file`, `wc`, `sha256sum`, `pdfinfo`, and `pdftotext` | 0 | PDF 1.2, 237594 bytes, two pages, SHA-256 `da6b2598...d64`; printed pp. 711-712 inspected |
| Crossref metadata queries for the 1976 announcement, 1977 Parts I/II, and supplements | 0 | titles, authors, dates, journals, DOI boundaries, and announcement pages confirmed; this is not an errata audit |
| Project Euclid Part I/II download attempts | 0 HTTP responses | approximately 1 KB anti-bot HTML, not PDFs; no detailed-primary-source claim |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3...`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | mathlib `8a178386...`, tree `bdc39a3...` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short --untracked-files=all` | 0 | no output; pinned worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0836/IntakeProbe.lean)` | 0 | eight adjacent APIs and one tiny coloring elaborated; 924-byte stdout SHA-256 `c7e10628...a4e8`; no canonical target |
| bounded exact-topic `rg` over pinned mathlib and repo Lean | 1 expected | no Appel-Haken/four-color/unavoidable-set/reducible-configuration/discharging-method occurrence; discovery only |
| `python3 -m json.tool` on the three owned JSON files and root worker packet | 0 | valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0836-pycache python3 -m py_compile Stage1_Instances/THM-M-0836/check_intake.py` | 0 | scoped validator compiles without generated owned-path files |
| `python3 -B Stage1_Instances/THM-M-0836/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H5/M4/R4 boundary, null target, hashes, exact inventory, handoff, and six open tasks agree |
| prohibited-declaration `rg` over owned Lean files | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped `git diff --check` and per-new-file no-index checks | 0 aggregate | no whitespace diagnostics |

The Lean probe initially exposed two ordinary type-inference mismatches while constructing the tiny
concrete example. Both were corrected explicitly, and the final recorded probe above passes. Those
failed drafting runs supplied no evidence and are not hidden proof failures: the example is only an
API check, not the canonical target.

## Known downstream failures

- The separate catalog row does not select the exact announced theorem versus an
  unavoidability/reducibility conjunction, program correctness theorem, or complete source-suite
  reconstruction, and it must remain distinct from `THM-M-0833`.
- The detailed 1977 sources and supplements, configuration inventory, code/tables/certificates,
  complete premise/conclusion/proof/correction map, and independent review are open.
- No canonical Lean expression, minimal imports, expression or environment fingerprint, checked
  alternate encoding, or required statement mutation exists.
- Formal anchor audit, discovery freeze, obligation registry and typed graphs, planarity and
  configuration infrastructure, computation checker, proof, composition, trust closure, readable
  reconstruction, hermetic replay, deterministic evidence bundle, independent release verification,
  and master acceptance remain open.

These failures block every statement, audit, and theorem-completion claim. They do not invalidate a
truthful, self-tested `planned` intake whose job is to freeze the ambiguity and open the downstream
DAG. Only the integration lane may accept the provisional worker receipt.
