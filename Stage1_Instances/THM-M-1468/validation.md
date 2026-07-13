# THM-M-1468 intake validation

Base revision: `521bd42e5ab5e30513a3c2b7377ea4a1516c0d16` (tree
`6f3d9fcf297fe5251a1dc839c1e67930001a86fc`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target-set consistency, the planned dossier, source-statement identity and
non-substitution boundaries, the six-node open task DAG, structured intake invariants, and a narrow
pinned Lean API probe. It does not validate a canonical hp finite-element proposition or proof:
the catalog supplies a method-family gloss rather than a source-selected truth-valued statement.
The automation-provided canonical `.lake` symlink was pre-existing and used read-only. No
dependency update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker
run is nonrelease evidence.

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

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1468` | exit 0; rank 1145, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree match this record |
| `git blame -L 10714,10719 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref lookups for DOI `10.21236/ADA170144`, DOI `10.1051/m2an/1987210201991`, and DOI `10.1137/0718033`; NUMDAM metadata/PDF inspection | exit 0; located the 1986 Babuska-Suri report, 1987 journal edition, and 1981 Babuska-Szabo-Katz p-version; the full 41-page NUMDAM PDF hash was `0f7272597535ec9836eb8c00a6171cba094418db9b692b7ff7525c4f5d867805`; Theorems 4.8 and 5.4 confirm multiple regular/singular candidate roots; no source was admitted as the catalog proposition |
| bounded exact-topic `rg` search in repo-local Lean and pinned mathlib | exit 1 as expected for no matches; empty output SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; no source-identical hp finite-element, combined-hp, Cea, or quasi-optimality terminal declaration located; intake discovery only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1468/IntakeProbe.lean)` | exit 0; eleven adjacent coercive-form, projection, and polynomial-degree APIs elaborated; stdout SHA-256 `561eb2655ef107c310b829075271e64541874e5070c1da250589aee6a43bd314`; representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1468-pycache python3 -m py_compile Stage1_Instances/THM-M-1468/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1468/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, null target, H5/M4/R4 boundary, pins, exact inventory, receipt/packet, and six open tasks agree |
| prohibited-construct scan of `IntakeProbe.lean` | exit 1 as expected; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration matched |
| scoped new-file no-index whitespace checks plus `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

The method label must be redirected to an independently reviewed, immutable, exact proposition.
The catalog attribution/year must be reconciled with the competing Babuska-Suri hp and
Babuska-Szabo p-version sources. The PDE or approximation problem, domain and boundary, continuous
and discrete spaces, mesh/refinement family, polynomial-degree family, conformity, regularity,
hp coupling, norm, rate, constants, ordered binders, conclusion, and degenerate cases remain open.
So do the canonical Lean expression and environment fingerprint, checked transports, statement
mutations, exhaustive formal anchor audit, discovery protocol, obligation registry, typed graphs,
proof and composition, trust and provenance closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion.

These open gates do not invalidate a truthful, self-tested `planned` intake. Only the integration
lane can accept the provisional node receipt.
