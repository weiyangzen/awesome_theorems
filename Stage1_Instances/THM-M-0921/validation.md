# THM-M-0921 intake validation

Base revision: `46a0f2a3ea74765a0467c489264b838ffbb70675` (tree
`7b1b5269d7da840fd086da731d6f92903c209c35`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and non-substitution boundaries, the
six-node open task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does
not validate a canonical Catalan-number root or package proof because the catalog does not select
one. The automation-provided canonical `.lake` symlink was pre-existing and used read-only; no
dependency update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker
run is nonrelease evidence.

## Source discovery boundary

Richard Stanley's author-hosted *Catalan Addendum*, version of 25 May 2013, was retrieved to a
temporary path and inspected. The 96-page PDF has SHA-256
`1d0e3cff08cbc7244d282e2c817f15fa3829b05941efaa4218ead49c9ec0e2b4`. Page 1 fixes the
conventional binomial formula and generating function and says that the combinatorial
interpretations continue Exercise 6.19; later pages provide many distinct interpretations. The
mutable copy was not added to the repository. This is a subject-family lead, not an immutable
catalog-cited proof source, selected proposition, correction audit, independent review, or `H0`
record.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e` on Linux `7.0.0-27-generic` x86_64.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0921` | exit 0; rank 1463, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 6735,6740 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| source-lead retrieval and `file`, `wc -c`, `sha256sum`, `pdfinfo`, and `pdftotext -layout` inspection | exit 0; 96-page, 604729-byte Stanley PDF; formula, generating function, interpretation-family statement, and mutable numbering warning inspected; family lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| bounded case-insensitive Catalan-number search over pinned mathlib and tracked Lean | exit 0; exact recurrence, formula, tree count, Dyck-word count, and generating-series candidates found; no catalog-selected root or bounded package exists |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0921/IntakeProbe.lean)` | exit 0; eight adjacent pinned declarations elaborated; stdout SHA-256 `6905bdd34565c91d65693680081ade0d6ba72930cc34d97ecc1dae9980422797`; four representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0921-pycache python3 -m py_compile Stage1_Instances/THM-M-0921/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0921/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, null target, H5/M4/R4 boundary, pins, hashes, receipt/packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0921/check_intake.py` | exit 0; public replay mode passes without the scheduler-only root worker packet |
| prohibited-construct `rg` scan over owned `*.lean` | exit 1 as expected; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| scoped `awk` trailing-whitespace checks on every new file plus `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

An immutable source edition and exact proposition or bounded multi-root package, complete Catalan
definition and object-family selection, size/labelling/quotient conventions, source proof and
errata mapping, independent review, ordered binders, conclusion, and boundary cases remain open.
So do the canonical Lean expression and environment fingerprints, checked transports, statement
mutations, exhaustive formal anchor and terminal-body audit, discovery protocol, obligation
registry, typed graphs, `<=100` leaf ledgers, proof and composition, trust/provenance closure,
readable reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. The strong adjacent mathlib candidates do not
remove these gates, and these open gates do not invalidate a truthful self-tested `planned` intake.
