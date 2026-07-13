# Intake validation

Validation date: `2026-07-13` (`Asia/Shanghai`). Base revision:
`997541734bb32f987fb15f163335a82512992120`; base tree:
`2c866b9d840d48c48ac839740c62d3b9440be0e5`.

This validation covers target membership, the planned dossier and open task DAG, exact catalog
provenance, a historical source locator, JSON and scoped invariants, a narrow pinned Lean API
probe, prohibited-construct hygiene, and whitespace. It does not validate a canonical statement or
proof because the catalog omits the actual characterization and its assumptions.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned files and root worker packet make the final tree dirty
and nonrelease.

## Source boundary

The University of the Pacific Euler Archive E53 record was inspected at HTML SHA-256
`cc9dae231be60f5eee526e1ae8899963ab763f9dcb3f4ebc6c445cfd5b5d30ba`. It identifies Euler's
*Solutio problematis ad geometriam situs pertinentis*, says it was written in 1735 and published
in 1741, and summarizes the Konigsberg impossibility argument. That does not establish the
catalog's date 1736 or one exact modern general iff. A PDF was retrieved at SHA-256
`7e32421527d27b83fa6c2ebf1bfadfdbacbdba86efd4449bd4b954f4b505ca58`, but `pdfinfo` and
`pdftotext` rejected its invalid xref/page structure. No source passage was credited.

## Environment fingerprint

- Platform: Linux 7.0.0-27-generic, x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- `Mathlib/Combinatorics/SimpleGraph/Trails.lean` SHA-256:
  `07dbbdce3ca11a5e32935403e14d0217fac0a7fe4abdd37991d910ad4bd76561`.

## Commands and results

All repository commands ran at the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0811` | 0 | rank 1370; planned; no legacy slot; legacy artifacts unaccepted; intake score 86; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 5963,5968 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Euler Archive HTML retrieval and inspection | 0 | E53 metadata and summary inspected outside the repo; observed HTML hash recorded; dates are 1735/1741 |
| Euler Archive PDF retrieval, `pdfinfo`, and `pdftotext` | 1 | retrieval succeeded and hash recorded, but both parsers rejected invalid xref/page structure; no passage credited |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0811/IntakeProbe.lean)` | 0 | six Eulerian definition/necessary-direction interfaces elaborated; output SHA-256 `0b8fcd3037e960843ceda587a3b90419037822a78cfceba648fa7eab0ee9416b` |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0811/check_intake.py` | 0 | validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0811/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H1/M3/R4 boundary, null target, exact inventory, source hashes, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0811/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file means only that each file is new |
| `git diff --check -- Stage1_Instances/THM-M-0811 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; no-index checks cover untracked files |

## Known downstream failures

- The catalog does not state the characterization or fix graph type, finiteness, connectivity and
  isolated-vertex convention, endpoints, circuit inclusion, parity formulation, or boundary cases.
- The historical locator neither supplies an accepted modern general iff nor reconciles the
  catalog's 1736 date; exact source statement, proof, corrections, mapping, and review remain open.
- Pinned mathlib has only definition and necessary-direction interfaces for this target family and
  explicitly records the converse existence direction as TODO.
- No canonical Lean expression, minimal import, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen.
- Formal anchor and provenance audit, discovery and obligation freezes, typed graphs, proof,
  composition, trust closure, readable reconstruction, hermetic replay, deterministic bundle,
  independent validation, release, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake. Only the integration lane may accept the
provisional worker receipt.
