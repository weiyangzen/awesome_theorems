# THM-M-1445 intake validation

Base revision: `b4e1220a37cc10a96534cfd411e3b29523d7fd81` (tree
`a67dd08a83c396119f4762e0ff109cd0df43ee60`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and non-substitution boundaries, open
task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does not validate a
canonical Gaussian-elimination proposition or proof because no source-selected root exists. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
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

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1445` | exit 0; rank 1122, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 10553,10558 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded inspection of Grcar 2011 / arXiv `0907.2397` | exit 0; observed 56-page v4 PDF SHA-256 `e1e0509ea763a44327ce521c39851fdab6e69178ddd6a09de66ab15841f4b2f2`; Sections 1.2 and 3.3 distinguish schoolbook elimination, factorization, and the 1810 least-squares context; source-family lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| bounded exact-topic `rg` search in pinned mathlib and repo-local Lean | completed; found meta homogeneous tableau code, transvection reduction, and adjacent matrix APIs, but no source-selected end-to-end target theorem; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1445/IntakeProbe.lean)` | exit 0; eight adjacent APIs elaborated; stdout SHA-256 `1a21c1a79f4101007aaa805344d1292d840f7b7aa21daa63f1ca2f8778758a06`; no target theorem |
| `python3 -m json.tool Stage1_Instances/THM-M-1445/instance.json`, repeated for `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1445-pycache python3 -m py_compile Stage1_Instances/THM-M-1445/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1445/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest/DAG identity, null target, H5/M4/R4 boundary, source and dependency pins, exact inventory, receipt/packet, and six open tasks agree |
| `rg -n -e '\bsorry\b' -e '\badmit\b' -e '\bsorryAx\b' -e '\baxiom\b' -e '\bconstant\b' -e '\bopaque\b' -e '\bunsafe\b' Stage1_Instances/THM-M-1445 --glob '*.lean'` | exit 1 as expected; no prohibited declaration in the API-only probe |
| scoped new-file no-index whitespace checks plus `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

The method label must be redirected to an independently reviewed, immutable, exact proposition.
The coefficient domain, matrix/system representation, elementary-operation model, pivot policy,
normal form or solver output, solution-set/correctness relation, termination, complexity, numerical
stability, ordered binders, LU boundary, and degenerate cases remain open. So do the canonical Lean
expression and environment fingerprints, transports, statement mutations, exhaustive formal anchor
audit, discovery protocol, obligation registry, typed graphs, proof and composition,
trust/provenance closure, readable reconstruction, hermetic replay, deterministic bundle,
independent verification, master acceptance, audit completion, and theorem completion. These open
gates do not invalidate a truthful self-tested `planned` intake.
