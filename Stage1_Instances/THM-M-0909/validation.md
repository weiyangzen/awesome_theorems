# Intake validation

Base revision: `39704171d88ffcdc33a47365ae9791f855fa3a44`; base tree:
`050ab5c6392560337051d2eadd1b82277dbe1c4f`.

This validation covers target membership, the planned dossier and open task DAG, catalog
provenance, source-family and scope boundaries, JSON and scoped invariants, a narrow pinned Lean
ordinary-coloring probe, prohibited-construct hygiene, and whitespace. It does not validate a
canonical theorem statement, Voigt's construction, or a proof.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source boundary

Crossref confirmed the 1993 article metadata. Dan S. Archdeacon's zbMATH review Zbl `0790.05030`
defines the relevant choosability convention and reports Voigt's 238-vertex planar graph that is
not 4-choosable. The normalized Crossref subset has SHA-256
`3f0a1b23c5901a3d4a720ca91cec056055ec080e9684553b1fd225fa12f28d14`; the normalized zbMATH
record subset has SHA-256 `140704e4d27cff1166de2499a955cdb39f0517c7f7481e9d1c1269d1950142fc`.
zbMATH identifies the 2006 same-title record as a reprint.

The primary article was not inspected at statement or construction level. The intake therefore
does not claim an exact theorem locator, definition and assumption map, proof boundary, correction
or errata audit, source admission, or H0. A later Gutner author manuscript was inspected only as
secondary corroboration; no proof or statement credit transfers from it.

## Environment fingerprint

- Platform: Linux `7.0.0-27-generic`, x86_64, Asia/Shanghai.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned `Mathlib/Combinatorics/SimpleGraph/Coloring.lean` SHA-256:
  `42c4c6ac9c763df08f33a9fc4cf329e19908dacc630be771a547fcb583f7be56`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0909` | 0 | rank 1451; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6649,6654 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| read-only Crossref query for DOI `10.1016/0012-365X(93)90579-I` | 0 | Voigt title, author, September 1993 date, volume 120, issues 1-3, pages 215-219, and DOI confirmed; no statement text |
| read-only zbMATH query for `List colourings of planar graphs` | 0 | Zbl `0790.05030` review records at-least-k list semantics and the 238-vertex non-4-choosable planar graph; 2006 record labeled reprint; secondary evidence only |
| temporary `curl`, `pdfinfo`, and `pdftotext` inspection of arXiv `0802.2668v1` | 0 | Gutner manuscript restates Voigt's result as Theorem 1.3 and defines finite undirected simple graph choosability; PDF SHA-256 `77e79ea70fad690e7e9273d55d004981103730241c223a39cfed0957b9168665`; secondary corroboration only |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree above; package worktree clean |
| bounded `rg` for Voigt, non-4-choosability, list coloring, choosability, and graph planarity in pinned mathlib and repo-local Lean | 0 | only the coloring module's `Planar graphs` TODO (plus an unrelated `choose_spec` substring) matched; no exact list-coloring, choosability, planarity, or Voigt declaration; intake discovery only |
| read-only inspection of preserved `bsniegowski/lean-planar-graphs` source extracts at `4d560bc5ec87c763d2042b9e7a5dcfc67b6e6c3d` | 0 | list-coloring and combinatorial-planarity interfaces located, but the only adjacent terminal is the positive Thomassen five-list-color result and it contains explicit `sorry` placeholders; no Voigt counterexample or proof credit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0909/IntakeProbe.lean)` | 0 | eight adjacent ordinary-coloring interfaces elaborated; complete output SHA-256 `0852835123f503927196ecd4ebe73804ba4a22403f17e67d8f0ebe4b20417051`; no target statement or proof credit |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all final structured artifacts are valid JSON |
| Python `ast.parse` on `Stage1_Instances/THM-M-0909/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0909/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H1/M4/R4 boundary, null target, inventory, source hashes, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0909/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0909 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked files are covered by the preceding no-index checks |

## Known downstream failures

- No independently approved immutable primary source, pinpoint statement, definition and assumption
  map, construction audit, complete proof boundary, correction or errata audit, or H0 review exists.
- Finite simple graph, planarity or embedding, color and list carrier, exact versus lower-bound list
  size, choosability binder order, bad-list witness, 238-vertex scope, and boundary cases remain open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen. Pinned mathlib supplies ordinary coloring
  substrate but no located graph-planarity or list-choosability interface.
- Formal anchor and provenance audit, discovery and obligation freezes, typed graphs, proof,
  composition, trust closure, readable reconstruction, hermetic replay, deterministic bundle,
  independent release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake. Only the integration lane may accept the
provisional worker receipt.
