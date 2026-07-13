# Intake validation

Base revision: `f3910e9d9c9dde383801913343b9244462e6173a` (tree
`28f0e995eac01d75999b013a02e02eb792c07754`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source and scope boundary, entirely open task DAG,
structured receipt, and a narrow pinned Lean API probe. It does not validate a canonical Rayleigh
quotient statement or proof because neither has been selected. The automation-provided canonical
`.lake` symlink was pre-existing and used read-only; no dependency update, build, clone, fetch, or
other `.lake` mutation was performed. The dirty worker evidence is nonrelease evidence.

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
| `python3 scripts/stage1_target.py show THM-M-0055` | exit 0; rank 1522, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 412,417 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref lookup for DOI `10.1112/plms/s1-4.1.357` | exit 0; identified Strutt's 1871 paper as a bibliographic lead; full-text request was access-controlled, so no statement or proof mapping was credited |
| author-hosted Spielman PDF download plus `pdfinfo`/`pdftotext` inspection | exit 0; 400 pages and 2,902,506 bytes; SHA-256 `6b70ebd...9369861c`; Chapter 2 definition, Theorems 2.0.1 and 2.2.1, and proof boundaries inspected as an uncredited modern lead |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision/tree above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0055/IntakeProbe.lean` | exit 0; twelve adjacent APIs elaborated; 3,402-byte combined output SHA-256 `524460a0dd7dd5530443ec243d1341a733a2c7dc2ece56b848bf8de39a15c4d1`; no target declared |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | exit 0 after finalization; all JSON valid |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0055-pycache python3 -m py_compile Stage1_Instances/THM-M-0055/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0055/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; target/DAG identity, null target, H1/M3/R4 boundary, source and pin hashes, exact inventory, receipt/packet agreement, and six open tasks agree |
| prohibited Lean construct scan over the sole owned Lean source `IntakeProbe.lean` | exit 0 under inverted no-match policy; no `sorry`, `admit`, `sorryAx`, bodyless declaration, `opaque`, or `unsafe` escape exists |
| `git diff --check -- Stage1_Instances/THM-M-0055 .stage1-worker-selftest.json` plus explicit checks for untracked files | exit 0; no whitespace errors |

## Known open gates

Master acceptance of this provisional intake remains open. So do immutable exact source selection,
historical identity and date, the literal `Hermite` interpretation, extremal-versus-indexed scope,
complete incorporated definition/premise/conclusion/proof-boundary and correction mapping,
real-to-complex and matrix-to-operator transports, independent source review, canonical Lean
expression and environment fingerprint, minimal imports, checked alternate encodings, statement
mutations, exhaustive anchor audit, discovery protocol, obligation registry, typed graphs, proof
and composition, trust and provenance closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, audit completion, and theorem completion. These
failures do not invalidate a truthful self-tested `planned` intake.
