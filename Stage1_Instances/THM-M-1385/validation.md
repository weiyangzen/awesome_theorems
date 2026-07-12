# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source ambiguity boundary, open task DAG, JSON and
scoped invariants, and a narrow pinned Lean API probe. It does not validate a canonical Sturm
comparison statement or proof because neither has been frozen. The automation-provided canonical
`.lake` symlink was pre-existing and used read-only; no dependency update, build, clone, fetch, or
other `.lake` mutation was performed. This dirty worker evidence is nonrelease evidence.

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

## Source discovery boundary

Sturm's original 1836 memoir was retrieved from NUMDAM to temporary storage, hashed, and inspected
at sections XII and XVI as recorded in the crosswalk. It was not added to the repository. The
inspection identifies two plausible roots but does not authorize intake to select one. Crossref
metadata and immutable Encyclopedia of Mathematics revision 51620 were also inspected; the latter
establishes that polynomial Sturm's theorem is a name collision. Complete proof mapping,
translation, errata audit, and independent review remain open, so no `H0` claim is made.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1385` | exit 0; rank 995, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 10090,10095 -- Docs/researches/math_theorems.md` | exit 0; the six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded `curl --range` retrieval in 262144-byte chunks followed by ordered concatenation to `/tmp/sturm_complete.pdf` | exit 0; server reported 3,056,791 bytes; all chunks retrieved; 82-page original memoir scan assembled with SHA-256 `dac792...c96`; `pdfinfo` and `pdftotext` passed |
| `pdftotext -f 21 -l 22 -layout /tmp/sturm_complete.pdf -` and page-scan inspection | exit 0; section XII global zero-count/order theorem, coefficient orders, and endpoint-ratio premise inspected |
| `pdftotext -f 31 -l 32 -layout /tmp/sturm_complete.pdf -` and page-scan inspection | exit 0; section XVI consecutive-zero comparison inspected; scan resolves OCR-dropped equality bars |
| `curl -L --fail --max-time 45 -sS -G https://api.crossref.org/works --data-urlencode 'query.title=Memoire sur les equations differentielles lineaires du second ordre' --data-urlencode 'query.author=Sturm' --data-urlencode rows=5 -o /tmp/sturm-crossref.json` | exit 0; memoir metadata located; response SHA-256 `f36a46...e6d`; metadata only |
| `curl -L --fail --max-time 45 -sS 'https://encyclopediaofmath.org/api.php?action=parse&page=Sturm_theorem&prop=wikitext&format=json' -o /tmp/sturm-eom-api.json` | exit 0; immutable revision 51620 polynomial root-counting entry inspected; response SHA-256 `f1fc28...94f7`; rejected as a substitute |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1385/IntakeProbe.lean)` | exit 0; ten adjacent pinned ODE, derivative, interval, and zero-set APIs elaborated; no target theorem declared |
| exact-topic `rg` search for Sturm comparison and zero-comparison names in repo-local and pinned mathlib `.lean` files | exit 1; expected no match; no exact target declaration found; bounded intake discovery rather than an exhaustive anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1385-pycache python3 -m py_compile Stage1_Instances/THM-M-1385/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1385/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, null target, H1/M4/R4 boundary, source pins, exact artifact inventory and hashes, receipt/packet agreement, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-1385` | exit 1; expected no match for prohibited Lean constructs |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

Canonical selection between inspected sections XII and XVI; complete proof, translation,
definition, hypothesis, conclusion, proof-boundary and errata crosswalk; independent source review;
every Lean ODE-form, coefficient, regularity, interval, solution, inequality, zero, endpoint and
degeneracy decision; canonical Lean expression and fingerprints; checked transports and mutations;
exhaustive formal anchor audit; discovery and obligation freezes; typed graphs; proof and
composition; trust and provenance closure; readable reconstruction; hermetic replay; deterministic
release bundle; independent verification; master acceptance; audit completion; and theorem
completion remain open. These failures do not invalidate a truthful self-tested `planned` intake.
