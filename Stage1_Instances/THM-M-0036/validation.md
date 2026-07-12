# THM-M-0036 intake validation

Base revision: `dc2eb1390c8f2a88e7afcbdbd35f92ab43f64fb8`; base tree:
`25138aaafcff80ee47bf04805bccd804978e6754`. Validation date: 2026-07-13
(Asia/Shanghai). This evidence covers only the planned intake node.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone/fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned outputs and worker packet make the run dirty nonrelease
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

All commands ran at repository root unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0036` | 0 | rank 1079; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 277,282 -- Docs/researches/math_theorems.md` | 0 | all six catalogue fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && lake --version && lake env lean --version)` | 0 | Lake 5.0.0 and Lean 4.29.0 at the pinned toolchain |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; clean package source |
| `sha256sum` on authority, source, toolchain, lock, two probed mathlib modules, and foreign wrapper | 0 | hashes recorded in `instance.json` and replay-checked by `check_intake.py` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0036/IntakeProbe.lean)` | 0 | `CSA` and three pinned Wedderburn-Artin candidate declarations elaborated; both simple-ring candidates report `propext`, `Classical.choice`, and `Quot.sound`; no canonical target declared |
| `python3 -m json.tool` on all structured owned files and root packet | 0 | valid JSON after finalization |
| `python3 -c` with `ast.parse` on `check_intake.py` | 0 | scoped checker parsed without bytecode output |
| `python3 -B Stage1_Instances/THM-M-0036/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, input hashes, null statement, H1/M3/R4 boundary, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0036/check_intake.py` | 0 | public replay mode passed without scheduler-only packet |
| prohibited construct scan over `Stage1_Instances/THM-M-0036/*.lean` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; each exit 1 was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0036 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; per-file checks cover untracked files |

## Source and statement boundary

The repository supplies only a six-line catalogue record. Artin's 1927 paper is recorded as a
bibliographic lead, not an inspected and accepted theorem passage. The exact source proposition,
definitions, assumptions, proof-node mapping, corrections/errata status, Wedderburn genealogy, and
independent review remain open. No H0 is credited.

The pinned probe is an API and axiom inspection only. In particular, the finite mathlib candidate
does not visibly return `Algebra.IsCentral K D`, although a source-selected CSA classification may
require the division algebra to be central. No source identity, expression fingerprint, checked
transport, proof-body audit, or M0 is credited.

## Known open gates

Exact source assertion and formulation selection, definition/assumption/proof crosswalk, errata
audit, independent source review, canonical Lean elaboration and fingerprints, checked transports,
four mutation classes, exhaustive anchor and terminal-body audit, discovery protocol, obligation
registry and typed graphs, proof/composition/provenance/trust closure, readable reconstruction,
hermetic replay, deterministic release evidence, independent verification, master acceptance,
audit completion, and theorem completion all remain open.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0036-INTAKE` only. It supports a planned
dossier, not an accepted receipt. No exact statement, H0, M0, R0, proof, audit completion, theorem
completion, or master acceptance is claimed.
