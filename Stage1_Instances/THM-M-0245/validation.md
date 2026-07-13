# Intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source and scope crosswalk, open task DAG, structured
invariants, bounded discovery, and pinned Lean substrate probe. It does not validate a canonical
Fatou proposition or proof because the repository gloss omits the size premise and exact boundary
conclusion, and the likely primary theorem passage was not accessible. The automation-provided
canonical `.lake` symlink was pre-existing and used read-only; no update, build, clone, fetch, or
other dependency mutation was performed. Dirty worker evidence is nonrelease.

## Source boundary

Crossref identified P. Fatou, *Series trigonometriques et series de Taylor*, *Acta Mathematica* 30
(1906), 335-400, DOI `10.1007/BF02418579`. DOI and Semantic Scholar metadata point to Project
Euclid. A zbMATH/JFM record for the same paper contains a historical review of Poisson-integral
boundary behavior. The Project Euclid PDF endpoint returned an access-control HTML response, not
the paper. Consequently no primary theorem/page, incorporated definition chain, exact assumptions
or conclusion, proof boundary, correction, erratum, translation, or independent review is
credited. The secondary review is discovery evidence only and is not substituted for the source.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0245` | exit 0; rank 1255, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git blame -L 1766,1771 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref, DOI, Project Euclid, zbMATH, and Semantic Scholar inspection for `10.1007/BF02418579` | metadata requests succeeded; matching 1906 publication and a historical review record were identified, while the primary PDF endpoint returned access-control HTML; source family only, not H0 |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0245/IntakeProbe.lean)` | exit 0 after correcting two initially overqualified namespace checks; ten unit-disc, analytic, radial-map, filter, almost-everywhere, and circle-measure APIs elaborated; no theorem was stated; complete output SHA-256 `204f1802bd26b702aaa51adb4b63844ed9a4aabd2efe22cf7cb57e70f51dc15f` |
| bounded `rg` search for Fatou, radial/nontangential boundary limits, and analytic Hardy spaces in pinned mathlib | specific query exited 1 with no matches; broad `Fatou` query found three measure-theoretic Fatou's lemma references only; intake discovery, not an exhaustive anchor audit |
| `python3 -m json.tool` on the structured intake artifacts | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0245-pycache python3 -m py_compile Stage1_Instances/THM-M-0245/check_intake.py` | exit 0; checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0245/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, source and dependency hashes, null target, H1/M4/R4 boundary, artifact hashes, worker packet, pinned Lean probe, and six open tasks agree |
| token-anchored prohibited Lean declaration scan over the owned path | exit 1 as expected; no declaration-token match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` in the API-only probe |
| scoped new-file whitespace checks and `git diff --check` | exit 0; no whitespace errors |

## Known open gates

Primary-source admission, the exact size or Hardy-class premise, boundary carrier and measure,
radial or nontangential approach filter, almost-everywhere exceptional set, finite-limit and any
boundary-function/norm conclusions, complete source definition and assumption reconstruction,
correction/errata audit, and independent source review remain open. So do the canonical Lean
expression and environment fingerprints, minimal imports, checked transports, statement mutations,
exhaustive anchor and provenance audit, discovery protocol, obligation registry, typed graphs,
proof and composition, trust closure, readable reconstruction, hermetic replay, deterministic
bundle, independent verification, master acceptance, audit completion, and theorem completion.
These failures do not invalidate a truthful, self-tested `planned` intake.
