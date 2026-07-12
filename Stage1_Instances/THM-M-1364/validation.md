# Intake validation

Base revision: `10064cd912bf0d94ab6c8d818dd3a30551a921cd`; base tree:
`f7483f57d60b00edad176cef2fa658a87622982d`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, bibliographic discrimination, JSON and scoped invariants, a narrow pinned Lean substrate
probe, bounded repository/mathlib discovery, prohibited-construct hygiene, and whitespace. It does
not validate a canonical Lorenz-system theorem or proof because the catalog does not identify one.
The structured recipes record denied-network replay policies; this inherited worker environment was
not independently network-sandboxed and is explicitly nonhermetic evidence.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

Crossref metadata for DOI `10.1175/1520-0469(1963)020<0130:DNF>2.0.CO;2` confirms Edward N.
Lorenz's *Deterministic Nonperiodic Flow*, **Journal of the Atmospheric Sciences** 20(2), 130-141
(1963). The captured response has SHA-256
`4972bd7d07af8983340449f8e11d24a8d1d86b162ac4bd68787f1eabba3846d0`.
This is a strong bibliographic match to the catalog attribution and date, but it does not select one
equation, observation, or theorem. Publisher full text was not available in this run, and no exact
source, proof or experiment boundary, correction, erratum, or independent review is claimed.

## Environment

- Linux `7.0.0-27-generic`, `x86_64`; timezone `Asia/Shanghai`.
- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1364` | 0 | rank 974; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 9943,9948 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref API query for the encoded Lorenz DOI; `jq` metadata inspection; `sha256sum` | 0 | title, Edward N. Lorenz, journal, volume 20, issue 2, pages 130-141, year 1963, and DOI confirmed; discovery response hash recorded above |
| publisher PDF retrieval | 22 | HTTP 403; no full-text inspection or source admission claimed |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above; no dependency-mutating operation run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | pinned hashes recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1364/IntakeProbe.lean)` | 0 | ten adjacent generic APIs elaborated; complete output SHA-256 `fcd83261...f61c`; no target theorem declared |
| `rg -n -i --glob '*.lean' '\bLorenz (system\|equations?\|attractor\|flow)\b\|geometric[ _-]*Lorenz\|strange[ _-]*attractor\|deterministic[ _-]*nonperiodic' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 (expected no match) | no exact-topic Lean declaration; bounded intake discovery only, not an exhaustive external audit |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1364-pycache python3 -m py_compile Stage1_Instances/THM-M-1364/check_intake.py` | 0 | scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1364/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, input pins, null target, H5/M4/R4 boundary, exact artifact inventory, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1364/check_intake.py` | 0 | public replay mode passed without the scheduler-only packet |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 per new file means only that content differs from `/dev/null` |
| `git diff --check -- Stage1_Instances/THM-M-1364 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; per-file no-index checks cover untracked files |

## Status boundary

Known downstream failures remain deliberately open: accountable target/source selection; immutable
full source and independent review; exact equations/model, parameters, solution semantics, invariant
set, chaos or attractor predicate, conclusion, computation and certificate boundary, and degenerate
cases; canonical Lean elaboration, expression and environment fingerprints, checked transports, and
statement mutations; immutable anchor audit; discovery and obligation freezes; proof and
composition; hermetic replay; deterministic evidence bundling; independent release verification;
and master acceptance. These block ordinary theorem execution and completion but do not invalidate
a truthful, self-tested `planned` intake.
