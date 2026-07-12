# Anchor-audit validation record

Item: `S56-M-1526-ANCHOR_AUDIT`  
Base revision: `2b5a356f0d547597e745bab548db0caac12e6c96`

## Result

The audit is bound to the frozen expression and `Statement.lean` hash. Pinned mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies Clifford generators and their quadratic and
polarized multiplication laws, plus the matrix-to-linear-map multiplication bridge. All twelve
named declarations in `AnchorAudit.lean` elaborate. A complete pinned-source search found no Dirac
equation, gamma-matrix, spinor, or Klein-Gordon terminal declaration. These APIs are useful
infrastructure but do not prove the frozen factorization.

The immutable external candidate is `HEPLean/PhysLean@cd22b0c28882412447d12d5cfde677c4ad999994`.
Its `Physlib.Relativity.CliffordAlgebra` module defines the four concrete Dirac-representation gamma
matrices, proves their squares and pairwise anticommutation relations, and constructs a surjective
Clifford-algebra map. The Pauli module supplies a second nearby Clifford map. The audited files have
content hashes in `anchor-audit.json`; no proof placeholder was observed in those two modules. They
contain no derivative family, free Dirac factorization, or Klein-Gordon consequence, however, and
therefore are not a terminal candidate or checked transport. Upstream also pins Lean 4.29.1 and
mathlib `5e932f...`, unlike this repository's Lean 4.29.0 and mathlib `8a178...`; no dependency
mutation or compatibility build was performed.

The exact root consequently remains `M3 / formalization_debt`. There is no external closure to
pin or vendor, hence no repo-local integration debt. This completes only the bounded anchor audit;
it supplies no proof, human-source promotion, audit completion, or theorem-completion credit.

## Commands and results

Commands ran on 2026-07-12 inside this worker clone. Lean used only the existing pinned `.lake`
artifacts; no update, fetch, clone, or build was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1526/AnchorAudit.lean` | 0 | Twelve pinned mathlib declarations elaborated and printed their types. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1526/Statement.lean` | 0 | Frozen exact target and statement mutations re-elaborated. |
| `python3 Stage1_Instances/THM-M-1526/check_anchor_audit.py` | 0 | Target hashes, clean installed mathlib pin, source witnesses, probes, and external classification agreed. |
| `rg -l -i 'dirac equation\|dirac operator\|gamma matrix\|gammamatrix\|klein.gordon\|spinor' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No match in the complete pinned mathlib source tree; exit 1 is ripgrep's expected no-match result. |
| Immutable raw inspection of the two PhysLean modules, `lake-manifest.json`, and `lean-toolchain` at `cd22b0...` | 0 | Gamma and Clifford support identified; source and environment SHA-256 values recorded in `anchor-audit.json`. |
| GitHub REST repository search for `Dirac equation Lean theorem prover` | 0 | `total_count=0`, `incomplete_results=false`; response SHA-256 `08c082...2600b2`. |
| GitHub REST code search for quoted Dirac equation in Lean | 0 transport | HTTP 401; response SHA-256 `b7dbd1...e29e`; no negative result claimed. |
| Sourcegraph and grep.app public searches | blocked | HTTP 502 and HTTP 429 respectively; no negative result claimed. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1526` | 0 | Rank 194, planned, legacy artifacts unaccepted, theorem incomplete. |
| `python3 -m json.tool Stage1_Instances/THM-M-1526/anchor-audit.json` | 0 | Structured audit is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1526 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

## Reopen condition

Reopen integration only for a concrete Lean 4 candidate with an immutable revision, compatible
license and dependency closure, exact type or checked transport, terminal body provenance,
placeholder/axiom/unsafe audit, and a successful repo-local pin/import/wrapper check.
