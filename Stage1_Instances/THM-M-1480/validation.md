# THM-M-1480 intake validation

Base revision: `fc0de001c634823043636f9380a991c027e42533` (tree
`b2e4d058036a1e9ec56bfc6aa5de3b015efe6330`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation covers target-set consistency, the fail-closed planned dossier, source-statement and
non-substitution boundaries, the six-node open task DAG, structured intake invariants, and a narrow
pinned Lean API probe. It does not validate a canonical quasi-Monte Carlo proposition or proof: the
catalog provides a topic gloss rather than a source-selected truth-valued statement. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only. No dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1480` | 0 | rank 1157; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree match this record |
| `git blame -L 10798,10803 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref work lookup for DOI `10.1090/S0002-9904-1978-14532-7` | 0 | deterministic metadata projection confirmed Niederreiter's 1978 *Bulletin AMS* survey, volume 84 issue 6, pages 957-1041; discovery only, no source proposition admitted |
| AMS DOI/article/full-text request | 403 | access blocker recorded; no article body, theorem passage, definition, proof, or correction was admitted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| bounded case-insensitive exact-topic search over repo-local Lean and pinned mathlib | 1 | expected no-match: no quasi-Monte-Carlo, low-discrepancy, star-discrepancy, Koksma-Hlawka, or equidistributed-sequence integration declaration; intake discovery only |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1480/IntakeProbe.lean)` | 0 | seven adjacent APIs elaborated; stdout SHA-256 `4c37116a63ff938ed6d13c5a4c6be16e139c4c5517d799e6c14667cfc0066c8c`; representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem |
| `python3 -m json.tool` on all JSON artifacts and the worker packet | 0 after finalization | valid JSON objects |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1480-pycache python3 -m py_compile Stage1_Instances/THM-M-1480/check_intake.py` | 0 | scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1480/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 after finalization | target/DAG identity, null target, H5/M4/R4 boundary, pins, inventory, receipt/packet, and six open tasks agree |
| prohibited-declaration scan of `IntakeProbe.lean` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped final-newline, LF, NUL, trailing-whitespace, no-index diff, and `git diff --check` checks | 0 | no diagnostics |

## Known open gates

An accountable correction must select and independently review one immutable exact proposition.
The point-set or sequence model, dimension, domain and measure, discrepancy definition, integrand
and variation/regularity class, quadrature estimator, hypotheses, conclusion, constants, rates,
quantifier order, arithmetic boundary, corrections, and degenerate cases remain open. So do the
canonical Lean expression and environment fingerprint, checked transports, statement mutations,
exhaustive formal anchor audit, discovery protocol, obligation registry, typed graphs, proof and
composition, trust and provenance closure, readable reconstruction, hermetic replay, deterministic
bundle, independent verification, master acceptance, audit completion, and theorem completion.

These open gates block ordinary theorem-proof execution but do not invalidate a truthful,
self-tested `planned` intake whose purpose is to freeze the ambiguity and dependent work. Only the
integration lane can accept the provisional node receipt.
