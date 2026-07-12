# THM-M-1146 anchor-audit validation

Item: `S56-M-1146-ANCHOR_AUDIT`  
Base revision: `b24e74e26136fe318a124a7754cc67fdb2a2f24c`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

Axler, Bourdon, and Ramey, *Harmonic Function Theory*, second edition,
Theorem 4.12 on printed pages 67-68 is an exact modern mathematical source
for the frozen specialization. It assumes symmetry about a hyperplane,
continuity and harmonicity on the positive side, and zero values on the
hyperplane. Its proof explicitly defines the negative odd-reflection branch.
The audited author-hosted PDF has SHA-256
`4e64124f7e36993ee784e575a024505f99d484ccf959d2d3864eae9232af8bf1`.
This resolves the statement-fidelity question, but the human status remains
`H3`: no primary historical source or independent review is claimed.

No exact Lean closure was found. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, negation, harmonic locality,
complex conjugation, and the complex mean-value equality are real supporting
anchors. They do not prove harmonicity across the reflecting boundary. In
particular, the available mean-value theorem is the forward direction, while
the cited paper proof needs a converse mean-value/gluing step. The root stays
`M4 / formalization_debt`, with no proof credit and no theorem-completion claim.

The bounded external search found no Schwarz-reflection repository result. It
also inspected `mccorvie/lean-harmonic` at immutable revision
`f3b75687e0ff790ab135811db54d5c2e4ea2170b`; that project contains preliminary
polar-sector work, no matching declaration, and uses an incompatible 2023
nightly plus an unpinned mathlib requirement.

## Commands and exact outcomes

All Lean commands ran from `Formalizations/Lean` against existing pinned
artifacts. No Lake update/build, dependency clone/fetch, or `.lake` mutation was
performed.

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1146` | 0 | rank 351, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact pin `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| scoped `rg` searches over repository-local and pinned mathlib Lean files | 0/1 | supporting harmonic declarations found; no Schwarz/reflection declaration matched (exit 1 for clean no-match queries) |
| GitHub repository API queries for `schwarz reflection lean`, `schwarz reflection theorem lean4`, and `harmonic reflection lean` | 0 | each returned total count 0 |
| immutable raw inspection of `mccorvie/lean-harmonic` revision `f3b7568...b0b` | 0 | source SHA-256 `145c361...a4a2`; no matching declaration; nightly toolchain and moving mathlib dependency confirmed |
| `curl -L --fail https://axler.net/HFT.pdf` plus `sha256sum`, `pdfinfo`, and `pdftotext` inspection | 0 | second-edition Theorem 4.12 and explicit odd-reflection proof found on printed pages 67-68; PDF digest recorded above |
| `lake env lean ../../Stage1_Instances/THM-M-1146/AnchorAudit.lean` | 0 | all six pinned candidate declarations elaborated; audited theorem anchors reported only their actual transitive axioms |
| `lake env lean ../../Stage1_Instances/THM-M-1146/Statement.lean` | 0 | canonical target and statement probes still elaborate |
| `python3 -m json.tool Stage1_Instances/THM-M-1146/anchor-audit.json >/dev/null` | 0 | structured ledger is valid JSON |
| scoped prohibited-token scan of Lean/JSON audit artifacts | 1 | clean no-match result |
| `git diff --check -- Stage1_Instances/THM-M-1146 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This completes only the candidate/source audit phase pending master acceptance.
The obligation tree, proof, release gates, and theorem completion remain open.
