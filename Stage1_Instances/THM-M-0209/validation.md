# Intake validation

Base revision: `72e9e8092182121a6794921f61fcc9cae22f726d`; base tree:
`0d6c1fdf06d1573c256af331c6b198e5a787af43`.

This validation covers target membership, the planned dossier and open task DAG, exact repository
wording, modern-source and non-substitution boundaries, JSON and scoped invariants, a narrow pinned
Lean discovery probe, prohibited-construct hygiene, and whitespace. It does not validate a
canonical Descartes-circle statement, source fidelity, proof, audit completion, or terminal status.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The immutable arXiv v1 PDF of Lagarias, Mallows, and Wilks' *Beyond the Descartes Circle Theorem*
was inspected as a modern source lead. The 561,140-byte PDF has SHA-256
`b5a2da8a...d7`. Theorem 1.1 and its definition context identify the candidate quadratic bend
identity, and the next page supplies the compatible-orientation and historical boundaries. The file
was not added to the repository. No source was admitted at H0 and no independent review ran.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `Mathlib/Geometry/Euclidean/Sphere/Tangent.lean` SHA-256:
  `1f71ad445672095889107a49893bfd74b05d5fba54ef89b8df298c4649240cec`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless another
working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0209` | 0 | rank 1540; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 1506,1511 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| immutable arXiv `math/0101066v1` PDF fetch; `pdfinfo`; `pdftotext`; `sha256sum` | 0 | 25-page, 561,140-byte modern source lead; Theorem 1.1 and orientation/history context inspected; SHA-256 `b5a2da8a...d7`; transient discovery input only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib `rev-parse HEAD HEAD^{tree}` and `status --short` | 0 | revision/tree above; empty status; source remained clean |
| bounded exact-topic `rg` search over pinned mathlib and repo-local Lean | 0 | no terminal Descartes/Soddy four-circle bend identity or signed-bend model found; ordinary sphere tangency APIs and unrelated name matches located; discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0209/IntakeProbe.lean)` | 0 | twelve sphere/tangency interfaces elaborated; both iff bodies reported only `propext`, `Classical.choice`, and `Quot.sound`; output SHA-256 `b499e7dc...27c9`; no canonical root declared |
| `python3 -m json.tool` on owned JSON and root worker packet | 0 | all finalized structured artifacts parse as JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0209-pycache python3 -m py_compile Stage1_Instances/THM-M-0209/check_intake.py` | 0 | scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0209/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M4/R4 boundary, source hashes, null target, artifact inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0209/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited-construct scan over `IntakeProbe.lean` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| direct final-newline/trailing-whitespace checks for every new file; `git diff --check` | 0 | no whitespace diagnostics |

## Known open gates

Master acceptance, immutable exact source admission, independent review, full definition and
assumption transcription, complete proof and correction audit, historical attribution boundary,
selection between ordinary and oriented formulations, canonical Lean expression and environment
fingerprints, minimal imports, checked transports, statement mutations, immutable anchor and
terminal-body provenance audit, discovery and obligation freezes, typed graphs, proof composition,
readable reconstruction, hermetic replay, deterministic bundle, and independent verification all
remain open.

This is provisional worker self-test evidence for `S56-M-0209-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt, audit completion, or theorem completion.
