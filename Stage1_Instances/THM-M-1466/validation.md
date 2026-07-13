# THM-M-1466 intake validation

Base revision: `2a5d4172283e286ab471a929ea09dfe1eaab55cb` (tree
`1fbe559d4eb9b58c24b3f80d1e3ffc19a95907c0`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and non-substitution boundaries, open
task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does not validate a
canonical finite-volume proposition or proof because no source-selected root exists. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

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

## Source boundary

Crossref bibliographic metadata for DOI `10.1016/S1570-8659(00)07005-8` was inspected on
2026-07-13 through the public unauthenticated API and matched
Eymard, Gallouet, Herbin, the title "Finite volume methods," *Handbook of Numerical Analysis*,
2000, pages 713-1018, and Elsevier. The observed response SHA-256 was
`6645995a1d4b228b9817fe57a8fda5faa563dbef1c0c03a1302331a41ae10e99`. No immutable chapter
body, theorem passage, complete assumptions, proof, corrections, catalog root selection, or
independent review was accepted. Mutable Crossref metadata does not support `H0`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1466` | exit 0; rank 1143, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 10700,10705 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -fsSL --retry 2 --max-time 20 -H 'User-Agent: awesome-theorems-stage1-intake/5.6 (mailto:noreply@example.invalid)' 'https://api.crossref.org/works/10.1016%2FS1570-8659%2800%2907005-8' -o /tmp/thm-m-1466-crossref-final.json` | exit 0 on 2026-07-13; SHA-256 `6645995a1d4b228b9817fe57a8fda5faa563dbef1c0c03a1302331a41ae10e99`; public unauthenticated API, mutable bibliographic metadata only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | exit 0; pinned revision and tree recorded above; mathlib worktree clean |
| `rg -n -i 'finite volume\|finite-volume\|FiniteVolume\|numerical flux\|cell average\|conservation law\|conservation-law' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems -g '*.lean'` | exit 0; 39 matches; output SHA-256 `e698f464c63eed63f49338e2325f6d171ead3f189e69e1e1142443eafe70cf8a`; legacy `S1_M_170`/`S1_M_207` conservation-law hits concern continuous compensated-compactness/KdV packages and other matches were unrelated measure/geometry prose; no exact finite-volume discretization target found; bounded intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1466/IntakeProbe.lean)` | exit 0; eight adjacent finite-sum APIs elaborated; representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1466-pycache python3 -m py_compile Stage1_Instances/THM-M-1466/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1466/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, null target, H5/M4/R4 boundary, pins, exact inventory, receipt/packet, and six open tasks agree |
| `rg -n -e '\bsorry\b' -e '\badmit\b' -e '\bsorryAx\b' -e '\baxiom\b' -e '\bconstant\b' -e '\bopaque\b' -e '\bunsafe\b' Stage1_Instances/THM-M-1466 --glob '*.lean'` | exit 1 as expected; no prohibited declaration matched |
| `rc=0; for f in .stage1-worker-selftest.json Stage1_Instances/THM-M-1466/*; do out=$(git diff --no-index --check /dev/null "$f" 2>&1); code=$?; if test -n "$out"; then printf '%s\n' "$out"; rc=1; elif test "$code" -ne 1; then rc=1; fi; done; test "$rc" -eq 0` | exit 0; no whitespace diagnostics in untracked artifacts |
| `git diff --check -- Stage1_Instances/THM-M-1466 .stage1-worker-selftest.json` | exit 0; no tracked-diff whitespace diagnostics |

## Result boundary

The scoped self-test passes only the worker's provisional intake checks. It establishes a
consistent `planned` dossier, not an accepted rev-5.6 node receipt. The first failed theorem gate is
the exact-statement gate: the catalog method gloss does not select one proposition. Source
admission and review; all domain, mesh, flux, update, hypothesis, conclusion, binder, arithmetic,
and boundary decisions; canonical elaboration and mutation tests; discovery and obligation
freezes; anchor audit; proof; composition and trust closure; readable reconstruction; hermetic
replay; deterministic evidence bundling; independent verification; release; and master acceptance
remain open. Accordingly `audit_complete=false` and `theorem_complete=false`.
