# Intake validation

Base revision: `902d9ce008e88a35a2307c85355560a230cc33c2`; base tree:
`dfc20d8141f18f6b09a03e818acfff408e836714`.

Validation ran on 2026-07-13 (Asia/Shanghai) in the isolated worker clone. It covers target
membership, the planned dossier and open task DAG, repository-source provenance, primary-source
discovery boundaries, JSON and scoped invariants, a narrow pinned Lean substrate probe, a bounded
local formal search, prohibited-construct hygiene, and whitespace. It does not validate a canonical
Kruskal theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source boundary

The catalog record was traced to its uncited introduction commit. Crossref confirms the
bibliographic identity of Kruskal's 1956 paper, and an official three-page discovery copy was
inspected at the finite connected positive distinct-weight assumptions, Construction A, and the
exchange proof. The intake nevertheless leaves the canonical claim null because the catalog does
not cite the paper or select construction correctness versus uniqueness or another bundled result,
and no complete definition, tie-policy, correction, errata, or independent-review gate passed.

## Environment fingerprint

- Platform: Linux x86_64, Asia/Shanghai.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran from the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0823` | 0 | rank 1381; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6047,6052 -- Docs/researches/math_theorems.md` | 0 | all six uncited source-record lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref query for DOI `10.1090/S0002-9939-1956-0078686-7` | 0 | Kruskal, paper title, Proceedings AMS 7(1), February 1956, pages 48-50; response SHA-256 `ed5d69a...45687` |
| official paper discovery-copy inspection | 0 | three pages inspected at assumptions, Problem 1, Construction A, and the exchange proof; PDF SHA-256 `b77f9dc0...70bd5`; discovery only; the unfrozen catalog root remains H5 |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0823/IntakeProbe.lean)` | 0 | six adjacent forest, tree, spanning-subgraph, edge-set, and spanning-tree-existence interfaces elaborated; no target theorem declared |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 0 only for unrelated surname matches | no weighted minimum-spanning-tree or Kruskal-algorithm declaration; the matches are Kruskal-Katona material |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts parse after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0823/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0823/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H5/M4/R4 boundary, source hashes, null formal target, exact inventory, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0823/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0823 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- No independently approved exact source identity, proposition, definition chain, proof and assumption
  crosswalk, correction and errata audit, or H0 review exists.
- Graph and edge representation, weight codomain, positivity or distinctness, tie policy, algorithm
  transition and termination, output contract, objective, uniqueness, binders, and boundary cases remain open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked alternate
  encoding, or required statement mutation is frozen.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust closure,
  readable reconstruction, hermetic replay, deterministic bundle, independent release verification,
  and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to preserve the source scope
and open work. Only the integration lane may accept the provisional receipt.
