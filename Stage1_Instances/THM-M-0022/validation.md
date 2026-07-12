# Intake validation

Base revision: `f608e06dccf2e158f1d2feeadb48f1b64d296cdd` (tree
`c0e4ab057a962cd2020342a692d39952f65d8bec`). Validation date: 2026-07-13
(`Asia/Shanghai`).

This validation covers manifest membership, the fail-closed planned dossier and open DAG,
repository source and duplicate-target provenance, JSON and scoped invariants, and one narrow
pinned Lean API probe. The probe only authenticates generic functional-equation machinery, a
Dirichlet-character special case, and adjacent number-field infrastructure. It neither selects nor
proves a Hecke-character L-function equation. The automation-provided canonical `.lake` symlink was
used read-only; no `lake update`, build, fetch, clone, or dependency mutation was run. The worker
tree is nonrelease evidence because the owned dossier and that pre-existing symlink are untracked.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0022` | 0 | rank 1069; planned; L0/rework_required; no accepted legacy artifact; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before edits, only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; final status adds only this owned dossier and the authorized worker packet |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree match the structured intake record |
| `git blame -L 177,182 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalogue lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| repository inspection of `THM-M-0425`, `THM-M-0426`, and `S1_M_080.lean` | 0 | confirmed separate Hecke L-function and functional-equation targets and that the legacy sibling module is an abstract, nonterminal shape boundary |
| bounded Crossref metadata query for Hecke's paper title | 0 | returned DOI `10.1007/BF01465095` for the 1918 volume 1 paper and `10.1007/BF01202991` for a 1920 continuation; no theorem text was admitted, and the sibling intake's conflicting DOI remains quarantined |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package source is clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0022/IntakeProbe.lean)` | 0 | nine adjacent generic, special-case, adele, and product-formula APIs elaborated; stdout SHA-256 `2f44f648c4bf45d59e2b1612aa03da64e31f25cdf15acf645d7eee3dfb8a47d2`; no target theorem was declared |
| bounded exact-topic `rg` search in pinned mathlib | 1 (expected) | no concrete Hecke-character, Hecke L-function, or idele-class-character occurrence; intake discovery only, not an exhaustive external audit |
| `python3 -m json.tool` over `instance.json`, `task-dag.json`, `intake-receipt.json`, and the worker packet | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0022-pycache python3 -m py_compile Stage1_Instances/THM-M-0022/check_intake.py` | 0 | scoped checker compiles without adding generated files to the repository |
| `python3 -B Stage1_Instances/THM-M-0022/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, H1/M4/R3 boundary, source and pin hashes, null target, exact artifact inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0022/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| prohibited-construct scan over `IntakeProbe.lean` | 1 (expected) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null` and scoped `git diff --check` | raw no-index exit 1 per new file, accepted because output was empty; aggregate diagnostic check and scoped command exit 0 | no whitespace diagnostics; raw exit 1 denotes a nonempty new-file diff rather than an error |

## Known open gates

An immutable primary-source proposition, full definition/assumption/conclusion/normalization and
errata crosswalk, the catalogue-1917 versus publication-date reconciliation, independent source
review, and an authoritative identity and ownership decision for `THM-M-0022` versus
`THM-M-0426` remain open. So do the canonical Lean expression and environment fingerprint,
minimal imports, transports, statement mutations, exhaustive formal anchor audit, discovery
protocol, obligation registry, typed graphs, proof and composition, trust and provenance closure,
readable reconstruction, hermetic replay, deterministic bundle, independent verification, and
master acceptance. These failures prevent statement, audit, or theorem completion but do not
invalidate a truthful self-tested `planned` intake.

This is provisional worker evidence for `S56-M-0022-INTAKE` only. It proposes `[_]` for integration
review; it is not an accepted receipt or a theorem-completion claim.
