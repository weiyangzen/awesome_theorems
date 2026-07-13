# Intake validation

Base revision: `72e9e8092182121a6794921f61fcc9cae22f726d` (tree
`0d6c1fdf06d1573c256af331c6b198e5a787af43`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation covers the planned dossier, source and stable-ID boundaries, open downstream task DAG,
and a narrow pinned Lean candidate-shape probe. It does not validate a canonical Hilton-Milner
statement or proof because primary-source inspection and root-variant selection remain open. The
automation-provided `.lake` symlink was pre-existing and used read-only. No dependency update,
build, clone, fetch, or other `.lake` mutation was performed. This dirty worker evidence is
nonrelease evidence.

## Environment

- Linux `7.0.0-27-generic` x86_64.
- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; used read-only.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0964` | exit 0; rank 1498, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree match this record |
| `git blame -L 7043,7048 -- Docs/researches/math_theorems.md` | exit 0; all catalog lines originate at commit `bcf3f9f...` |
| pre/post-dedup `git show` searches at `c61be3c...` | exit 0; before dedup `THM-M-0964` was Vosper and Hilton-Milner was `THM-M-0992`; after dedup Hilton-Milner is current `THM-M-0964` |
| Crossref DOI query and canonical JSON projection | exit 0; authors, title, journal, volume, issue, pages, year, DOI, and publisher PDF locator confirmed; projection SHA-256 `5b47fba5...afbf0` |
| OUP DOI/PDF retrieval | HTTP 403 / Cloudflare challenge; primary body not admitted and no primary-source statement credit assigned |
| arXiv `1609.04714v3` PDF retrieval, `pdfinfo`, `pdftotext -layout`, and bounded inspection | exit 0; 168086-byte, nine-page PDF, SHA-256 `6e354fcd...9035`; Theorem 11 bound, range, construction, equality classification, and reference [11] inspected |
| arXiv `2411.02513v4` PDF retrieval, `pdfinfo`, `pdftotext -layout`, and bounded inspection | exit 0; PDF SHA-256 `b01196bd...bb2c`; bound-only Theorem 1, endpoint, construction, and separate uniqueness discussion inspected |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0 with no output; pinned mathlib source remained clean |
| bounded Hilton-Milner name/exact-topic search under pinned mathlib and repo-local Lean | exit 1 as expected; no matching declaration located; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0964/IntakeProbe.lean)` | exit 0; seven adjacent APIs and the unproved candidate proposition shape elaborated; stdout SHA-256 `a88e8dd0...70ed`; no target theorem declared |
| `python3 -m json.tool` on all owned JSON files and the worker packet | exit 0 after finalization |
| `python3 -B Stage1_Instances/THM-M-0964/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest/DAG identity, pins, null target, H1/M3/R4 boundary, stable identity, receipt/packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0964/check_intake.py` | exit 0; public replay mode passes without the scheduler-only packet |
| prohibited Lean construct scan over the owned path | exit 1 as expected; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

The first API-probe elaboration failed because the draft used the nonexistent identifier
`Set.empty`. It was corrected to the typed empty set `(empty : Set (Fin n))`, after which the narrow
probe passed. No theorem or proof body was involved, and the failed draft receives no evidence
credit.

## Known open gates

Primary theorem access, exact bound/attainment/classification selection, endpoint and degenerate-case
review, correction/errata audit, independent source review, canonical Lean expression and
environment fingerprint, alternate transports and statement mutations, exhaustive formal-anchor
audit, discovery and obligation freezes, typed graphs, proof and composition, trust closure,
readable reconstruction, hermetic replay, deterministic evidence bundle, independent verification,
master acceptance, audit completion, and theorem completion remain open. These failures do not
invalidate a truthful, self-tested `planned` intake.
