# Intake validation

Base revision: `0ea006c25dcbfe400adbb084c0a3476a9b271741` (tree
`ff2e3bde08d7f5d6c83519160a4a6bd2cb7526db`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers manifest membership, the planned dossier, provisional full-SVD scope,
duplicate boundary, source-statement crosswalk, six-node open task DAG, JSON/scoped invariants, and
a narrow pinned Lean prerequisite API and axiom probe. It does not validate a canonical SVD Lean
target or proof because source ratification, exact elaboration, factor construction, body
provenance, and trust closure remain open. The automation-provided canonical `.lake` symlink was
pre-existing and used read-only; no dependency update, build, clone, fetch, or other `.lake`
mutation was performed. This dirty worker evidence is nonrelease evidence.

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

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0044` | 0 | rank 1084, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | preflight contained only the automation-provided untracked `Formalizations/Lean/.lake` symlink |
| `git blame -L 335,340 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| author-hosted Axler fourth-edition PDF inspection | 0 | Definition 7.65 and Theorem 7.70 on printed pages 271 and 273-274 were mapped as a modern source lead; no H0 packet accepted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes recorded above |
| bounded exact-topic search in pinned mathlib | 0 | singular-value and spectral prerequisites found; no terminal SVD witness theorem located; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0044/IntakeProbe.lean)` | 0 | twelve prerequisite APIs elaborated; support and matrix spectral theorem axiom reports were `[propext, Classical.choice, Quot.sound]` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all finalized structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0044-pycache python3 -m py_compile Stage1_Instances/THM-M-0044/check_intake.py` | 0 | scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0044/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, planned H1/M3/R3 boundary, source, duplicate and pin hashes, artifact inventory, receipt packet, and six open tasks agree |
| prohibited Lean construct scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0044 .stage1-worker-selftest.json` plus scoped new-file checks | 0 | no whitespace diagnostics |

## Known downstream failures

- No immutable primary theorem/proof passage has been admitted and independently reviewed with
  scalar domain, matrix and factor shapes, definitions, assumptions, conclusion, attribution,
  proof-boundary, and errata mapping.
- `THM-M-1449` remains an unreconciled likely duplicate; no source or formal credit is transferred.
- The conventional full finite rectangular real/complex scope is selected but not ratified;
  full/thin form, star, unitary, rectangular diagonal, ordering, padding, and empty dimensions
  remain statement-gate decisions.
- No canonical Lean expression or environment fingerprint, checked matrix/linear-map transport,
  boundary witness, or four-class statement mutation has been accepted.
- Formal anchor and terminal-body provenance audit, discovery protocol, obligation registry, typed
  graphs, proof, composition, readable reconstruction, hermetic replay, deterministic bundle,
  independent verification, master acceptance, audit completion, and theorem completion remain
  open.

These failures do not invalidate a truthful, self-tested `planned` intake. Only the integration lane
may accept the provisional node receipt.
