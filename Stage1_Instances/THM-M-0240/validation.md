# Intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source and neighbor-scope boundary, open task DAG,
structured invariants, and a narrow pinned Lean API probe. It does not validate a canonical
Abel-Jacobi statement or proof because the catalog does not identify one. The automation-provided
canonical `.lake` symlink was pre-existing and used read-only. No dependency update, build, clone,
fetch, or other `.lake` mutation was performed. This dirty worker evidence is not release evidence.

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
| `python3 scripts/stage1_target.py show THM-M-0240` | exit 0; rank 1251, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short` | preflight exit 0; only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was present |
| `git blame -L 1731,1736 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --retry 3 --fail --silent --show-error --max-time 120 https://www.jmilne.org/math/xnotes/JVs.pdf` | exit 0; SHA-256 `36c3f09c7462dbbd4ae1f8b81a02bd9ff84f03c5a346351d7d5d78fc3f173486`; corrected 2021 edition and Theorems 1.1, 1.2, and 2.5 inspected as distinct source candidates, none admitted as the target or `H0` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0240/IntakeProbe.lean)` | exit 0; seven adjacent pinned scheme, smoothness, properness, Weierstrass-curve, and Jacobian-coordinate interfaces elaborated; complete stdout SHA-256 `000f934cba853b17c2758921194deceeefd0a93fc88929bf8d910aba5d2eb859`; no target theorem declared |
| `rg -n -i --glob '*.lean' 'Abel.?Jacobi\|Jacobian variet\|Picard (scheme\|functor)\|degree.zero Picard' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | exit 1; expected no match; bounded pinned-mathlib discovery only, not an exhaustive external audit |
| the same exact `rg` command with `Formalizations/Lean/AwesomeTheorems` as its final path | exit 0; existing planning prose identifies curve-Jacobian and Picard target debt but no exact formal artifact or proof |
| `python3 -m json.tool Stage1_Instances/THM-M-0240/instance.json` | exit 0; the same command separately passed for `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` |
| `python3 -c "import ast,pathlib; ast.parse(pathlib.Path('Stage1_Instances/THM-M-0240/check_intake.py').read_text())"` | exit 0; scoped validator parsed without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0240/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; target and authoritative-DAG identity, source pins, H5/M4/R4 boundary, null target, exact artifact inventory, provisional receipt, worker packet, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0240` | exit 1; expected no match; no prohibited declaration in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-0240 .stage1-worker-selftest.json` plus `git diff --no-index --check /dev/null <each-new-file>` | exit 0; no whitespace diagnostics, including untracked files |

## Known open gates

The received title/gloss must first be corrected or resolved to one stable proposition. An accepted
immutable primary source, exact incorporated definitions, assumption/conclusion/proof-boundary and
errata crosswalk, algebraic-versus-analytic and neighbor-scope decisions, and independent review
remain open. So do the canonical Lean expression and environment fingerprints, checked transports
and mutations, exhaustive anchor audit, discovery protocol, obligation registry, typed graphs,
proof and composition, trust and provenance closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These open gates do not invalidate a truthful, self-tested `planned` intake.
