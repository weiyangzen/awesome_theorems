# Intake validation

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a` (tree
`fdfff18dea4c6798c5b322b6088dfe556109c134`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers only the planned dossier, source-statement and non-substitution boundaries,
open task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does not
validate a canonical Green-Tao-Ziegler proposition or proof because neither has been frozen. The
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
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0946` | exit 0; rank 1485, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 6910,6915 -- Docs/researches/math_theorems.md` | exit 0; all six sparse catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded primary-source inspection | exit 0; Green-Tao arXiv `math/0606088v2` Main Theorem, Corollary 1.7, Theorem 1.8, and Corollary 1.9 located; 84-page PDF SHA-256 `4cc772cfa6f2f9fa2af82d07b6323669c8150ac1911e83a245cc667f956500f5`; discovery only |
| bounded dependency-source inspection | exit 0; Green-Tao-Ziegler arXiv `1009.3998v5` Theorem 1.3 and finite-complexity application text located; 116-page PDF SHA-256 `24b5b74b1c4f31986bfc75955f8528e81753efc0c45bd99bc23fee58171a4711`; discovery only |
| bounded secondary-source discrimination | exit 0; Bienvenu arXiv `1607.06625v1` Theorem 1.1 and explicit Green-Tao-Ziegler naming explanation located; 20-page PDF SHA-256 `440ab085d68922005e9a4824ce32eae5a8d27e293e6fc8dd8105304593effdee`; secondary discovery only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| bounded exact-topic `rg` searches in pinned mathlib and repository-local Lean | exit 1 expected no-match; no Green-Tao-Ziegler, linear-equations-in-primes, finite-complexity prime-pattern, inverse-Gowers, or nilsequence root declaration found; intake discovery only |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0946/IntakeProbe.lean)` | exit 0; eight adjacent APIs elaborated; combined-output SHA-256 `5b66078e382fd3068381d7f6f859826f23c376dcf96ced619fe01ee59029aa7e`; three axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target declaration or proof body |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0946-pycache python3 -m py_compile Stage1_Instances/THM-M-0946/check_intake.py` | exit 0; scoped validator compiled without adding generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0946/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; authority identity, current hashes, null target, H1/M4/R4 boundary, exact inventory, receipt/worker packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0 after finalization; no whitespace errors |

## Known open gates

One immutable root and edition, complete incorporated-definition/premise/conclusion/correction
crosswalk, authorship/year interpretation, conditional-versus-unconditional dependency boundary,
affine-form-versus-matrix encoding, and independent source review remain open. So do the canonical
Lean expression and environment fingerprints, checked transports, statement mutations, exhaustive
formal anchor audit, discovery protocol, obligation registry, typed graphs, proof and composition,
trust and provenance closure, readable reconstruction, hermetic replay, deterministic evidence
bundle, independent verification, and master acceptance. These failures do not invalidate a
truthful self-tested `planned` intake. Verdict: `no_state_change`; `audit_complete=false` and
`theorem_complete=false`.
