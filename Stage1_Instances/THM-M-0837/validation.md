# Intake validation

Base revision: `be8701e88e791545c16a262edd1909486d5cef4b` (tree
`78b0a751473bf6d71f453a6aad18b130268a3428`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set and execution-item consistency, exact dossier invariants,
repository provenance, bibliographic and discovery-source boundaries, pinned environment identity,
a narrow Lean colouring-API probe, bounded local name searches, JSON integrity, proof-escape
hygiene, and whitespace. The received proof-family label does not select a stable proposition, so
elaborating a purported canonical target would invent or substitute a root. `IntakeProbe.lean`
therefore states no theorem and supplies no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0837` | 0 | rank 1394, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 6145,6150 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref query for DOI `10.1006/jctb.1997.1750` | 0 | Robertson, Sanders, Seymour, Thomas; JCTB 70(1), May 1997, 2-44; response 6236 bytes, SHA-256 `935a9ba2d5dd08bdb4c6b095e8c882c53658d40e44dd6915ddcb37849ba61b61` |
| retrieval and inspection of the author-maintained Four Color Theorem page | 0 | 16056-byte HTML, SHA-256 `c096ff0c8b5da0bb9267071b83f65679bb7ce5a54b16b3fcbdde0502c1e8d83f`; 633 configurations, two main clauses, 32 rules, algorithm, and trust discussion located |
| retrieval and visual inspection of the authors' 1996 announcement | 0 | 203692-byte, nine-page PDF, SHA-256 `df597ecb200d7fcfecbebd00ce5d79c13e9e106fd47b39c9b9ddca225baeaca3`; abstract, (2.1)-(2.3), (3.1), (4.4), algorithm, and discussion located; formula extraction was garbled and was not treated as exact transcription |
| attempt to retrieve the 1997 JCTB article through the DOI/Elsevier routes | nonzero/incomplete | DOI metadata resolved, but the article body was not successfully retrieved; the JCTB record remains a bibliographic lead, not inspected proof evidence |
| arXiv API query for `1401.6481,1401.6485` | 0 | author records identify reducibility and discharging supplements with ancillary programs/data for the two computer-verified lemmas; no ancillary artifact was fetched or credited |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0837/IntakeProbe.lean)` | 0 | eight pinned simple-graph colouring interfaces elaborated; stdout SHA-256 `d1603a5b562207c41f04798f19bc0fc69bd1b2aab5366567bb811ccf55405d9e`; no target declaration |
| `rg -n -i --glob '*.lean' '(four.?colou?r\|4.?colou?r\|Robertson.?Sanders\|Seymour.?Thomas\|good configuration\|internally 6.?connected)' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | expected no-match for an exact Four-Colour or RSST declaration; bounded intake discovery only |
| `rg -n --glob '*.lean' 'def .*Planar\|class .*Planar\|IsPlanar' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph` | 1 | expected no-match for a simple-graph planarity definition; colouring module independently lists planar graphs as TODO |
| `python3 -m json.tool` on owned JSON and the worker packet | 0 | instance, open task DAG, provisional receipt, and handoff are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0837-pycache python3 -m py_compile Stage1_Instances/THM-M-0837/check_intake.py` | 0 | scoped validator compiles without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0837/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, planned H5/M4/R4 boundary, null target, source hashes, exact inventory, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0837/check_intake.py` | 0 | public replay passes without requiring the worker handoff |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0837` | 1 | expected no-match; no prohibited proof escape in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-0837 .stage1-worker-selftest.json`, plus no-index checks for every new file | 0 | no whitespace diagnostics |

## Known downstream failures

- The proof-family label is not one stable truth-valued proposition. A reviewed redirect must choose
  generic theorem, RSST provenance package, clause suite, computation-correctness package,
  algorithm theorem, or exact conjunction without borrowing the neighboring targets.
- The 1997 article body, exact incorporated definitions, assumption and correction mapping,
  computer-proof boundary, source-to-root composition, and independent review are open.
- No canonical Lean expression, minimal exact imports, expression or environment fingerprint,
  checked alternate encoding, or statement mutation exists.
- Planarity and plane-embedding infrastructure, 633 configurations, reducibility, 32-rule
  unavoidability, programs/data/certificates/checkers, anchor audit, obligation registry, typed
  graphs, proof, composition, trust closure, readable reconstruction, hermetic replay,
  deterministic bundle, and independent release verification are open.

These failures block ordinary theorem execution, audit completion, and theorem completion. They do
not invalidate a truthful self-tested `planned` intake whose purpose is to freeze the ambiguity and
open DAG. Only the integration lane may accept the provisional worker receipt.
