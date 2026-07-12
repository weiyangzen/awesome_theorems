# Intake validation

Base revision: `531673f2e97293dd22e5727b12fc7e13eca7d6e5` (tree
`4acbd91f6e676b2b89949bb52992c0be522de40f`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source and neighbor-scope boundary, open task DAG,
structured invariants, and a narrow pinned Lean API probe. It does not validate a canonical
characteristic-exponent statement or proof because the catalog does not identify one. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only. No dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker evidence is
not release evidence.

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
| `python3 scripts/stage1_target.py show THM-M-1354` | exit 0; rank 964, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short` | preflight exit 0; only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was present |
| `git blame -L 9873,9878 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --retry 2 --fail --silent --show-error --max-time 60 http://www.numdam.org/item/ASENS_1883_2_12__47_0/` | exit 0; landing-page citation metadata gives Floquet, the periodic-linear-equations title, 1883, volume 12, pages 47-88, and DOI `10.24033/asens.220`; no proposition or `H0` source admitted |
| `curl -L --retry 3 --fail --silent --show-error --max-time 120 https://api.crossref.org/works/10.24033/asens.220` | exit 0; Crossref metadata independently gives the same bibliographic identity; no proposition or proof text admitted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1354/IntakeProbe.lean)` | exit 0; eleven adjacent pinned periodicity, ODE, matrix, exponential, characteristic-polynomial, spectrum, and eigenvalue interfaces elaborated; no target theorem declared |
| `rg -n -i --glob '*.lean' 'floquet\|characteristic[ _-]*(exponent\|multiplier)\|fundamental[ _-]*matrix.*periodic\|periodic.*fundamental[ _-]*matrix' Formalizations/Lean/AwesomeTheorems` | exit 1; expected no match; bounded repo-local intake discovery only |
| the same exact `rg` command with `Formalizations/Lean/.lake/packages/mathlib/Mathlib` as its final path | exit 1; expected no match; bounded pinned-mathlib discovery only, not an exhaustive external audit |
| `python3 -m json.tool Stage1_Instances/THM-M-1354/instance.json` | exit 0; the same command separately passed for `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` |
| `python3 -c "import ast,pathlib; ast.parse(pathlib.Path('Stage1_Instances/THM-M-1354/check_intake.py').read_text())"` | exit 0; scoped validator parsed without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1354/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; target and authoritative-DAG identity, source pins, H5/M4/R4 boundary, null target, exact artifact inventory, provisional receipt, worker packet, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1354` | exit 1; expected no match; no prohibited declaration in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-1354 .stage1-worker-selftest.json` plus `git diff --no-index --check /dev/null <each-new-file>` | exit 0; no whitespace diagnostics, including untracked files |

## Known open gates

The received title/gloss must first be corrected or resolved to one stable proposition. An accepted
immutable primary source, exact incorporated definitions, assumption/conclusion/proof-boundary and
errata crosswalk, multiplier-versus-exponent and logarithm-branch convention, neighbor-scope
decision, and independent review remain open. So do the canonical Lean expression and environment
fingerprints, checked transports and mutations, exhaustive anchor audit, discovery protocol,
obligation registry, typed graphs, proof and composition, trust and provenance closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These open gates do not invalidate a truthful,
self-tested `planned` intake.
