# THM-M-0278 intake validation

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458`; base tree:
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`. Validation date: 2026-07-13
(`Asia/Shanghai`). This evidence covers only the planned intake node.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone/fetch, or other `.lake` mutation was performed. The
owned outputs and root worker packet make the run dirty nonrelease evidence.

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
- Pinned `Mathlib/Analysis/InnerProductSpace/Dual.lean` SHA-256:
  `26e8e9002c7f599d472f26aad25d57ff899cc8f0907cb3fe43fe0748f9b4ac1d`.

## Commands and results

All commands ran at repository root unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0278` | 0 | rank 1284; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 1999,2004 -L 2225,2230 -- Docs/researches/math_theorems.md` | 0 | both duplicate six-line catalogue records originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && lake --version && lake env lean --version)` | 0 | Lake 5.0.0 and Lean 4.29.0 at the pinned toolchain |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; clean package source |
| `sha256sum` on authority, source, toolchain, lock, pinned dual module, and mathlib bibliography | 0 | hashes recorded in `instance.json` and replay-checked by `check_intake.py` |
| bounded exact-topic `rg` search in pinned mathlib and repo-local Lean | 0 | located the direct Fréchet-Riesz module, mathlib coverage maps, and uses in other targets; discovery evidence only |
| Crossref query for DOI `10.1007/978-3-319-58540-6` | 0 | confirmed Einsiedler/Ward, Springer, 2017, and the ISBNs; no theorem/page locator or H0 admission |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0278/IntakeProbe.lean)` | 0 | five direct interfaces and the explicit candidate `ExistsUnique` wrapper elaborated; output 1217 bytes with SHA-256 `93f3c131b916d8eb29ae1480e5fc06f3d3ea81cc77da50cce84615bbb9ba2ea7`; both axiom reports were `[propext, Classical.choice, Quot.sound]` |
| `python3 -m json.tool` on all structured owned files and the root worker packet | 0 | valid JSON after finalization |
| `python3 -c` with `ast.parse` on `check_intake.py` | 0 | scoped checker parsed without bytecode output |
| `python3 -B Stage1_Instances/THM-M-0278/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, pins, source hashes, null canonical target, H1/M3/R4 boundary, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0278/check_intake.py` | 0 | public replay mode passed without the scheduler-only worker packet |
| prohibited construct scan over `Stage1_Instances/THM-M-0278/*.lean` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; each exit 1 was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0278 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; per-file checks cover untracked files |

## Source and statement boundary

The repository supplies an uncited theorem-family gloss, not an exact proposition. The modern
Einsiedler/Ward book is a credible source lead because the pinned mathlib module cites it, but no
edition copy, theorem/page, incorporated-definition map, proof-node map, correction audit,
historical 1909 reconciliation, or independent review is accepted. No H0 is credited.

The Lean probe is deliberately stronger than a name search: it elaborates a universe-polymorphic
existence-and-uniqueness consequence of `InnerProductSpace.toDual`. But the received gloss does not
fix scalar field, continuity, completeness, inner-product orientation, uniqueness, or norm
preservation. The candidate therefore stays M3 discovery evidence rather than a canonical target
or M0 proof credit.

## Known open gates

Exact source proposition and edition, all definitions and assumptions, proof and errata crosswalk,
historical identity, independent source review, canonical Lean expression and fingerprints,
checked transports, four mutation classes, exhaustive anchor and terminal-body audit, discovery
protocol, obligation registry and typed graphs, proof/composition/provenance/trust closure,
readable reconstruction, hermetic replay, deterministic release evidence, independent
verification, master acceptance, audit completion, and theorem completion all remain open.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0278-INTAKE` only. It supports a planned
dossier, not an accepted receipt. No exact statement, H0, M0, R0, proof, audit completion, theorem
completion, or master acceptance is claimed.
