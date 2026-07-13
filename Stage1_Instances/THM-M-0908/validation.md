# Intake validation

Base revision: `39704171d88ffcdc33a47365ae9791f855fa3a44`; base tree:
`050ab5c6392560337051d2eadd1b82277dbe1c4f`.

This validation covers target membership, the planned dossier and open task DAG, catalog
provenance, bibliographic family identification, scope and source boundaries, JSON and scoped
invariants, a narrow pinned Lean coloring probe, prohibited-construct hygiene, and whitespace. It
does not validate a canonical theorem statement or proof because the source does not freeze the
graph, planarity, and list-coloring encoding.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source boundary

Crossref and DOI metadata identify C. Thomassen, *Every Planar Graph Is 5-Choosable*, *Journal of
Combinatorial Theory, Series B* 62(1) (1994), 180-181, DOI
`10.1006/jctb.1994.1062`. Unpaywall reported no open-access or repository copy. Secondary arXiv
abstracts identify the conventional family and the at-least-five list convention. This run did not
admit an immutable primary text or inspect its pinpoint theorem, incorporated definitions, proof
boundary, corrections, or errata. Exact scope and transport to a modern Lean proposition also lack
independent review, so the source classification remains H1 rather than H0.

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
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0908` | 0 | rank 1450; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6642,6647 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| read-only Crossref and Unpaywall API inspection for DOI `10.1006/jctb.1994.1062` | 0 | bibliographic identity confirmed; no OA/repository copy; normalized metadata SHA-256 values recorded in `instance.json` |
| read-only arXiv API inspection of `1103.1801v1` and `1005.5194v3` | 0 | secondary abstracts identify the family; the former defines at-least-`k` choosability; feed hashes recorded |
| read-only immutable raw-source inspection of `bsniegowski/lean-planar-graphs` at `4d560bc5ec87c763d2042b9e7a5dcfc67b6e6c3d` | 0 | syntactic `PlanarGraph.fiveListColorable` lead is placeholder-backed, narrower, and on Lean 4.30.0-rc2; blocked with no proof credit |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 0 | only the ordinary Coloring module's planar-graph TODO and unrelated prose matched; no obvious list-coloring, choosability, planarity, or Thomassen declaration |
| `(cd Formalizations/Lean && lake env lean --version && lake env lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0908/IntakeProbe.lean)` | 0 | eight adjacent coloring interfaces elaborated; complete output SHA-256 `0852835123f503927196ecd4ebe73804ba4a22403f17e67d8f0ebe4b20417051` |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0908/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0908/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H1/M4/R4 boundary, null target, inventory, source hashes, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0908/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0908 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- No independently approved immutable primary source, pinpoint statement, definition and assumption
  map, complete proof boundary, correction or errata audit, modern graph/list-coloring transport, or
  H0 review exists.
- Finite versus locally finite scope, simple graph versus supplied plane map, existential versus
  supplied embedding, exactly-five versus at-least-five lists, representation, color carrier,
  disconnected graphs, ordered binders, and degenerate cases remain open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked alternate
  encoding, or required statement mutation is frozen. Pinned mathlib supplies only ordinary coloring;
  the external candidate is placeholder-backed, narrower, and toolchain-incompatible.
- Formal anchor and provenance audit, discovery and obligation freezes, typed graphs, proof,
  composition, trust closure, readable reconstruction, hermetic replay, deterministic bundle,
  independent release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake. Only the integration lane may accept the
provisional worker receipt.
