# Intake validation

Base revision: `531673f2e97293dd22e5727b12fc7e13eca7d6e5` (tree
`4acbd91f6e676b2b89949bb52992c0be522de40f`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-convention boundary, open task DAG, JSON and
scoped invariants, and a narrow pinned Lean API probe. It does not validate a canonical
Routh-Hurwitz statement or proof because neither has been frozen. The automation-provided
canonical `.lake` symlink was pre-existing and used read-only; no dependency update, build, clone,
fetch, or other `.lake` mutation was performed. This dirty worker evidence is nonrelease evidence.

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

Hurwitz's GDZ article scan, Barkovsky arXiv v1, and Holtz arXiv v1 were downloaded to temporary
storage, inspected at the passages recorded in the crosswalk, and hashed. They were not added to
the repository. This supports theorem-family and convention mapping only. Complete source/proof
review, translation, errata resolution, canonical-root approval, and independent review remain
open, so no `H0` claim is made. The historical scan's terms restrict reuse; the dossier retains
only citation, stable identifiers, page findings, and the observed digest.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1356` | exit 0; rank 966, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 9887,9892 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 60 -sS https://gdz.sub.uni-goettingen.de/download/pdf/PPN235181684_0046/LOG_0026.pdf -o /tmp/hurwitz-gdz.pdf` | exit 0; 13-page, 800020-byte GDZ article scan retrieved; SHA-256 `e625ad...fbad`; pages 273-274 inspected as discovery/source-intake evidence only |
| `curl -L --fail --max-time 45 -sS https://arxiv.org/pdf/0802.1805v1 -o /tmp/barkovsky0802.1805v1.pdf` | exit 0; 43-page Barkovsky v1 PDF retrieved; SHA-256 `da0e65...02c6` |
| `pdftotext -layout /tmp/barkovsky0802.1805v1.pdf /tmp/barkovsky.txt` and bounded `rg`/`sed` inspection | exit 0; strict stability, finite Hurwitz matrix, Theorem 40, and boundary warning inspected |
| `curl -L --fail --max-time 45 -sS https://arxiv.org/pdf/math/0512591v1 -o /tmp/holtz0512591v1.pdf` | exit 0; 4-page Holtz v1 PDF retrieved; SHA-256 `38b234...c79` |
| `pdftotext -layout /tmp/holtz0512591v1.pdf /tmp/holtz.txt` and bounded `rg`/`sed` inspection | exit 0; materially different ascending/infinite-matrix formulation inspected |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1356/IntakeProbe.lean)` | exit 0; twelve adjacent pinned polynomial, root, complex, finite-matrix, submatrix, and determinant API checks elaborated; no target theorem declared |
| exact-topic `rg` search for Routh-Hurwitz, Hurwitz matrix/determinant, and stable polynomial in repo-local and pinned mathlib `.lean` files | exit 1; expected no match; no exact target declaration found; bounded intake discovery rather than an exhaustive external anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1356-pycache python3 -m py_compile Stage1_Instances/THM-M-1356/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1356/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and authoritative-DAG identity, null target, H1/M4/R4 boundary, source pins, exact artifact inventory and hashes, receipt/packet agreement, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-1356` | exit 1; expected no match for prohibited Lean constructs |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

The first draft of `IntakeProbe.lean` checked nonexistent identifiers `Complex.ofReal` and
`Complex.re` without importing the complex module; that narrow command exited 1. The probe was
corrected to import `Mathlib.Data.Complex.Basic` and check `Complex.ofRealHom` and `Complex.re`,
after which the exact recorded recipe passed. No dependency artifact was changed.

## Known open gates

Canonical root selection; a complete accepted source, translation, proof and errata crosswalk;
independent source review; every coefficient/degree/root/matrix/minor/equivalence and boundary
decision; the canonical Lean expression and fingerprints; checked transports and statement
mutations; exhaustive formal anchor audit; discovery and obligation freezes; typed graphs; proof
and composition; trust and provenance closure; readable reconstruction; hermetic replay;
deterministic release bundle; independent verification; master acceptance; audit completion; and
theorem completion remain open. These failures do not invalidate a truthful self-tested `planned`
intake.
