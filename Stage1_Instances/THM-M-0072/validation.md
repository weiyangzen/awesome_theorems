# Intake validation

Historical scope note: this record describes the intake node at its original base snapshot. Its
statements that no canonical target had yet been frozen are superseded in the live dossier by
`statement.json` and the provisional `statement-receipt.json`; they remain accurate descriptions of
what the intake run itself validated and do not grant or revoke statement-node acceptance.

Base revision: `59c86ca38b16fe4d3901ba66530aae4df0e881b0` (tree
`2b8fc12c558d4fe807d7b4ac4b2c9a127002338e`). Validation date: 2026-07-13
(Asia/Shanghai).

This validates only the `S56-M-0072-INTAKE` planned dossier: manifest and execution identity, source
and non-substitution boundaries, exact owned inventory, open task DAG, pinned API availability, and
representability of a deliberately noncanonical source-scope envelope. It does not validate a
canonical Thompson statement or proof. The automation-provided canonical `.lake` symlink was
pre-existing and used read-only; no update, build, clone, fetch, or dependency mutation was run.
This dirty worker packet is nonrelease evidence.

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
| `python3 scripts/stage1_target.py show THM-M-0072` | exit 0; rank 1102, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git blame -L 533,538 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded source inspection of the AMS-hosted Thompson 1968 PDF and arXiv `1303.5996v2` | exit 0; primary Lemma 5.38(a)(i), printed page 411, and its proof located; Lynd independently names it the classical lemma; hashes recorded |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and scoped status | exit 0; pinned revision/tree recorded; status empty |
| bounded `rg` search for Thompson, 2-perfect, p-perfect, a local predicate, and target ID over repo-local and pinned Lean | exit 1; expected no-match result; no exact formal theorem or established predicate located |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0072/IntakeProbe.lean)` | exit 0; thirteen APIs and the noncanonical source envelope elaborated; adjacent proof axioms were `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0072-pycache python3 -m py_compile Stage1_Instances/THM-M-0072/check_intake.py` | exit 0; checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0072/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; target, authority, sources, H1/M3/R4 boundary, null canonical target, pins, inventory, receipt, worker packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

Independent approval of the source identity, the 1964/1968 conflict, exact part of Lemma 5.38,
universal versus restricted formulation, incorporated definitions, correction and preservation
record, ordered binders, nested coercions, exact conclusion, and alternate transports remain open.
So do canonical expression and environment fingerprints, mutations, exhaustive formal anchor and
provenance audit, discovery and obligation freezes, typed graphs, proof and composition, readable
reconstruction, trust closure, hermetic replay, deterministic bundle, independent verification,
master acceptance, audit completion, and theorem completion. These gates do not invalidate a
truthful self-tested `planned` intake.
