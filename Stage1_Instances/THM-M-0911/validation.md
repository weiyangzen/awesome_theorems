# Intake validation

Base revision: `39704171d88ffcdc33a47365ae9791f855fa3a44` (tree
`050ab5c6392560337051d2eadd1b82277dbe1c4f`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source-statement and
non-substitution boundaries, the six-node open task DAG, scoped intake invariants, and one narrow
pinned Lean discovery probe. It does not freeze or validate a canonical binomial proposition,
audit a terminal proof body, or confer proof credit. The automation-provided canonical `.lake`
symlink was pre-existing and used read-only; no dependency update, build, clone, fetch, or other
`.lake` mutation was performed. This dirty worker run is nonrelease evidence.

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
- Pinned `Mathlib.Data.Nat.Choose.Sum` source SHA-256:
  `24629e74afa48706f470fccab4c8bfadd229e42e07ce8ba2e192aee4af6d3fe3`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0911` | exit 0; rank 1453, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 6663,6670 -- Docs/researches/math_theorems.md` | exit 0; all catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded repository and pinned-mathlib search for binomial/add-power declarations | exit 0; direct commutative, commuting-element, and antidiagonal candidates found in `Mathlib.Data.Nat.Choose.Sum`; nearby formulas kept outside scope |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0911/IntakeProbe.lean)` | exit 0; four exact-topic APIs elaborated; a commutative wrapper, equality with the explicit-commutation form, range-sum `n = 0` and `n = 2` boundaries, and the antidiagonal `n = 2` boundary kernel-checked; inspected candidates reported `propext`, `Classical.choice`, and `Quot.sound`; stdout SHA-256 `1fca6d3559b745f876989ffe3e68552566c2c0c32ebde377582bea2101e7c2e8` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0911-pycache python3 -m py_compile Stage1_Instances/THM-M-0911/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0911/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest and DAG identity, pins, `H1/M3/R4` null-target boundary, receipt, packet, exact inventory, Lean replay, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped `git diff --no-index --check /dev/null <new-file>` loop, followed by `git diff --check -- Stage1_Instances/THM-M-0911 .stage1-worker-selftest.json` | exit 0; every new owned file and the worker packet passed explicit whitespace validation, with no tracked-diff diagnostics |

An exploratory `/tmp` probe included the nonexistent identifier `Finset.sum_range` and exited 1
after the actual binomial declarations and axiom reports had elaborated. The invalid line was not
copied into the owned probe and grants no evidence. The final owned probe above passed cleanly.

## Known open gates

An admitted immutable primary or authoritative statement, pinpoint theorem/page, historical
attribution and date audit, definitions, assumptions, correction or errata review, and independent
source approval remain open. So do the exact coefficient domain, commutativity premise, coefficient
cast or scalar action, summation and exponent conventions, binder order, boundary contract,
expression and environment fingerprints, checked alternate transports, and statement mutations.
The exhaustive formal-anchor, terminal-body, provenance, dependency, axiom, and TCB audits;
discovery and obligation freezes; typed graphs; proof and composition; readable reconstruction;
hermetic replay; deterministic bundle; independent verification; audit completion; theorem
completion; and master acceptance also remain open. These gates prevent any theorem-completion
claim but do not invalidate a truthful self-tested `planned` intake.
