# Intake validation

Base revision: `2eea98305d46266f078a50cf0e85853bf6a5e702`; base tree:
`02279a8caa5f31ed8e37e35c8584a336eed9b974`.

Validation is limited to target-set consistency, the planned dossier and open downstream DAG,
repository-source provenance, pinned environment identity, a narrow Lean exact-topic API probe,
proof-escape hygiene, JSON and scoped invariants, and whitespace. It does not validate a canonical
theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No `lake
update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed. This is
dirty, nonrelease worker evidence.

## Environment fingerprint

- Platform: Linux x86_64, kernel `7.0.0-27-generic`, timezone Asia/Shanghai.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All commands ran on 2026-07-13 Asia/Shanghai. Repository-root commands are shown without a `cwd`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0280` | 0 | rank 1286; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 2013,2018 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalogue lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3...16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` and status | 0 | pinned revision/tree above; package worktree clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes match the environment fingerprint |
| bounded exact-topic `rg` search over pinned mathlib and repo-local Lean | 0 findings classified | located direct `eLpNorm`, `lpNorm`, explicit integral, quotient `Lp`, and finite-sum candidates plus unrelated Minkowski namesakes; not an exhaustive anchor audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0280/IntakeProbe.lean)` | 0 | five candidate interfaces elaborated; four direct theorem axiom reports each showed `[propext, Classical.choice, Quot.sound]`; output SHA-256 `06295a3965083752673a8dc0ced2ed75c9919708deb3ff73b3c9f4f2d164d2cb` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0280-pycache python3 -m py_compile Stage1_Instances/THM-M-0280/check_intake.py` | 0 | scoped validator compiled without writing generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0280/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, H1/M3/R4 boundary, null target, source and candidate pins, exact artifact inventory, packet agreement, probe replay, and six open tasks agree |
| prohibited Lean proof-escape scan over `IntakeProbe.lean` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0280 .stage1-worker-selftest.json` plus scoped new-file checks | 0 | no whitespace diagnostics in changed files |

## Known downstream failures

- No immutable exact primary or authoritative source, statement/formula, incorporated definition
  and assumption map, proof boundary, correction or errata check, or independent review is accepted.
- The root has not selected the exponent representation and endpoints, measure assumptions,
  codomain, measurability/integrability premises, representative or quotient formulation, extended-
  infinite semantics, or exact conclusion encoding.
- No canonical Lean expression, minimal imports, expression/environment fingerprint, checked
  transport, or statement mutation exists.
- Discovery protocol, exhaustive anchor audit, obligation registry and typed graphs, proof,
  composition and trust closure, readable reconstruction, hermetic replay, deterministic evidence
  bundle, and independent release verification remain open.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity and evidence
boundary. Only the integration lane may accept the provisional worker receipt.
