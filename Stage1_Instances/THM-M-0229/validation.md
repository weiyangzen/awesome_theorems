# Intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and non-substitution boundaries, open
task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does not validate a
canonical Great Picard proposition or proof because neither has been frozen. The
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

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0229` | exit 0; rank 1241, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 1654,1659 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded inspection of *Encyclopedia of Mathematics*, stable revision 48178 | exit 0; the finite-value Big Picard statement, infinitely-often consequence, meromorphic sphere variant, and primary bibliographic leads were located; observed response SHA-256 `fa88ffd89368610214e47ee1c953b3ef4a30294fc11474a8764acb6ed35d3997`; H1 lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| `rg -n -i --glob '*.lean' 'great.?picard\|picard.?theorem\|essential.?singular' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | exit 1; expected no-match result; no exact-topic declaration found in this bounded intake search, not an exhaustive external audit or global absence proof |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0229/IntakeProbe.lean)` | exit 0; twelve adjacent punctured-neighborhood, analytic, removable/meromorphic-singularity, and cluster-value APIs elaborated; stdout SHA-256 `1c38c165d88ee0eb4f1e33770ad5f409f5a9c13b36490d08a8c974487ce35fcd`; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0229-pycache python3 -m py_compile Stage1_Instances/THM-M-0229/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0229/check_intake.py` | exit 0; public replay confirmed manifest/DAG identity, planned H1/M4/R3 boundary, null target, source/dependency pins, exact artifact inventory, receipt, and six open tasks |
| `python3 -B Stage1_Instances/THM-M-0229/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; the same invariants plus the seven-key provisional worker packet and packet digest agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| per-new-file `git diff --no-index --check` plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

An accepted immutable source edition and exact proposition, complete incorporated definitions and
premise/conclusion crosswalk, function/domain encoding, isolated-essential-singularity definition,
neighborhood and global-exception quantifiers, finite-plane versus sphere-valued boundary,
recurrence and multiplicity clause, errata audit, and independent source review remain open. So do
the canonical Lean expression and environment fingerprints, checked transports, statement
mutations, exhaustive formal anchor audit, discovery protocol, obligation registry, typed graphs,
proof and composition, trust and provenance closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These open gates do not invalidate a truthful self-tested `planned` intake.
