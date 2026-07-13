# Intake validation

Base revision: `c5f6fb269f6eb84efa935ee66c4e9bab92495e61`; base tree:
`7a41063c920c1b9cb849aa35c2f02ec4a4733655`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, exact human scope and non-substitution boundaries, pinned environment identity, a
narrow Lean API/finite-scope probe, JSON integrity, prohibited-construct hygiene, and whitespace.
It does not validate a canonical Lean declaration, expression fingerprint, source proof, or proof
closure; those are downstream gates.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The owned intake files and root worker packet make the final tree dirty and nonrelease.

## Source boundary

The catalog sentence is sufficiently specific to freeze the human mathematical claim: every
subgroup of a finite group has order dividing the group's order. It supplies no proof citation.
Dummit and Foote, *Abstract Algebra*, third edition, section 3.2 is recorded only as a modern
bibliographic lead; no stable copy or pinpoint proof passage was inspected. Historical attribution,
exact primary source, definitions, proof-node crosswalk, corrections, errata, and independent
review remain open, so the source classification is H1 rather than H0.

## Environment fingerprint

- Platform: Linux x86_64; kernel `7.0.0-27-generic`.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned `Mathlib/GroupTheory/Coset/Card.lean` SHA-256:
  `cb3efb11057211d161637ba7e6c75d64271faa95e5bdafff96f82168329b236e`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0061` | 0 | rank 1093; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 456,461 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa...b74f` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the recorded environment; no update/build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; mathlib worktree clean |
| bounded exact-topic search in repo-local Lean and pinned mathlib | 0 | `Subgroup.card_subgroup_dvd_card` located as the close formal candidate; the legacy `S1_M_061.lean` belongs to THM-M-0433 |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0061/IntakeProbe.lean)` | 0 | Lagrange and quotient-card APIs elaborated; finite-scope, bottom, and top examples passed; candidate reports `[propext, Classical.choice, Quot.sound]` |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all finalized structured artifacts are valid JSON |
| Python `ast.parse` on `Stage1_Instances/THM-M-0061/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0061/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, H1/M3/R4 scope boundary, pins, inventory, packet agreement, and six open tasks passed |
| `python3 -B Stage1_Instances/THM-M-0061/check_intake.py` | 0 | public replay mode passed |
| `rg` prohibited declaration scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration found |
| per-file `git diff --no-index --check /dev/null` for every owned file and root packet | 0 aggregate | no whitespace diagnostics; new-file difference exit is ignored |
| `git diff --check -- Stage1_Instances/THM-M-0061 .stage1-worker-selftest.json` | 0 | no tracked-diff whitespace diagnostics; untracked files covered by the preceding checks |

## Known downstream failures

- No primary source edition, theorem/page, definitions, proof passage, correction/errata decision,
  source-to-node mapping, or independent H0 review is accepted.
- No canonical Lean declaration or normalized expression/environment fingerprint is frozen.
- `Finite`/`Nat.card` versus `Fintype`/`Fintype.card`, the additive boundary, alternate transports,
  and the required statement mutations remain open.
- The close pinned theorem deliberately has a stronger domain than the finite catalog claim; it has
  not undergone exact wrapper identity, terminal-body, transitive provenance, placeholder, axiom,
  or complete TCB audit.
- Discovery protocol, obligation registry, typed graphs, proof/composition, readable
  reconstruction, hermetic replay, deterministic evidence bundle, independent verification,
  release, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful self-tested `planned` intake. Only the integration lane may accept the
provisional worker receipt.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0061-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No H0, M0, R0, accepted proof state, audit completion,
theorem completion, or master acceptance is claimed.
