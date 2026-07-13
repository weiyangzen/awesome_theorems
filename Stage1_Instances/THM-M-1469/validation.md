# Intake validation

Base revision: `521bd42e5ab5e30513a3c2b7377ea4a1516c0d16` (tree
`6f3d9fcf297fe5251a1dc839c1e67930001a86fc`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and non-substitution boundaries, open
task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does not validate a
canonical adaptive finite-element proposition or proof because neither has been selected. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

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

## Source boundary

Crossref bibliographic metadata for DOI `10.1137/0715049` was inspected and matched the
Babuška-Rheinboldt title, author pair, *SIAM Journal on Numerical Analysis* 15(4), 1978, and pages
736-754. The observed response digest was
`c8515c57a6154543d140c9e520605e9c9b1dc55fe5fce59d41fe1829512fb2c7`. The publisher PDF endpoint
returned HTTP 403 and public access metadata described the article as closed. No primary theorem
passage, assumptions, proof, corrections, immutable capture, catalog root selection, or independent
review was accepted. Bibliographic agreement alone does not support `H0`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1469` | exit 0; rank 1146, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 10721,10726 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error 'https://api.crossref.org/works/10.1137/0715049' -o /tmp/thm1469_crossref.json` plus `sha256sum` and bounded `jq` field extraction | exit 0; response digest and matching bibliographic fields recorded above; metadata only |
| `curl -L --fail --silent --show-error -D /tmp/thm1469_headers -o /tmp/thm1469_siam.pdf 'https://epubs.siam.org/doi/pdf/10.1137/0715049'` | exit 22; HTTP 403, so no primary source text was admitted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | exit 0; pinned revision and tree recorded above; mathlib worktree clean |
| `rg -n -i 'adaptive finite element\|adaptive.?fem\|a posteriori (error\|estimat)\|residual estimator\|reliability\|efficiency' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems --glob '*.lean'` | exit 0; only generic efficiency prose and an unrelated fixed-point posteriori result matched; no source-identical adaptive-FEM target declaration found; intake discovery only |
| `(cd Formalizations/Lean && env -i HOME="$HOME" LANG=C.UTF-8 LC_ALL=C.UTF-8 PATH="$PATH" lake env lean ../../Stage1_Instances/THM-M-1469/IntakeProbe.lean)` | exit 0; eleven adjacent coercive-form, projection, and nested-subspace convergence APIs elaborated; representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1469-pycache python3 -m py_compile Stage1_Instances/THM-M-1469/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `env -i HOME="$HOME" LANG=C.UTF-8 LC_ALL=C.UTF-8 PATH="$PATH" python3 -B Stage1_Instances/THM-M-1469/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, null target, H5/M4/R4 boundary, pins, exact artifacts, receipt/packet, and six open tasks agree |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-1469/IntakeProbe.lean` | exit 1 as expected; no prohibited Lean construct matched |
| scoped `git diff --check` plus per-new-file whitespace validation | exit 0; no whitespace diagnostics |

## Known open gates

The method gloss must be redirected to an independently reviewed, immutable, exact proposition.
The PDE or variational problem, spaces, meshes, elements, estimator and local indicators, constants,
marking/refinement algorithm, solve accuracy, arithmetic model, selected conclusion, ordered binders,
neighbor-target identity, and degenerate cases remain open. So do the primary theorem and proof
crosswalk, canonical Lean expression and environment fingerprint, checked transports, statement
mutations, exhaustive formal anchor audit, discovery protocol, obligation registry, typed graphs,
proof and composition, trust/provenance closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These open gates do not invalidate a truthful self-tested `planned` intake.
