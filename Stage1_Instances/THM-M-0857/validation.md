# Intake validation

Base revision: `561d83df037004ceb2259292d7c63be930b40391`; base tree:
`6eb02475bf5a70139d60615c924b31c930efc2bb`.

This validation covers target membership, the planned dossier and open task DAG, catalog
provenance, the inspected primary-source route, JSON and scoped invariants, a narrow pinned Lean API
probe, prohibited-construct hygiene, and whitespace. It does not validate a canonical theorem
statement or proof because the catalog leaves material graph-model and scope choices unresolved.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned files and worker packet make the final tree dirty and
nonrelease.

## Source boundary

The CC0 Zenodo copy of Julius Petersen, *Die Theorie der regulären graphs*, *Acta Mathematica* 15
(1891), 193-220, DOI `10.1007/BF02392606`, was inspected at PDF SHA-256
`8762abd5e2f1fb3edcd1917b4db3b0c213a75d4ecfe026829b58e2e7913cca8c`. Printed pages 194, 210,
and 218-219 establish the multigraph convention, bridge-separated-leaf vocabulary, primitive
cubic result, and degree-two plus degree-one factor route. Translation, complete assumptions and
proof mapping, errata, the modern simple-graph specialization, and independent review remain open,
so the source status is H1.

The observed Zenodo API response had SHA-256
`8e99a06f50f15d3098022bb4a669c5d97c21652a2f2c903d0e0ff0b7cdb926bc`; the Crossref response had
SHA-256 `a20f0b9d6c57bfaeb624fff7360ccd6ee4368e5bc56f026d651553982a88c5ae`.
These temporary discovery inputs are not a durable archive or release bundle.

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

All commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different `cwd` is
shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0857` | 0 | rank 1411; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6285,6290 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail -sS https://zenodo.org/api/records/2304433 -o /tmp/petersen-zenodo.json` | 0 | 3925-byte metadata response; CC0; one 2,288,748-byte `article.pdf`; SHA-256 recorded above |
| `curl -L --fail -sS https://zenodo.org/api/records/2304433/files/article.pdf/content -o /tmp/petersen-zenodo.pdf` | 0 | 29-page, 2,288,748-byte PDF; SHA-256 recorded above |
| `pdftotext -layout` and passage inspection of the primary PDF | 0 | printed pages 194, 210, and 218-219 provide the recorded historical route |
| `curl -L --fail -sS https://api.crossref.org/works/10.1007/BF02392606 -o /tmp/petersen-crossref.json` | 0 | 2029-byte bibliographic response; volume 15, pages 193-220, 1891; SHA-256 recorded above |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree shown above; package worktree clean |
| bounded `rg` search of repo-local and pinned mathlib Lean sources | 0 aggregate | no Petersen/bridgeless/cubic-perfect-matching closure found; this is not an exhaustive absence claim |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0857/IntakeProbe.lean)` | 0 | ten graph interfaces elaborated; complete output SHA-256 `6eb4c3680897ad6b9603200c7697c9b085b4c8fdd70c974d407d1ba63af6dd81`; no target or proof credit |
| `python3 -m json.tool` on structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all JSON parsed after finalization |
| Python `ast.parse` on `check_intake.py` | 0 | scoped validator parsed without bytecode output |
| `python3 -B Stage1_Instances/THM-M-0857/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H1/M3/R4 boundary, null target, source hashes, inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0857/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` and `git diff --check` | 0 aggregate | no whitespace diagnostics; expected no-index new-file differences ignored |

## Known downstream failures

- An independent reviewer must verify the German terminology, translation, assumptions, complete
  proof mapping, correction history, and bridge-free specialization.
- The canonical graph model, finiteness, connectedness, degree semantics, bridge quantifier,
  perfect-matching encoding, ordered binders, and boundary cases are not frozen.
- No canonical Lean expression, minimal imports, expression/environment fingerprint, checked
  transport, or required statement mutation is frozen.
- No exact Petersen proof declaration was located. Tutte and the core graph predicates are formal
  substrate only; their terminal provenance and trust are not an exact-root audit.
- Discovery and obligation freezes, typed graphs, proof, composition, readable reconstruction,
  hermetic replay, deterministic bundle, independent verification, release, and master acceptance
  remain open.

These failures block statement and theorem completion but do not invalidate a truthful,
self-tested `planned` intake. Only the integration lane may accept the provisional worker receipt.
