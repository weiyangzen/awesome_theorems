# Intake validation

Base revision: `d257e1e5e5fa003d6e1f26344c0331bf99374fa9` (tree
`fa06b50b528e038d182d5479a18296f63fa5eae5`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, two-clause scope and source crosswalk, six-node open
task DAG, structured intake invariants, and a narrow pinned Lean interface probe. It does not
validate a canonical conjunction or proof because the source crosswalk, independent binder scopes,
root packaging, exact expression, and statement mutations remain open. The automation-provided
canonical `.lake` symlink was present before this work and used read-only. No dependency update,
build, clone, fetch, or other `.lake` mutation was performed. This dirty worker evidence is
nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; its package worktree remained clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0617` | exit 0; rank 1311, planned, no legacy slot, legacy artifacts unaccepted, source status untrusted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'`; `git blame -L 4580,4585 -- Docs/researches/math_theorems.md` | exit 0; base revision/tree recorded above; all six uncited source lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded bibliographic retrieval attempts for a Munkres source copy and metadata | source PDF and metadata endpoints timed out or were unavailable; no source passage was admitted, no theorem/page was guessed, and the concrete source-retry blocker was recorded |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | exit 0; pinned revision/tree recorded above; empty status output |
| bounded `rg` inspection of pinned compactness source and repo-local artifacts | direct first- and second-clause interfaces plus the continuous-on variant located; no existing target dossier or source-identical root was found; this was intake discovery, not exhaustive anchor audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0617/IntakeProbe.lean)` | exit 0; `IsCompact`, the three exact-topic interfaces, and two axiom reports elaborated; complete output SHA-256 `1ba2ff9c58728fdf189ec19105f478c2d8a96c20a12e514bb23e86c561484d75`; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 after finalization; all structured artifacts parse |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0617-pycache python3 -m py_compile Stage1_Instances/THM-M-0617/check_intake.py` | exit 0; checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0617/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; target/DAG identity, frozen human gloss, null formal root, H1/M3/R4 boundary, source and dependency hashes, exact artifact inventory, receipt/packet agreement, pinned Lean output, and six open tasks agree |
| token-anchored prohibited Lean declaration scan over `IntakeProbe.lean` | exit 1 as expected; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration; diagnostic `#print axioms` is permitted |
| scoped per-file whitespace checks plus `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

An admitted immutable source edition, exact statements and incorporated definitions for both
clauses, complete assumption and proof maps, historical attribution, translation, corrections or
errata, and independent review remain open. So do the exact independent Lean binders, conjunction
or checked child-to-root composition, minimal environment and expression fingerprints, alternate
transports, statement mutations, exhaustive anchor and body-provenance audit, discovery and
obligation freezes, typed graphs, proof and composition credit, trust closure, readable proof
reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These open gates do not invalidate a
truthful self-tested `planned` intake.
