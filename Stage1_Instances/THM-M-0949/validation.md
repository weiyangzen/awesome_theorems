# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, a published exact statement/proof lead, JSON and scoped invariants, a narrow pinned Lean
interface and candidate-shape probe, bounded repo-local discovery, prohibited-construct hygiene,
and whitespace. It does not validate a canonical statement or proof. Source adoption, full mapping,
independent review, and the statement gate remain downstream.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The published Annals PDF for D. H. J. Polymath's *A new proof of the density Hales-Jewett theorem*
was inspected temporarily. Theorem 1.4 is on printed page 1285, with incorporated definitions on
pages 1283-1285. The observed PDF SHA-256 is
`b7f68cc3e49357ddb836b542519164e9846010d9224dc7d942fe571f4cd9f2df`. The original 1991
Furstenberg-Katznelson article was identified by journal, pages, and DOI but not fully inspected.
A bounded Crossref and publisher-page check exposed no correction relation or erratum for the
Polymath article. That negative observation is not a complete errata audit. No external source was
added to the repository, no source was accepted as `H0`, and independent review remains open.

## Environment fingerprint

- Platform: Linux x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0949` | 0 | rank 1010; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6931,6936 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| temporary download and `pdftotext` inspection of the published Polymath PDF | 0 | exact Theorem 1.4 and incorporated definitions located; observed digest recorded above; source discovery only |
| bounded Crossref and publisher-page correction search | 0 | no correction relation or matching erratum exposed; not a complete errata audit |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0949/IntakeProbe.lean)` | 0 | line, properness, monochromaticity, ordinary Hales-Jewett, finite density, and the candidate proposition shape elaborated; no target theorem was declared |
| bounded `rg` search for `density Hales-Jewett` or `DHJ` in pinned mathlib and repo-local Lean | 1 (expected no match) | no exact density-theorem declaration found; intake discovery only, not an exhaustive anchor audit |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0949/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0949/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M3/R4 boundary, null canonical target, source pins, exact inventory, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0949/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0949 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- The repository does not cite or adopt the inspected restatement; original-source inspection,
  complete incorporated-definition/premise/proof/errata mapping, and independent review are open.
- Alphabet, word and set representation, density codomain and casts, threshold convention, binder
  order, combinatorial-line containment, alternate transports, and every boundary case remain open.
- No canonical Lean expression, minimal-import decision, normalized expression/environment
  fingerprint, checked alternate encoding, or four-class statement mutation is frozen.
- The pinned ordinary Hales-Jewett proof is not a density theorem. The candidate shape definition
  is neither a theorem nor proof evidence, and exhaustive formal-candidate provenance remains open.
- Discovery and obligation freezes, typed graphs, proof, composition, trust closure, readable
  reconstruction, hermetic replay, deterministic bundle, independent release verification, and
  master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose role is to freeze the scope boundary and
open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
