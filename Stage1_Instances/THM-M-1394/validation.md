# Intake validation

Base revision: `02cc55f883d5b5d091ead6851bffe89199eb8391` (tree
`035212d041a1e61553b3d2f465964c9bbb35e47d`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, literal catalog boundary, open task DAG, source-family
discrimination, structured intake invariants, and a narrow pinned Lean API probe. It does not
validate a canonical shooting theorem or proof because the repository record supplies no truth-
valued proposition. The automation-provided canonical `.lake` symlink existed before this intake
and was used read-only; no dependency update, build, clone, fetch, or other `.lake` mutation was
performed. This dirty warm-cache worker evidence is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; its package source remained clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1394` | exit 0; rank 1004, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | pre-edit exit 0; only the pre-existing `Formalizations/Lean/.lake` symlink was untracked; base revision and tree match this record |
| `git blame -L 10153,10158 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref retrieval for DOI `10.1016/0022-247X(68)90064-4` | exit 0; confirmed Bailey/Shampine title, authors, August 1968, journal, volume/issue, pages, and DOI; response SHA-256 `8d9df580...f5aa` |
| Crossref retrieval for DOI `10.1145/355580.369128` | exit 0; confirmed Morrison/Riley/Zancanaro title, authors, December 1962, journal, volume/issue, pages, and DOI; response SHA-256 `5d636b30...9d97` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | exit 0; pinned revision/tree recorded above; package source clean before and after the probe |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1394/IntakeProbe.lean)` | exit 0; eight adjacent pinned IVP, error-bound, and intermediate-value APIs elaborated; stdout SHA-256 `e2120767...8428`; stderr empty; no target theorem declared |
| bounded case-insensitive `rg` search for shooting method, single/multiple shooting, shooting parameter/residual, and boundary residual in repo-local Lean and pinned mathlib | exit 1; expected no exact-topic match, discovery only rather than an exhaustive anchor audit |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1394-pycache python3 -m py_compile Stage1_Instances/THM-M-1394/check_intake.py` | exit 0; the scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-1394/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest/DAG identity, current hashes, null target, H5/M4/R4 boundary, exact inventory, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1394/check_intake.py` | exit 0; public replay mode passes without the scheduler-only worker packet |
| prohibited Lean construct scan over the owned path | exit 1; expected no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped per-new-file `git diff --no-index --check` plus `git diff --check` | exit 0 for whitespace diagnostics; every owned artifact and the root handoff passed |

## Known open gates

An exact immutable primary or authoritative theorem/page, incorporated definitions, complete
premise/conclusion/proof-boundary/errata crosswalk, choice among BVP and shooting variants,
neighbor ownership review, and independent source review remain open. So do the canonical Lean
target and minimal imports, expression/environment fingerprints, checked transports, four statement
mutation classes, exhaustive anchor audit, discovery protocol, obligation registry, typed graphs,
proof and composition, source/provenance/trust closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These failures do not invalidate a truthful self-tested `planned` intake.
