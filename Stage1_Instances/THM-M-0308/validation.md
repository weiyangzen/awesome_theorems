# Intake validation

Base revision: `d257e1e5e5fa003d6e1f26344c0331bf99374fa9` (tree
`fa06b50b528e038d182d5479a18296f63fa5eae5`).

All commands ran from the isolated worker clone on 2026-07-13 in timezone `Asia/Shanghai`.
Validation covers target membership, the planned dossier and open DAG, JSON and scoped invariants,
duplicate source-record discrimination, adjacent pinned Lean APIs, prohibited constructs, and
whitespace. The automation-provided `.lake` symlink and canonical pinned artifacts were used read
only. No Lake update or build, dependency clone or fetch, or `.lake` modification was performed.

No canonical proposition has been selected. The Lean probe is substrate evidence only and neither
elaborates nor proves a Sobolev extension theorem.

## Environment fingerprint

- Platform: Linux x86_64, kernel `7.0.0-27-generic`.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0308` | 0 | rank 1309, planned, L0/rework-required, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was untracked; preserved read only |
| `git blame -L 2209,2214 -- Docs/researches/math_theorems.md` and lines `9059,9064` | 0 | both six-line uncited records originate at commit `bcf3f9fa...` and are byte-identical |
| excerpt SHA-256 checks on catalog lines `2209-2214`, `9059-9064`, and Stage0 lines `8494-8519` | 0 | catalog blocks both `ec0360e...a2c50`; Stage0 block `2920b8cc...ebfc` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0308/IntakeProbe.lean)` | 0 | eight adjacent `L^p`, continuous-linear-map, and Sobolev-inequality API checks elaborated; stdout SHA-256 `a144900e...69d2`; no target theorem was stated |
| bounded `rg` for Sobolev extension names in repo-local Lean and pinned mathlib | 0 | matched only the distinct `S1_M_175.lean` embedding boundary and an unrelated occurrence in `S1_M_127.lean`; no exact target declaration found; scoped intake search only |
| `python3 -m json.tool` separately on owned JSON and `.stage1-worker-selftest.json` | 0 | planned instance, open task DAG, provisional receipt, and worker handoff parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0308-pycache python3 -m py_compile Stage1_Instances/THM-M-0308/check_intake.py` | 0 | scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0308/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | after finalization, target identity, pins, planned H5/M4/R4 boundary, null target, duplicate source records, strict handoff, and six open tasks agree |
| scoped Lean scan for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declarations | 1 | expected no-match; no proof escape declaration in the API-only probe |
| scoped `git diff --check` plus no-index checks for every untracked changed file | 0 | no whitespace diagnostics |

## Known downstream failures

- No immutable primary source, exact theorem and incorporated definitions, assumption/conclusion
  map, genealogy, translation, correction history, or independent review is accepted.
- Domain, extension-domain regularity, Sobolev model and parameters, values, operator versus
  per-function form, restriction identity, norm estimate, constants, support behavior, ordered
  binders, and boundary cases are not selected by the catalog.
- No canonical Lean target, exact minimal imports, elaborated expression/environment fingerprint,
  checked alternate encoding, or required statement mutation exists.
- Formal anchor audit, discovery protocol, obligation registry, typed graphs, proof, composition,
  trust closure, readable reconstruction, hermetic replay, deterministic evidence bundle, and
  independent release verification remain open.

These failures block statement and theorem completion but do not invalidate a truthful,
self-tested `planned` intake that freezes the ambiguity boundary and opens the dependency DAG. Only
the integration lane may accept the provisional receipt.
