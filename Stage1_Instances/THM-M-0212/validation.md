# Intake validation

Base revision: `72e9e8092182121a6794921f61fcc9cae22f726d` (tree
`0d6c1fdf06d1573c256af331c6b198e5a787af43`). Validation date: 2026-07-13
(`Asia/Shanghai`).

This validation covers only the planned dossier, source and scope boundaries, open task DAG,
structured intake invariants, and a narrow pinned Lean API probe. It does not validate a canonical
Brianchon proposition or proof because neither has been frozen. The pre-existing
automation-provided `Formalizations/Lean/.lake` symlink was used read-only. No dependency update,
build, clone, fetch, or other `.lake` mutation was performed. The dirty worker run is nonrelease
evidence.

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

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0212` | 0 | rank 1541; geometry/Euclidean geometry; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | preflight contained only the pre-existing `.lake` symlink; base revision and tree appear above |
| catalog, Stage0, git provenance, and neighboring-target inspection | 0 | sparse gloss, open exact fields, source-record commit, and Pascal/Desargues boundaries recorded |
| arXiv `1202.2340v1` PDF and publisher DOI `10.3906/mat-2102-2` metadata/abstract inspection | 0 | located Valles's complex-projective smooth-conic formulation and duality proof route, plus the second source's wider Brianchon-point configuration; no H0 acceptance |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 at `98dc76e3`; Lake 5.0.0-src+98dc76e |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | mathlib pin and tree above; clean package worktree |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0212/IntakeProbe.lean` | 0 | twelve adjacent APIs elaborated; complete stdout SHA-256 `49378727ad2a2a9561cddf8ec443dab52b1569d7c5e06a0e240c86751e631034`; no target or proof body |
| bounded exact-topic `rg` search in pinned mathlib and repository-local Lean | 1 | expected no-match for Brianchon/circumscribed-hexagon/tangent-hexagon phrases; not an exhaustive anchor audit |
| `python3 -m json.tool` on the four JSON artifacts | 0 | instance, open task DAG, provisional receipt, and worker packet parsed after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0212-pycache python3 -m py_compile Stage1_Instances/THM-M-0212/check_intake.py` | 0 | scoped checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0212/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and DAG identity, current hashes, null formal target, H1/M4/R4 vector, inventory, packet, and six open tasks agreed |
| prohibited Lean construct scan over `IntakeProbe.lean` | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` plus `git diff --check` | 0 | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |

## Open gates

An accepted immutable source and exact row-by-row source review, projective plane and scalar field,
conic and tangency policy, ordered side lines and vertex construction, principal diagonals,
projective concurrency and duality or converse boundary, canonical Lean expression and environment
fingerprint, checked transports and statement mutations, exhaustive anchor audit, obligation
registry, typed graphs, proof and composition, trust closure, readable reconstruction, hermetic
replay, deterministic evidence bundle, independent verification, and master acceptance remain
open. These prevent statement and theorem completion but do not invalidate this fail-closed
`planned` intake.
