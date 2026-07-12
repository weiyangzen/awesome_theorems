# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation covers the planned dossier, source/result and neighboring-target boundaries, open task
DAG, JSON and scoped invariants, and a narrow pinned Lean API probe. It does not validate a
canonical Polymath statement or proof because neither has been selected. The automation-provided
canonical `.lake` symlink was pre-existing and used read-only; no dependency update, build, clone,
fetch, or other `.lake` mutation was performed. This dirty worker evidence is nonrelease evidence.

## Environment

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
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0950` | exit 0; rank 1022, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 6938,6943 -- Docs/researches/math_theorems.md` | exit 0; all six catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| publisher PDF download, `pdfinfo`, `pdftotext`, and bounded inspection | exit 0; 554622-byte, 45-page PDF with SHA-256 `b7f68cc3...2df`; located definitions and Theorems 1.4 and 1.5 on pp. 1283-1285 |
| arXiv API query for `0910.3926` | exit 0; confirmed v2 identity, authorship and dates; live-summary exponent conflict recorded as non-authoritative metadata |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0950/IntakeProbe.lean)` | exit 0; line, ordinary Hales-Jewett, density, word-cardinality and prospective predicate APIs elaborated; output SHA-256 `537c8866...7c1`; no target theorem declared |
| bounded exact-topic `rg` over pinned mathlib and repo-local Lean | exit 1 as expected; no density-Hales-Jewett, DHJ, or Polymath declaration; intake discovery only |
| `python3 -m json.tool` on all JSON artifacts and the worker packet | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0950-pycache python3 -m py_compile Stage1_Instances/THM-M-0950/check_intake.py` | exit 0; validator compiled without generated files in the owned path |
| `python3 Stage1_Instances/THM-M-0950/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest/DAG identity, null target, H5/M4/R4 boundary, source pins, exact inventory, receipt/packet, and six open tasks agree |
| prohibited Lean construct scan over the owned path | exit 1 as expected; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

The first two experimental API-probe elaborations failed before the final passing probe: the first
used an inferred `NNReal` where `Finset.dens` returns `NNRat`, omitted a function-space `Fintype`
instance, used escaped membership syntax, and referenced an unavailable imported lemma; the second
retained only the density-codomain mismatch. These probe-only issues were corrected. No target
declaration or proof was involved, and no failed attempt is credited as evidence.

## Known open gates

An exact source result or provenance-sensitive package, the `THM-M-0949` boundary, incorporated
definitions and premises, correction/exponent audit, and independent source review remain open. So
do the canonical Lean expression and environment fingerprints, checked transports and mutations,
exhaustive formal-anchor audit, discovery and obligation freezes, typed proof/provenance graphs,
Polymath proof reconstruction, proof and composition, trust closure, readable reconstruction,
hermetic replay, deterministic bundle, independent verification, master acceptance, audit
completion, and theorem completion. These failures do not invalidate a truthful, self-tested
`planned` intake.
