# Intake validation

Base revision: `fcabbf1e0ad9507eebe91663bccabfa87d22813e`; base tree:
`873e589c594454b7f263c7ed2342089a4d15e842`.

This validation covers target membership, the planned dossier and open task DAG, catalog and
neighbor provenance, bibliographic source-family identification, proposition-changing scope,
structured intake invariants, a narrow pinned Lean API probe, prohibited-construct hygiene, and
whitespace. It does not validate a canonical Kim-Vu statement or proof because none is frozen.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned files and root worker packet make the final tree dirty
and nonrelease.

## Source boundary

Crossref metadata for DOI `10.1007/s004930070014` confirmed Kim and Vu's article title, authors,
journal, March 2000 date, volume 20, issue 3, and pages 417-434. The observed JSON response had
SHA-256 `5b6d2a3765bd2bd7bcb8f4b5ddfbbdab942338faad21a5766cef03643b6205d4`.
Springer exposed bibliographic metadata and a formula-stripped abstract, but access control prevented
inspection of the formula-bearing primary theorem. A transient author-hosted PDF endpoint timed
out. The exact theorem number/page, definitions, assumptions, derivative controls, constants,
conclusion, proof boundary, corrections, and errata were therefore not inspected. This supports an
H1 bibliographic/source-family lead with explicit reconstruction debt, not H0.

## Environment fingerprint

- Platform: Linux 7.0.0-27-generic, x86_64.
- Lean: 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0973` | 0 | rank 1507; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 7106,7111 -- Docs/researches/math_theorems.md` | 0 | all six uncited source-record lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref API query for `10.1007/s004930070014` to `/tmp` | 0 | exact bibliographic record identified; response SHA-256 shown above |
| DOI, Springer page, PDF, and author-hosted endpoint checks | mixed | DOI and abstract metadata reachable; publisher returned HTML/access control rather than the formula-bearing PDF; author endpoint timed out; no exact statement credited |
| bounded `rg` over pinned mathlib and repo-local Lean for Kim-Vu and polynomial concentration | 1, expected no match | no relevant declaration located; not a global absence claim |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake identities agree with the fingerprint; no update or build ran |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0973/IntakeProbe.lean)` | 0 | eight generic polynomial/probability APIs elaborated; complete stdout SHA-256 `a048f43a0f87ea112ff2d786dce0c806a60a1afe1838cd9893ed684fdf05fbab`; empty stderr; no target or proof credit |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 after finalization | all JSON parsed |
| Python `ast.parse` on `Stage1_Instances/THM-M-0973/check_intake.py` | 0 | scoped validator parsed without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0973/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 after finalization | authority identity, planned H1/M4/R4 boundary, null target, source and artifact hashes, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0973/check_intake.py` | 0 after finalization | public replay mode passed without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1, expected no match | no prohibited declaration or proof escape occurs in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 per new file was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0973 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; preceding no-index checks covered untracked files |

## Known downstream failures

- An approved immutable primary source must be inspected for the exact numbered theorem,
  definitions, random-variable laws, polynomial and coefficient conditions, derivative controls,
  constants, parameter ranges, conclusion, proof boundary, corrections, and errata, then
  independently reviewed.
- The catalog's first-author string must be formally reconciled with the bibliographic author, and
  the original theorem versus later variants or corollaries must be selected explicitly.
- No canonical Lean expression, minimal imports, expression/environment fingerprint, checked
  alternate transport, or required statement mutation is frozen.
- The pinned APIs are generic substrate, not a Kim-Vu formal artifact; no terminal proof body,
  provenance, axiom/TCB closure, or formal candidate receives credit.
- Discovery and obligation freezes, typed graphs, proof, composition, readable reconstruction,
  hermetic replay, deterministic bundle, independent release verification, and master acceptance
  remain open.

These failures block statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake. Only the integration lane may accept the
provisional worker receipt.
