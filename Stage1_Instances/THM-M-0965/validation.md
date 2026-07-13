# Intake validation

Base revision: `fcabbf1e0ad9507eebe91663bccabfa87d22813e` (tree
`873e589c594454b7f263c7ed2342089a4d15e842`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation covers the planned dossier, primary-source scope crosswalk, open downstream task DAG,
and a narrow pinned Lean substrate probe. It does not validate a canonical Complete Intersection
statement or proof because the conclusion strength and exact encoding remain unselected. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker evidence is
nonrelease evidence.

## Environment

- Linux `7.0.0-27-generic` x86_64.
- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; used read-only and observed clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0965` | exit 0; rank 1499, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree match this record |
| `git blame -L 7050,7055 -- Docs/researches/math_theorems.md` | exit 0; all six catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| author-hosted primary PDF download, `pdfinfo`, `pdftotext -layout`, and bounded inspection | exit 0; 392690-byte, 12-page PDF with SHA-256 `2a0d46d7...a365`; definitions (1.1)-(1.3), candidate formula (1.9)-(1.10), main piecewise theorem, low-parameter remark, and proof boundary inspected |
| Crossref DOI query and canonical JSON projection | exit 0; authors/title/journal/volume/issue/pages/date/DOI confirmed; 612-byte projection SHA-256 `655c24ba...c8` |
| arXiv `1602.02634v1` PDF download, `pdfinfo`, `pdftotext -layout`, and bounded inspection | exit 0; 92754-byte, seven-page secondary source with SHA-256 `df9d325c...da3`; Construction 5 and bound-only Theorem 4 inspected |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0 with no output; shared pinned mathlib source remained clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0965/IntakeProbe.lean)` | exit 0; eight adjacent set-family, uniformity, cardinality, EKR, and prospective-predicate APIs elaborated; stdout SHA-256 `e1551dfa...6b9`; no target theorem declared |
| `rg -n -i --glob '*.lean' -e 'Ahlswede[-_ ]*Khachatrian' -e Khachatrian -e 'complete[ _-]*intersection theorem' -e 'complete[ _-]*t[ _-]*intersection' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | exit 1 as expected; bounded name/exact-topic discovery found no matching declaration; intake discovery only |
| `python3 -m json.tool` on all owned JSON artifacts and the worker packet | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0965-pycache python3 -m py_compile Stage1_Instances/THM-M-0965/check_intake.py` | exit 0; validator compiled without repository bytecode |
| `python3 -B Stage1_Instances/THM-M-0965/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest/DAG identity, source pins, null target, H1/M4/R4 boundary, inventory, receipt/packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0965/check_intake.py` | exit 0; public replay mode passes without the scheduler-only root packet |
| prohibited Lean construct scan over the owned path | exit 1 as expected; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

The first API-probe elaboration failed because parser notation `#(A intersect B)` was used in a term
without opening the scoped notation. The definition was changed to explicit `.card`, after which the
narrow probe passed. No target declaration or proof was involved, and the failed attempt receives no
evidence credit.

## Known open gates

Exact sharp-bound versus full-classification selection, visual transcription and independent review
of every transition and low-parameter clause, correction/errata audit, canonical Lean expression and
environment fingerprints, alternate transports and statement mutations, exhaustive formal-anchor
audit, discovery and obligation freezes, typed proof/provenance graphs, proof and composition, trust
closure, readable reconstruction, hermetic replay, deterministic bundle, independent verification,
master acceptance, audit completion, and theorem completion remain open. These failures do not
invalidate a truthful, self-tested `planned` intake.
