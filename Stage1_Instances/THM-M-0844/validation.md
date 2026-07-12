# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

This validation covers target membership, the planned dossier and open task DAG, catalog
provenance, bibliographic disambiguation, JSON and scoped invariants, a narrow pinned Lean substrate
probe, a bounded repo-local and mathlib search, prohibited-construct hygiene, and whitespace. It
does not validate a canonical theorem statement or proof because the catalog supplies no stable
truth-valued proposition.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

Crossref and DBLP metadata establish the leading three-author 2007 candidate as *Efficient Testing
of Bipartite Graphs for Forbidden Induced Subgraphs*, SIAM Journal on Computing 37(3), 959-976,
DOI `10.1137/050627915`. Unpaywall reported no open or repository copy, and the author-copy lead
returned by Semantic Scholar was unavailable during the bounded run. The primary theorem text was
therefore not inspected and no H0 admission is claimed.

Fox-Pach-Suk arXiv `1710.03745v1` was inspected as a later source-family discriminator. It cites the
2007 paper and attributes to it a polynomial-size ultra-strong regularity result for bipartite
graphs of bounded VC-dimension. The observed PDF SHA-256 is
`a79fc0300c2669ecc5df444283b5cfd25b40317f521e41ddce961ac5bbfb7a25`.
Its paraphrase is not substituted for the missing primary statement. The four-author testability
characterization and the two-author Fischer-Newman estimation theorem were separately identified
as confusable but nonidentical results.

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

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0844` | 0 | rank 1033; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6194,6199 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git rev-parse bcf3f9fa79ab8c2b6610c9875668c2589b35b74f:Docs/researches/math_theorems.md` | 0 | source-record blob `5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf` |
| Crossref, DBLP, Semantic Scholar, and Unpaywall metadata queries for DOI `10.1137/050627915` | 0 | three-author 2007 bibliographic identity confirmed; no primary theorem text admitted |
| `curl -L --max-time 30 -sS https://export.arxiv.org/pdf/1710.03745` plus `pdftotext` | 0 | later bounded-VC regularity attribution inspected; PDF SHA-256 recorded above; secondary discriminator only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0844/IntakeProbe.lean)` | 0 | eight adjacent VC, bipartite-graph, density, partition, uniformity, and ordinary-regularity APIs elaborated; complete output SHA-256 `28739e9f581ad4ca91839f2259050894c2f657fe93ffd853e8c683936355ce43` |
| `rg -n -i --glob '*.lean' 'Alon.?Fischer.?Newman\|forbidden induced.*bipartite\|bipartite.*forbidden induced\|graph propert(y\|ies).*test\|testable graph' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 (expected no match) | no Alon-Fischer-Newman, forbidden-induced bipartite testing, or testable-graph declaration; intake discovery only |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0844/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0844/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H5/M4/R4 boundary, null formal target, exact inventory, worker packet, source hashes, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0844/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0844 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- The eponym and gloss do not select one truth-valued proposition. No repository-selected primary
  source, theorem number, incorporated definitions, exact proof boundary, errata audit, or
  independent review exists.
- The leading 2007 paper, its bounded-VC regularity result, its forbidden-induced-subgraph testing
  results, the four-author characterization, and the Fischer-Newman estimation theorem are not
  interchangeable. The catalog's intended result remains unresolved.
- Graph/two-sorted encoding, VC convention, partition and homogeneity/regularity definition,
  tester and edit-distance model, probability/query complexity, parameter dependence, quantifier
  order, exact conclusion, and boundary cases remain open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze ambiguity and open
the downstream DAG. Only the integration lane may accept the provisional worker receipt.
