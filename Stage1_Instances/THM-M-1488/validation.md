# THM-M-1488 intake validation

Base revision: `9e2ab501f9bd297b7bda1d222aec4e6f2029019a` (tree
`eab3198df44944dd50b95951243c5f9d3922a703`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation covers target-set consistency, the fail-closed planned dossier, source-statement and
non-substitution boundaries, the six-node open task DAG, structured intake invariants, and a narrow
pinned Lean API probe. It does not validate a canonical recurrent-neural-network proposition or
proof: the catalog provides an architecture/application gloss rather than a source-selected
truth-valued statement. The automation-provided canonical `.lake` symlink was pre-existing and
used read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was performed.
This dirty worker run is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean before and after
  the probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1488` | 0 | rank 1165; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree match this record |
| `git blame -L 10875,10880 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref work lookup for DOI `10.1207/s15516709cog1402_1` | 0 | deterministic metadata projection SHA-256 `c0d930f9c225c149628918ccab9719dddb57a23caaa993bbb2482beb3e9947c4`; Elman, *Finding Structure in Time*, *Cognitive Science* 14(2), 179-211 (1990); discovery only, no source proposition admitted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` before and after probe | 0 | empty output |
| bounded case-insensitive RNN/neural-network search over repo-local Lean and pinned mathlib | 0 | one match, only an incidental tensor documentation sentence in `Mathlib.Data.Holor`; no recurrent-network target declaration; intake discovery only |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1488/IntakeProbe.lean)` | 0 | eight adjacent APIs elaborated; stdout plus stderr SHA-256 `cee02e9e6f17c7b41b02c04dbba998bf58754fd6a0046d54ebc128a5c3f03a5d`; representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem |
| `python3 -m json.tool` on all JSON artifacts and the worker packet | 0 after finalization | valid JSON objects |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1488-pycache python3 -m py_compile Stage1_Instances/THM-M-1488/check_intake.py` | 0 | scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1488/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 after finalization | authorities, target/DAG identity, null target, H5/M4/R4 boundary, pins, artifact hashes, receipt/packet, and six open tasks agree |
| prohibited-declaration scan of `IntakeProbe.lean` | 1 | expected no-match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check`, plus `git diff --no-index --check /dev/null <file>` for every new file | 0 for tracked-diff check; 1 expected per no-index content diff | no whitespace diagnostics; no-index exit 1 means the new file differs from `/dev/null`, not that whitespace validation failed |

## Known open gates

An accountable correction must select and independently review one immutable exact proposition.
The recurrence and architecture, time/sequence carrier and horizon, state/input/output spaces,
parameters and sharing rule, activation and gates, initial state, task or target functional, loss,
training model, hypotheses, conclusion, constants, rates, quantifier order, arithmetic boundary,
corrections, and degenerate cases remain open. So do the canonical Lean expression and environment
fingerprint, checked transports, statement mutations, exhaustive formal anchor audit, discovery
protocol, obligation registry, typed graphs, proof and composition, trust and provenance closure,
readable reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion.

These open gates block ordinary theorem-proof execution but do not invalidate a truthful,
self-tested `planned` intake whose purpose is to freeze the ambiguity and dependent work. Only the
integration lane can accept the provisional node receipt.
