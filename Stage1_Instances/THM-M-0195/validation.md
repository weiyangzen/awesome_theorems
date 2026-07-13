# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2` (tree
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target-set membership, the planned dossier, repository-source provenance,
scope and source-statement crosswalks, the six-task open DAG, structured invariants, and a pinned
Lean discovery probe. It does not validate a canonical Euler-line proposition or proof because the
primary statement, center-definition mapping, exact conclusion boundary, and checked transport
remain open.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This dirty worker run is nonrelease evidence.

## Environment

- Linux `7.0.0-27-generic`, x86_64; timezone `Asia/Shanghai`.
- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned `MongePoint.lean` SHA-256:
  `e319a267949c6ec11cdf39f3b9ceb67a186c07d596e94de41dc6a83301211aaf`.

## Commands and results

All repository commands ran at the repository root unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0195` | 0 | rank 1224, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only the pre-existing automation `Formalizations/Lean/.lake` symlink was untracked; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 1408,1413 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '1408,1413p' Docs/researches/math_theorems.md \| sha256sum` | 0 | exact catalog block SHA-256 `5470fe3b343b3ba7076de91af9c790e5221d992208834af2805ec16bbeac3ce2` |
| repository source and Stage0 inspection | 0 | no primary source, exact definitions, binders, hypotheses, conclusion encoding, proof, errata, reviewer, or formal artifact is supplied |
| bounded University of the Pacific Euler Archive E325 record and primary-scan inspection | 0 | matching work identified: written 1763, published 1767, *Novi Commentarii* 11, 103-123; center definitions and later ratio passages located as H1 evidence; complete Latin statement/proof translation, correction audit, immutable admission, and independent review remain open |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0195/IntakeProbe.lean)` | 0 | ten pinned triangle-center, Euler-position, collinearity, and affine-span interfaces elaborated; both axiom reports were `[propext, Classical.choice, Quot.sound]`; output SHA-256 `b3cda0db83d11fcfdae2809de7adbdabe6b08cd0bd0e3b16bd8b0c6ba2c90796` |
| bounded `rg` search over pinned mathlib and repo-local Lean | 0 | direct Monge-point and orthocenter interfaces located; no existing repo-local Euler-line target found; this is bounded intake discovery, not an exhaustive anchor audit or global absence proof |
| `python3 -m json.tool` separately on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured records are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0195-pycache python3 -m py_compile Stage1_Instances/THM-M-0195/check_intake.py` | 0 | target-scoped validator compiles without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0195/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, source and dependency hashes, H1/M3/R4 boundary, null canonical target, artifact hashes, receipt/packet agreement, and six open tasks agree |
| token-anchored prohibited Lean declaration scan over `IntakeProbe.lean` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration; diagnostic `#print axioms` commands are intentionally permitted |
| scoped new-file whitespace checks and `git diff --check` | 0 | no whitespace, CR, NUL, missing-final-newline, or inventory diagnostics |

## Known open gates

- A matching primary work and relevant passages were located, but no immutable source packet has
  been admitted; complete Latin transcription, exact definitions, assumptions, conclusion, proof
  boundary, modern notation and ratio translation, corrections or errata, and independent review
  remain open.
- The root does not yet select ambient dimension and representation, exact triangle and center
  definitions, bare rank-based collinearity versus the stronger position/ratio/order result, or
  all degenerate-case conventions.
- No canonical Lean expression, minimal-import statement receipt, expression or environment
  fingerprint, checked alternate encoding, or required semantic mutation exists.
- Exhaustive anchor/provenance audit, discovery precommit, obligation registry, typed graphs,
  proof, child-to-parent composition, trust closure, readable reconstruction, hermetic replay,
  deterministic evidence bundle, and independent release verification remain open.
- Master acceptance is pending.

These failures prevent exact-statement, audit-completion, and theorem-completion claims. They do
not invalidate a truthful, self-tested `planned` intake whose deliverable is the dossier, scope
map, source-statement crosswalk, and open downstream DAG.
