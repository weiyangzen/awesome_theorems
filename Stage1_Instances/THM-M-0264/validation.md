# Intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, scope and source crosswalk, open task DAG, structured
invariants, and pinned Lean candidate probe. It does not validate a canonical Bolzano-Weierstrass
statement or proof because source-exact carrier, boundedness, subsequence, convergence, and binder
choices remain open. The automation-provided canonical `.lake` symlink was pre-existing and used
read-only. No update, build, clone, fetch, or dependency mutation was performed. Dirty worker
evidence is nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean after the probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0264` | exit 0; rank 1272, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'`; `git blame -L 1901,1906 -- Docs/researches/math_theorems.md` | exit 0; base revision/tree recorded above; all six source-record lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | exit 0; pinned revision/tree recorded above; empty status output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0264/IntakeProbe.lean)` | exit 0; five direct or supporting interfaces elaborated; both direct declarations reported `[propext, Classical.choice, Quot.sound]`; complete output SHA-256 `6b48207f7b1a9555239c71c399c62cc69f5d7c06548087fd0043192566b39d4b` |
| bounded `rg` search in pinned mathlib and repo-local Lean | exit 0; the explicitly documented proper-metric Bolzano-Weierstrass declarations and supporting compactness interfaces were located; no source-identical root or proof credit was inferred |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 after finalization; all structured artifacts parse |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0264-pycache python3 -m py_compile Stage1_Instances/THM-M-0264/check_intake.py` | exit 0; checker compiled without writing generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0264/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; authorities, source and dependency pins, duplicate boundary, H1/M3/R4 planned state, null target, artifact hashes, receipt/packet, Lean probe, and six open tasks agree |
| token-anchored prohibited Lean declaration scan over the owned path | exit 1 as expected; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` remains permitted |
| scoped new-file whitespace checks and `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

An immutable primary source, exact theorem/page, incorporated definitions, ordered proposition,
assumption and proof crosswalk, attribution and date review, translation, corrections or errata, and
independent review remain open. So do the canonical Lean expression and environment fingerprints,
checked Real specialization and alternate boundedness encodings, statement mutations, exhaustive
anchor and provenance audit, discovery and obligation freezes, typed graphs, proof and composition,
accepted trust closure, readable reconstruction, hermetic replay, deterministic bundle, independent
verification, master acceptance, audit completion, and theorem completion. These open gates do not
invalidate a truthful self-tested `planned` intake.
