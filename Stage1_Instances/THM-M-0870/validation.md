# THM-M-0870 intake validation

Item: `S56-M-0870-INTAKE`

Base revision: `748243faadc15828fb087059337fd05b7be9fdeb`

Base tree: `e46d642646f80980838b6f016f5d69b817bd464d`

Validation date: 2026-07-13 (Asia/Shanghai)

## Validated boundary

Validation covers target membership, the fail-closed source and scope discrimination, the planned
nine-file dossier, the exact six-node open downstream DAG, current source and dependency hashes, a
bounded formal search, and a discovery-only pinned Lean API probe. It does not validate an exact
treewidth definition, theorem statement, source crosswalk, proof body, audit completion, or theorem
completion because the catalog supplies no truth-valued proposition.

The initial worker tree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink. It points to the canonical pinned artifacts and was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was run.

## Environment

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision/tree:
  `8a178386ffc0f5fef0b77738bb5449d50efeea95` /
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Mathlib source SHA-256 values: `Acyclic.lean`
  `94a3dad09f48c9a2b1d0dc68914f4060bec2943e2977a7cdf4e2105df7afe50a`, `Maps.lean`
  `60bcb9baa33451ed189091e3254004bf77f9b814a87a6ce9709042c4db6d7d2a`, and `Set/Card.lean`
  `09942e2b66a4dfafd949dc32da33c41d3ada901769fda4ceb1f7e06dc8b0b5f5`.

## Commands and results

All commands ran in this worker clone unless a working directory is stated otherwise.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0870` | 0 | rank 1424; planned; score 86; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before editing | 0 | only pre-existing untracked `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 6376,6381 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref work lookup for DOI `10.1016/0196-6774(86)90023-4` | 0 | confirmed Robertson/Seymour, article title, Journal of Algorithms 7(3), 1986, pages 309-322; response SHA-256 `77028f...8f72`; bibliographic discovery only |
| Elsevier full-text endpoint attempts | nonzero | primary text was not obtained; no theorem locator, definition, proof, or H0 source mapping was claimed |
| bounded case-insensitive `rg` search for treewidth spellings, `TreeDecomp`, `Treewidth`, and graph/tree-decomposition phrases in repo-local and pinned Lean | 1 (expected no match) | no literal target-topic declaration found; adjacent graph/tree/cardinality substrate only; not a complete external absence claim |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions agree with the environment record |
| preliminary `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0870/IntakeProbe.lean` | 1 | rejected the misqualified name `Set.Finite.ncard_eq_toFinset_card`; corrected to the actual public name without adding or substituting a target |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0870/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; axiom reports were `[propext, Quot.sound]` and `[propext, Classical.choice, Quot.sound]`; output SHA-256 `07e698...d27e`; no target or proof credit |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all finalized JSON documents parsed |
| Python `ast.parse` and isolated `py_compile` on `check_intake.py` | 0 | scoped validator parsed and compiled without writing generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0870/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | authority identity, planned H5/M4/R4 boundary, null target, hashes, artifact inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0870/check_intake.py` | 0 | public replay mode passed without the scheduler-only worker packet |
| prohibited declaration/proof-escape scan over `IntakeProbe.lean` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0870 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; per-file checks cover untracked artifacts |

## Known open gates

- The catalog's invariant/decomposition phrase is not a truth-valued proposition. Integration must
  authorize a corrected exact target or redirection after independent primary-source review.
- No authoritative primary text, exact definition or theorem locator, incorporated definitions,
  complete assumption/conclusion/proof-boundary/correction map, or independent review is admitted.
- Graph, tree-index, bag, vertex/edge cover, running-intersection, width/optimum, binder, conclusion,
  and degenerate-case conventions remain open, including the empty graph's `-1` versus `0` width.
- No canonical Lean expression, minimal imports, expression/environment fingerprint, checked
  transport, or removed-hypothesis/domain/binder/boundary mutation is frozen.
- Formal anchor and provenance audit, discovery and obligation freezes, typed graphs, proof,
  composition, trust closure, readable reconstruction, hermetic replay, deterministic evidence
  bundle, independent release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity and
open the downstream DAG. Only the integration lane may accept the provisional worker receipt.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0870-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. H5 applies only to the unstable catalog target, not to
standard treewidth mathematics. No canonical proposition, H0, M0, R0, audit completion, theorem
completion, accepted receipt, or master acceptance is claimed.
