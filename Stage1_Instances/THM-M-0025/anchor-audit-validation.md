# THM-M-0025 Anchor-Audit Validation

Item: `S56-M-0025-ANCHOR_AUDIT`

Base revision: `94f6abf9359f26384e0f68bef694dc5b9aae624c`

Base tree: `e0083f4f402c93febe4419b51498afa8ecf81c06`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Polynomial.isNoetherianRing` exactly matches the frozen commutative, one-indeterminate target.
The local audit wrapper retains the same universe, structure instances, conclusion, and zero-ring
boundary. Lean prints the substantive finite-generation proof body, reports it sorry-free, and
reports only `propext`, `Classical.choice`, and `Quot.sound` for both the terminal theorem and the
exact wrapper.

The finite-variable `MvPolynomial` and finite-type-algebra routes are downstream of the same
terminal polynomial body and are deduplicated. The only additional public repository located by
the bounded search proves a Noetherian result for formal power series, so it is a carrier mismatch.
No second exact terminal body was established; unauthenticated code-search failures prevent a
discovery-saturation claim.

The exact mathlib route is a self-tested `M0-W / E2` candidate. The accepted root remains
`[H1, M3, R3]` until downstream proof, composition, complete provenance/trust, `E1`, and master
acceptance. Neither `AUDIT-Z` nor theorem completion is claimed.

## Commands And Results

All local validation used the automation-provided canonical `.lake` symlink read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard structure and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0025` | 0 | rank 1070; planned; L0/rework-required; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386...ea95`, tree `bdc39a31...5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; dependency worktree clean |
| manifest-driven `git rev-parse HEAD` and `git status --short` over all 11 materialized packages | 0 | every package matched its `lake-manifest.json` revision and had a clean worktree |
| bounded `rg` search over repository-local Lean and all locally materialized manifest packages | 0 | only pinned mathlib supplied the exact body; no independent locally materialized body found |
| anonymous GitHub repository queries for the theorem name and exact/type aliases | 0 | one power-series mismatch and two zero-result exact queries recorded with response hashes |
| GitHub code search for `Polynomial.isNoetherianRing language:Lean` | HTTP 401 | authentication required; access limitation, not negative evidence |
| grep.app queries for the declaration and theorem name | HTTP 429 | Vercel security checkpoint; access limitation, not negative evidence |
| immutable GitHub API/raw inspection of the power-series repository at `3599301f...bbcf` | 0 | source/tree/blob/hash/license recorded; theorem carrier is `PowerSeries R`, not `Polynomial R` |
| `lake env lean ../../Stage1_Instances/THM-M-0025/AnchorAudit.lean` from `Formalizations/Lean` | 0 | exact type/body printed; terminal sorry-free; two expected axiom reports; stdout SHA-256 `79b75df3...f223` |
| `python3 -B Stage1_Instances/THM-M-0025/check_anchor_audit.py` | 0 | item identity, pins, hashes, source markers, provenance, candidate classifications, packet, and Lean replay matched |
| `python3 -m json.tool` on anchor JSON artifacts and root packet | 0 | all structured artifacts parsed |
| scoped prohibited-construct scan over `AnchorAudit.lean` and the pinned terminal body | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, declared axiom, unsafe/opaque declaration, or `proof_wanted` marker |
| `git diff --check -- Stage1_Instances/THM-M-0025 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Status Boundary

This phase supplies provisional self-tested anchor evidence pending master acceptance. The
obligation registry, proof-phase integration, full transitive trust/TCB closure, primary-source and
readable reconstruction review, hermetic and independent validation, deterministic release bundle,
`AUDIT-Z`, and theorem completion remain open.
