# Intake validation

Base revision: `10064cd912bf0d94ab6c8d818dd3a30551a921cd` (tree
`f7483f57d60b00edad176cef2fa658a87622982d`). Validation ran on 2026-07-13 in the isolated worker
clone (Asia/Shanghai).

Validation is limited to target-set consistency, the planned dossier and scope invariants,
repository-source provenance, source-family discrimination, pinned environment identity, a narrow
Lean API probe, a bounded local exact-topic search, JSON integrity, proof-escape hygiene, and
whitespace. The catalog does not select one proposition, so no canonical target, expression hash,
statement mutation, accepted source, or proof is claimed.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

## Environment

- Linux `7.0.0-27-generic`, x86_64; timezone Asia/Shanghai.
- Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1368` | 0 | rank 978, planned, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 9971,9976 -- Docs/researches/math_theorems.md` and duplicate-line blame | 0 | all twelve uncited catalog lines originate at commit `bcf3f9fa...b74f` |
| Crossref inspection of Smale 1961, Palis 1969, and Palis-Smale 1970 metadata | 0 | distinguished a plausible 1961 gradient source lead, including the catalog's Marston/Stephen first-name discrepancy, from later Morse-Smale/structural-stability results; metadata discovery only, no H0 acceptance |
| fixed Scholarpedia revision `132702` inspection | 0 | distinguished the Morse-Smale definition from the separately attributed Palis-Smale structural-stability theorem; revision wikitext SHA-256 `38215ae4...ff0`; secondary discriminator only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1368/IntakeProbe.lean)` | 0 | nine adjacent pinned ODE, flow, invariant, periodic-point, manifold-integral-curve, and derivative APIs elaborated; output SHA-256 `847485a6...033`; no target declaration |
| `rg -n -i --glob '*.lean' 'Morse.?Smale\|structural(ly)? stable\|structural stability\|MorseSmale' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | expected no-match result; bounded repo-local and pinned-mathlib intake search only |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1368-pycache python3 -m py_compile Stage1_Instances/THM-M-1368/check_intake.py` | 0 | scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1368/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, current source/dependency hashes, null H5/M4/R4 target, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1368/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| prohibited Lean construct scan over the owned path | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null` plus `git diff --check -- Stage1_Instances/THM-M-1368 .stage1-worker-selftest.json` | 0 for whitespace diagnostics | no whitespace errors; no-index exit 1 was only the expected new-file difference |

## Known downstream failures

- No approved canonical root, complete primary-source edition, exact theorem locator,
  definition/assumption/conclusion/proof-boundary/correction mapping, terminology chronology, or
  independent review exists.
- Flow, vector field, and diffeomorphism variants and the definition, structural-stability,
  gradient-genericity, Morse-theoretic, and surface-characterization conclusions have materially
  different contracts; the catalog selects none.
- No canonical Lean expression, exact minimal imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation test exists.
- The generic pinned APIs are adjacent substrate only. Exhaustive anchor audit, discovery protocol,
  obligation registry, typed graphs, proof, composition, trust closure, readable reconstruction,
  hermetic replay, deterministic bundle, independent verification, and master acceptance are open.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity and open task DAG.
Only the integration lane may accept the provisional worker receipt.
