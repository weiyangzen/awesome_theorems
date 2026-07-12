# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation is limited to target-set consistency, the planned dossier and open task DAG, source and
scope discrimination, pinned environment identity, adjacent Lean API elaboration, bounded local
name search, JSON and scoped invariants, proof-escape hygiene, and whitespace. The catalog does not
select a unique proposition, so no canonical target, expression hash, statement mutation, source
acceptance, construction, uniqueness theorem, or proof is claimed.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

## Environment

- Platform: Linux 7.0.0-27-generic, x86_64; Lean target `x86_64-unknown-linux-gnu`.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0892` | 0 | rank 1038, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the pre-existing `.lake` symlink; base revision and tree recorded above |
| `git blame -L 6530,6535 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref, OpenAlex, DBLP, and Semantic Scholar metadata inspection for DOI `10.1147/rd.45.0497`, plus temporary complete-scan inspection | 0 | exact 1960 match; HS60 definition and pp. 497-504 classification/uniqueness boundaries inspected; scan SHA-256 `fa0d1563...c09`; access/provenance unsuitable for a lawful public source packet, so no H0 source admitted |
| inspection of arXiv `1405.4643v1` | 0 | modern construction source identifies the unique `(50,7,0,1)` strongly regular graph and Theorem 1.8 construction; PDF SHA-256 `60181514...e8c5`; discriminator only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake versions above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package source clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0892/IntakeProbe.lean)` | 0 | ten adjacent finite-graph, regularity, metric, girth, and strongly regular APIs elaborated; complete output SHA-256 `26a23940...434d8`; no target declaration or proof body |
| bounded case-insensitive `rg` for Hoffman-Singleton and Moore-graph Lean declarations | 1 (expected no match) | no exact-topic target in repo-local or pinned-mathlib Lean; intake discovery only, not exhaustive external audit |
| `python3 -m json.tool` on the three owned/root JSON artifacts after finalization | 0 | valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0892-pycache python3 -m py_compile Stage1_Instances/THM-M-0892/check_intake.py` | 0 | scoped checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0892/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and dependency hashes, H1/M4/R4 null target, inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0892/check_intake.py` | 0 | public replay mode passed without the scheduler-only worker packet |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file whitespace checks and `git diff --check -- Stage1_Instances/THM-M-0892 .stage1-worker-selftest.json` | 0 aggregate | no whitespace diagnostics |

## Known open gates

Exact source and result selection, lawful immutable primary text, complete definition, premise,
conclusion, proof-boundary and correction crosswalk, independent review, and separation of the
degree-7 construction, uniqueness, degree classification, diameter-3 results, and open degree-57
existence branch remain open. So do the canonical Lean target and minimal imports,
expression/environment fingerprints, checked transports, four statement mutation classes,
exhaustive anchor audit, discovery protocol, obligation registry, typed graphs, proof and
composition, source/provenance/trust closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These failures block statement and theorem progress but do not invalidate a truthful
self-tested `planned` intake.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0892-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, H0 source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.
