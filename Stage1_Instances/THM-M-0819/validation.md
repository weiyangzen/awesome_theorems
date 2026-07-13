# Intake validation

Base revision: `902d9ce008e88a35a2307c85355560a230cc33c2`; base tree:
`dfc20d8141f18f6b09a03e818acfff408e836714`.

This validation covers target membership, the planned dossier and open task DAG, catalog
provenance, the inspected primary-statement preview, JSON and scoped invariants, a narrow pinned
Lean API probe, the truthful failure boundary of an immutable external Lean candidate, prohibited
construct hygiene, and whitespace. It does not validate a canonical theorem statement or proof.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The external candidate was downloaded to `/tmp` and checked there;
generated temporary Lean outputs were removed. The owned intake files and root worker packet make
the final tree dirty and nonrelease.

The provisional receipt binds the root packet and every non-receipt owned input by SHA-256, records
the empty tracked patch and pre-existing `.lake` symlink boundary, and carries recipe-bound structure
and Lean-probe actions. It is unsigned, non-content-addressed, unsupported for release, and due for
integration review before any dependent statement work.

## Source boundary

The publisher preview of Dilworth's 1950 paper, exposed through the 1990 reprint DOI
`10.1007/978-1-4899-3558-8_1`, was inspected at PDF SHA-256
`6af3f64b82c9788779586fbc43d8fa845b24c3ff8f34414c5518aa3545b78243`.
Original page 161 provides the definitions and exact Theorem 1.1; page 162 begins the finite proof.
The preview does not contain original pages 163-166. Full proof and transfinite-argument review,
correction status, modern equality transport, and independent review remain open, preventing H0.

Pinned mathlib's curated `docs/1000.yaml` points to a Lean 4 formalization at immutable commit
`f82f920f05a381bb1ce5e8903bde33e27f4365b6`. Its source has no textual proof escape, but the direct
current-pin check exited 1 at source lines 397, 404, and 597; Lean's error recovery caused the
terminal declarations to report `sorryAx`. This is recorded as M5, not converted to proof credit.

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
| `python3 scripts/stage1_target.py show THM-M-0819` | 0 | rank 1377; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6019,6024 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 60 -sS https://page-one.springer.com/pdf/preview/10.1007/978-1-4899-3558-8_1 -o /tmp/dilworth-primary-preview.pdf` | 0 | two-page, 442264-byte publisher preview; SHA-256 recorded above |
| `pdftotext -layout /tmp/dilworth-primary-preview.pdf /tmp/dilworth-primary-preview.txt` and inspection | 0 | original pages 161-162 crosswalked; extracted-text SHA-256 `c05889cda31f656611c864b8f0f1273bea1b5f0e5999c055ad3b304cbc8e3157` |
| Crossref metadata query for DOI `10.2307/1969503` | 0 | author, title, journal, volume, issue, year, and first page corroborated; metadata received no source-proof credit |
| `curl -L --fail --max-time 60 -sS https://arxiv.org/pdf/1703.06133 -o /tmp/dilworth-coq.pdf` | 0 | 12-page secondary Coq-formalization paper; SHA-256 `037feec9c90034a475c9d296c7d511ffc50249fa765f6421abe1b81d480be646` |
| immutable source and lock inspection of `vlad902/misc-lean-proofs@f82f920f05a381bb1ce5e8903bde33e27f4365b6` | 0 | candidate source SHA-256 `4bc86897588087f472b358830bba157b92994e2b0dd44c66805f57c29211c985`; original Lean v4.28.0-rc1 and mathlib `3234d21e...`; no textual proof escape |
| `(cd Formalizations/Lean && lake env lean /tmp/Dilworth-f82f-check.lean)` | 1, expected blocker | errors at source lines 397, 404, and 597; recovered declarations report `sorryAx`; output SHA-256 `01a36fd460bb5ef6f3761d026e1846e39755b9b8ec06f00b52a5bf76abd3d56e` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| bounded exact-topic `rg` over pinned mathlib and repo-local Lean | 1 for exact implementation names | no pinned `Dilworth`, `antichainWidth`, `IsChainPartition`, or `minChainPartition` declaration; curated YAML locator and adjacent APIs only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0819/IntakeProbe.lean)` | 0 | eight adjacent order, chain-height, and cardinality APIs elaborated; stdout SHA-256 `adacf11317077ad5c3413827d68c50565055f62db00b183948660e4038a6ee00` |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0819/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0819/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H1/M5/R3 boundary, null target, receipt governance, action hashes, inventory, source hashes, candidate blocker, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0819/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0819 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- The catalog omits the equality comparator and does not select primary finite-width or modern
  finite-poset scope. Domain, cover, partition, width, cardinality, binder, and boundary conventions
  remain open.
- The primary preview is pinpointed and hashed, but the full proof, transfinite argument, correction
  or errata status, complete mapping, exact modern transport, and independent review are open.
- The external Lean candidate fails under the repository pin and is not in the validation closure.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen.
- Formal anchor and provenance audit, discovery and obligation freezes, typed graphs, proof,
  composition, trust closure, readable reconstruction, hermetic replay, deterministic bundle,
  independent release verification, and master acceptance remain open.

The provisional readability classification is `R3`: this dossier is a useful labeled source, scope,
and blocker report, but it is not a proof reconstruction.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake. Only the integration lane may accept the
provisional worker receipt.
