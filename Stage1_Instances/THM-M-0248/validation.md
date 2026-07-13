# Intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978`; base tree:
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`.

Validation ran on 2026-07-13 (Asia/Shanghai) in the isolated worker clone. It covers target
membership, the planned dossier and open task DAG, repository-source provenance, inspected source
metadata and Theorem 4 discovery copy, JSON and scoped invariants, a narrow pinned Lean substrate
probe, a bounded local formal search, prohibited-construct hygiene, and whitespace. It does not
validate a canonical theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source boundary

The catalog record was traced to its uncited introduction commit. Bishop's 1959 Bulletin paper was
inspected at Theorems 1 and 4, and Crossref metadata confirms its title, author, venue, year, volume,
issue, pages, and DOI. Theorem 4 closely matches the catalog gloss. The intake nevertheless leaves
the canonical claim null because the catalog does not cite the paper or select one equivalence,
the inspected paper announces rather than supplies the full proof, OCR-sensitive definitions need
exact transcription, and no correction, errata, dependency, or independent source review passed.

## Environment fingerprint

- Platform: Linux `7.0.0-27-generic`, x86_64, Asia/Shanghai.
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
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0248` | 0 | rank 1258; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 1787,1792 -- Docs/researches/math_theorems.md` | 0 | all six uncited source-record lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref query for DOI `10.1090/S0002-9904-1959-10283-4` | 0 | Bishop, *Some theorems concerning function algebras*, Bulletin AMS 65(2), 1959, pages 77-78; response SHA-256 `3ae6b23f...d4d8e` |
| `pdfinfo`, `pdftotext -layout`, and line inspection of the lawful discovery copy | 0 | two-page source inspected at Theorems 1 and 4; PDF SHA-256 `2f659092...853ef`; no full-proof or H0 credit |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0248/IntakeProbe.lean)` | 0 | seven adjacent complex, compactness, continuous-map, separating-algebra, and Stone-Weierstrass interfaces elaborated; complete output SHA-256 `2dc99e44...3272`; no target theorem declared |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 0 only for unrelated phrase matches | no Bishop rational-approximation or controlled-pole terminal declaration; unrelated uses of "minimal boundary" carry no credit |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts parse after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0248/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0248/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M4/R4 boundary, source hashes, null formal target, exact inventory, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0248/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0248 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- No independently approved exact source identity, definition chain, proof body or dependency,
  correction and errata audit, source-to-node mapping, or H0 review exists.
- The rational-function and pole model, uniform closure, minimal boundary, real-part algebra, peak
  set, planar measure, selected equivalence, binders, and boundary cases remain open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  alternate encoding, or required statement mutation is frozen.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to preserve the source scope
and open work. Only the integration lane may accept the provisional receipt.
