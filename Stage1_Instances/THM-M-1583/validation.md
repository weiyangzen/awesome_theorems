# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2`; base tree:
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`. Validation date: 2026-07-13
(Asia/Shanghai); exact start and end timestamps are recorded in the provisional receipt.

This validation covers target membership, the planned dossier and open task DAG, literal repository
source provenance, field-versus-proposition and neighboring-record discrimination, JSON and scoped
invariants, a narrow pinned Lean substrate probe, bounded repository/mathlib search,
prohibited-construct hygiene, and whitespace. It does not validate a canonical algorithmic-
information theorem or proof because the catalog supplies no truth-valued proposition.

The preflight worktree contained only the automation-provided untracked `Formalizations/Lean/.lake`
symlink to canonical pinned artifacts. It was used read-only. No `lake update`, `lake build`,
dependency clone or fetch, network-triggering Lake operation, or other `.lake` mutation was
performed. The owned intake files and root worker packet make the final tree dirty and nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean before and after the
  probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source discovery boundary

The catalog record and Stage0 projection were inspected at the pinned repository revision. They
name algorithmic information theory, give broad historical attribution, and contain no proposition
or source citation. Neighboring mathematical and computer-science records were inspected to keep
Kolmogorov complexity, incompressibility, and Chaitin's uncomputable-number families separate.

No external source file was added. No exact theorem, source edition, result locator, incorporated
definition, assumption map, proof boundary, translation or correction record, target-ownership
decision, or independent review was accepted. Historical attribution supports truthful field
classification only, not `H0` admission.

## Commands and results

All repository commands ran at the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1583` | 0 | rank 1205; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 11665,11670 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above; package status clean |
| `sha256sum` on authoritative manifests, source records, toolchain, lock, and three probed mathlib modules | 0 | hashes recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1583/IntakeProbe.lean)` | 0 | seven adjacent partial-recursive-code and finite coding APIs elaborated; complete output SHA-256 `eb75d536041de2a97c47c9c59db16fc101d1da563691d7e6f9a285b88f03a91a`; no target declaration or proof body |
| bounded case-insensitive algorithmic-information exact-topic `rg` search in repo-local Lean and pinned mathlib | 1 (expected no match) | no algorithmic-information, Kolmogorov-complexity, universal-prefix-machine, Solomonoff, Chaitin-Omega, or Martin-Lof-randomness target; intake discovery only |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | every structured artifact is valid JSON after finalization |
| `python3 -c` with `ast.parse` on `Stage1_Instances/THM-M-1583/check_intake.py` | 0 | scoped validator parsed without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1583/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and dependency hashes, H5/M4/R4 null target, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1583/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| `sha256sum` on the root worker packet and eight non-receipt owned intake files | 0 | raw SHA-256 values recorded and replay-checked by the scoped validator; the self-referential receipt output is excluded from its own digest map |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1583 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; per-file no-index checks cover all untracked artifacts |

## Known open gates

An accepted correction, redirect, or split; one stable truth-valued root; exact immutable primary
source; complete definition/premise/conclusion/proof-boundary and correction crosswalk; neighboring
ownership decision; and independent review remain open. So do the canonical Lean target and
minimal imports, expression/environment fingerprints, checked transports, four statement mutation
classes, exhaustive anchor audit, discovery protocol, obligation registry, typed graphs, proof and
composition, source/provenance/trust closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion.

`H5` classifies only the received field label and gloss as non-propositional; it makes no claim that
any proper algorithmic-information theorem is false, independent, or open. These failures block
ordinary theorem-proof execution but do not invalidate a truthful self-tested `planned` intake.

## Status boundary

This is provisional worker self-test evidence for `S56-M-1583-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, `H0` source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.
