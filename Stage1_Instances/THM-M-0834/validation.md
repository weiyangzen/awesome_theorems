# Intake validation

Base revision: `be8701e88e791545c16a262edd1909486d5cef4b`; base tree:
`78b0a751473bf6d71f453a6aad18b130268a3428`.

This validation covers target membership, the planned dossier and open task DAG, catalog
provenance, scope and source boundaries, JSON and scoped invariants, a narrow pinned Lean coloring
probe, prohibited-construct hygiene, and whitespace. It does not validate a canonical theorem
statement or proof because the source does not freeze the graph and planarity encoding.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source boundary

The uncited catalog record was traced to its introduction commit. The standard historical lead is
P. J. Heawood, *Map-Colour Theorem*, *Quarterly Journal of Pure and Applied Mathematics* 24 (1890),
332-338. The identity was independently confirmed by zbMATH/JFM record `22.0562.02`; its secondary
review describes line-adjacent plane regions and the improvement from six to five colors. The
intake did not admit an immutable primary text or inspect a pinpoint statement, definitions, proof
boundary, corrections, or errata. The exact finite graph/map scope and the transport to a modern
graph-planarity proposition also lack independent review, so the source classification remains H1
rather than H0.

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
- Pinned `mathlib/docs/1000.yaml` SHA-256:
  `12792e25ca081fb16c149223f9920c0dff1214ebe5e46b026e15829862a0130c`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0834` | 0 | rank 1392; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6124,6129 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| read-only zbMATH API inspection of document `2689944` | 0 | JFM `22.0562.02` confirms Heawood 1890, volume 24, pages 332-338; normalized bibliographic TSV SHA-256 `74bc517d8586bf6ca007053236adc9162ef6505c0fccabfe8acda1a39447ca54`; secondary review only |
| bounded exact-topic `rg` over repo-local Lean and pinned dependencies | 0 | no exact five-color, Heawood, map-color, or graph-planarity declaration; coloring docs list planar graphs as TODO and the thousand-theorem index has the title without a declaration |
| read-only GitHub source inspection of `bsniegowski/lean-planar-graphs` at `4d560bc5ec87c763d2042b9e7a5dcfc67b6e6c3d` | 0 | syntactic `PlanarGraph.fiveColorable` lead depends on numerous `sorry`-backed results and Lean 4.30.0-rc2; blocked with no proof credit |
| `(cd Formalizations/Lean && lake env lean --version && lake env lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0834/IntakeProbe.lean)` | 0 | seven adjacent coloring interfaces elaborated; complete output SHA-256 `dec3dd9d2ce185193f252f1477a619ebc5f45438c5a3a60ffd43996067107ef2` |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0834/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0834/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H1/M4/R4 boundary, null target, inventory, source hashes, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0834/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0834 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- No independently approved immutable primary source, pinpoint statement, definition and assumption
  map, complete proof boundary, correction or errata audit, modern map-to-graph transport, or H0
  review exists.
- Finite versus locally finite scope, simple graph versus plane map, supplied versus existential
  embedding, plane versus sphere, vertex versus region coloring, at-most-five semantics, ordered
  binders, and degenerate cases remain open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  alternate encoding, or required statement mutation is frozen. Pinned mathlib supplies ordinary
  coloring substrate but no located graph-planarity or five-color declaration.
- Formal anchor and provenance audit, discovery and obligation freezes, typed graphs, proof,
  composition, trust closure, readable reconstruction, hermetic replay, deterministic bundle,
  independent release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake. Only the integration lane may accept the
provisional worker receipt.
