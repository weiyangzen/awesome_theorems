# Intake validation

Base revision: `dd8846dbc83818f6ba7124151d5d4b7b29bb5b0d` (tree
`1bf3680085cf7338ac4d405cf4ef2188fa14ccec`). Validation ran on 2026-07-12/13 in the
isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, primary
source discovery, neighbor-target boundaries, pinned environment identity, a narrow Lean API
probe, a bounded local exact-topic search, proof-escape hygiene, JSON integrity, and whitespace.
The catalog describes a proof and does not select one proposition, so no canonical target,
expression hash, statement mutation, source acceptance, or proof is claimed.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

Environment fingerprint:

- Platform: Linux x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1439` | 0 | rank 937, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git blame -L 10509,10514 -- Docs/researches/math_theorems.md` | 0 | all six uncited target-record lines originate at commit `bcf3f9fa...b74f` |
| bounded primary-source discovery and inspection of arXiv `math/9903201v1` | 0 | 102-page published-version PDF inspected; abstract and pages 320-323 distinguish bounded-type hyperbolicity, stationary scaling, and other named theorems; PDF SHA-256 `8e324963...a9e0` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| Python `ast.parse` on `Stage1_Instances/THM-M-1439/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1439/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, neighbor boundaries, planned H5/M4/R4 state, null target, exact artifact inventory, provisional packet, and six open tasks agree |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1439/IntakeProbe.lean)` | 0 | eleven adjacent pinned complex, analytic, iteration, semiconjugacy, compactness, connectedness, and linear-operator APIs elaborated; no Lyubich theorem |
| bounded exact-topic `rg` over repo-local and pinned-mathlib Lean sources | 1 | expected no-match exit after excluding unrelated generic renormalization uses; no Feigenbaum/Coullet/Tresser/Lyubich, quadratic-like-germ, hybrid-class, or Mandelbrot-copy renormalization declaration found; intake discovery only |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1439 .stage1-worker-selftest.json` plus scoped new-file checks | 0 | no whitespace diagnostics in changed files |

## Known downstream failures

- The catalog proof label is not a stable proposition. The exact-match primary paper presents
  multiple candidate roots and therefore confirms rather than resolves the ambiguity.
- No approved canonical-root correction, independently reviewed exact theorem and full
  definition/assumption/proof/errata crosswalk, or reconciliation with `THM-M-1437` and
  `THM-M-1438` exists.
- No canonical Lean expression, expression/environment hash, exact imports, checked alternate
  encoding, or statement mutation test exists.
- Discovery protocol, anchor audit, obligation registry and typed graphs, proof, composition and
  trust checks, readable reconstruction, hermetic replay, deterministic evidence bundle, and
  independent release verification are open.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity boundary and open
DAG. Only the integration lane may accept the provisional worker receipt.
