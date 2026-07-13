# THM-M-0043 Anchor-Audit Validation

Item: `S56-M-0043-ANCHOR_AUDIT`

Base revision: `72f928bdf1a47d7c119826db45575bd02a3a63ce`

Base tree: `171a6bfae88220f5df9b39cdd6c7e1bf17639889`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

The pinned mathlib tree does not contain the exact normal complex matrix theorem. Its closest
packaged result, `Matrix.IsHermitian.spectral_theorem`, has the required unitary-diagonal output
shape but assumes the strictly stronger Hermitian condition. `AnchorAudit.lean` checks that output
adapter and a one-dimensional normal non-Hermitian matrix with entry `Complex.I`.

The broader external search located an exact proof at immutable
`facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50`:
`SpectralTheorem.normal_complex_unitarily_diagonalizable`. It proves the conjugated-diagonal form for
all finite index types, so it is stronger than the frozen nonempty target. The local audit adapter
checks the exact transport back to the root equation. The immutable source was streamed to a
temporary file and elaborated against the same Lean 4.29.0 and mathlib revision as this repository;
Lean reports only `propext`, `Classical.choice`, and `Quot.sound` for its terminal theorem.

This is an `M1` candidate with `E2` evidence, not `M0-P`: the Atlas declaration is not in the local
dependency closure, the project's noncommercial/no-training license needs review, and there is no
accepted local wrapper, full transitive trust packet, or release-grade `E1` receipt. The accepted
root remains `H1/M3/R4`. Neither `AUDIT-Z` nor theorem completion is claimed.

## Commands And Results

All local validation ran in this worker clone. The automation-provided canonical `.lake` symlink
was used read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard structure and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0043` | 0 | rank 1083; planned; L0/rework-required; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a1783...ea95`, tree `bdc39a...5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain=v1 --untracked-files=no` | 0 | empty output; dependency worktree clean |
| bounded `rg`/`git grep` over repository-local Lean and pinned mathlib | 0/1 | only strict Hermitian theorem and composition anchors found; no exact pinned root declaration; exit 1 denotes a no-match probe |
| GitHub repository queries and Sourcegraph streaming queries recorded in `anchor-audit.json` | 0/403/429 | five topic repositories classified; broader `IsStarNormal` query located Atlas; GitHub code search and grep.app access failures recorded, so saturation is not claimed |
| immutable raw/codeload inspection of the six external projects in `anchor-audit.json` | 0 | full commits, reconstructed trees, source/archive hashes, tools, dependencies, licenses, and gap status recorded without retaining a checkout |
| streamed Atlas source plus `#print axioms SpectralTheorem.normal_complex_unitarily_diagonalizable`, run by `lake env lean` | 0 | exact terminal elaborated under matching pins; axiom output SHA-256 `65afdb...565`; only `propext`, `Classical.choice`, `Quot.sound` |
| `lake env lean ../../Stage1_Instances/THM-M-0043/AnchorAudit.lean` from `Formalizations/Lean` | 0 | Hermitian adapter, exact Atlas-shape adapter, strictness witness, and route probes elaborated; stdout SHA-256 `8ddeb8...308` |
| `python3 -B Stage1_Instances/THM-M-0043/check_anchor_audit.py` | 0 | pins, local blobs/hashes/body markers, Atlas immutable source and standalone replay, inventory, packet, and classifications matched |
| `python3 -m json.tool` on anchor JSON artifacts and root packet | 0 | all structured artifacts parsed |
| scoped prohibited-construct scan over `AnchorAudit.lean` | 1 (expected no match) | no proof gap, axiom declaration, unsafe/opaque body, TODO, FIXME, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0043 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Search Boundary

The frozen inventory classifies nine candidate groups. Public query response hashes and access
failures are recorded in `anchor-audit.json`. Repository metadata and indexed code search do not
establish internet-wide absence or discovery saturation. The exact Atlas result supersedes the
earlier bounded negative intake search but does not by itself integrate or accept the theorem.

## Status Boundary

This phase supplies provisional self-tested anchor evidence pending master acceptance. License and
integration policy, the obligation registry, proof-phase wrapper or independent implementation,
full provenance/trust closure, source and readable reconstruction review, hermetic and independent
validation, deterministic release bundle, `AUDIT-Z`, and theorem completion remain open.
