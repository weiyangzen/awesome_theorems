# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, bibliographic source-family discrimination, JSON and scoped invariants, a narrow pinned
Lean substrate probe, a bounded repo-local and mathlib search, prohibited-construct hygiene, and
whitespace. It does not validate a canonical theorem statement or proof because the catalog does
not supply one binder-complete proposition.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

Crossref and DBLP live bibliographic metadata identify the exact-match 1994 article by Morgenstern,
its title, journal, volume, issue, pages, DOI, and PII. The title distinguishes a likely theorem
family involving `(q + 1)`-regular graphs for every prime power `q` and explicit constructions. It
does not expose or authenticate every numbered theorem, definition, hypothesis, construction
branch, exception, or proof boundary. The live metadata responses were not preserved as immutable
theorem-text evidence. No source admission, complete crosswalk, errata review, or independent H0
review is claimed.

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
| `python3 scripts/stage1_target.py show THM-M-0885` | 0 | rank 1036; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6481,6486 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git rev-parse bcf3f9fa79ab8c2b6610c9875668c2589b35b74f:Docs/researches/math_theorems.md` | 0 | source-record blob `5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf` |
| Crossref works query for DOI `10.1006/jctb.1994.1054` | 0 | live metadata identified the exact article title, author, venue, issue, pages, date, DOI, and PII; discovery only |
| DBLP record query for `journals/jct/Morgenstern94` | 0 | live metadata independently agreed on the bibliographic identity; discovery only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0885/IntakeProbe.lean)` | 0 | eight adjacent graph, regularity, adjacency-matrix, Hermitian-spectrum, and square-root APIs elaborated; complete output SHA-256 `338dc5b58bca6fa8b32a5e7bca7bc571b5f33033b8486a444857c78a05af24cd` |
| `rg -n -i --glob '*.lean' 'morgenstern\|ramanujan[ _-]?graph' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 (expected no match) | no exact-topic occurrence; intake discovery only, not an exhaustive anchor audit or global absence claim |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0885/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0885/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M4/R4 boundary, null target, source and neighbor boundaries, exact inventory, worker packet, source hashes, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0885/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0885 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- The catalog gloss does not select one binder-complete proposition. The exact-match article is
  identified bibliographically, but no immutable theorem-text edition, pinpoint theorem,
  incorporated definitions, assumptions, proof boundary, errata disposition, or independent
  source review is admitted.
- The prime-power representation, family and explicitness quantifiers, graph category, regularity,
  connectedness, bipartiteness, trivial spectrum, spectral bound, construction data, exceptions,
  quantifier order, exact conclusion, and boundary cases remain open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the source boundary
and open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
