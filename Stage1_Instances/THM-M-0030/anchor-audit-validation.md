# THM-M-0030 Anchor-Audit Validation

Item: `S56-M-0030-ANCHOR_AUDIT`

Base revision: `7e54c0fcaf9c0e53fa7afbbeb0a36218152f932c`

Base tree: `80ece87e35401b07ba76abc36ea83440b5fa7f31`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Ideal.iInf_pow_eq_bot_of_isLocalRing` has the frozen proper-ideal hypotheses and conclusion. Its
only interface difference is binder ordering, which `AnchorAudit.lean` resolves with a direct
zero-strengthening wrapper. Lean prints the transparent terminal body, reports it and its two
immediate bridge declarations sorry-free, and reports only `propext`, `Classical.choice`, and
`Quot.sound` for the three declarations and exact wrapper.

The terminal declaration specializes the finite-module theorem at `M = R`. That theorem reduces
the local-ring hypothesis to the Jacobson-radical theorem through `le_maximalIdeal` and
`maximalIdeal_le_jacobson`; the latter uses the finitely generated intersection submodule and a
Nakayama determinant-trick witness. These declarations are one deduplicated proof path.

A bounded immutable search found the exact name in mathlib and as downstream uses in Atlas and
FLT. Neither external project supplies an independent declaration or exact root wrapper. Atlas
uses the same Lean and mathlib pins; FLT uses different pins. GitHub code search and grep.app were
inaccessible, and discovery saturation is not claimed.

The exact mathlib route is a self-tested `M0-W / E2` candidate. The accepted root remains
`[H1, M3, R3]` until downstream proof integration, complete provenance/trust closure, `E1`, and
master acceptance. Neither `AUDIT-Z` nor theorem completion is claimed.

## Commands And Results

All local validation used the automation-provided canonical `.lake` symlink read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard structure and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0030` | 0 | rank 1075; planned; L0/rework-required; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386...ea95`, tree `bdc39a31...5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; dependency worktree clean |
| manifest-driven `git rev-parse HEAD` and `git status --short` over all 11 materialized packages | 0 | every package matched its manifest revision and had a clean worktree |
| bounded `rg` search over repository-local Lean and all locally materialized packages | 0 | only pinned mathlib supplied the proof declaration; no independent local-package body found |
| anonymous GitHub repository metadata queries for theorem name and exact name | 0 | three zero-result metadata queries recorded with response hashes |
| GitHub code search for the exact declaration | HTTP 401 | authentication required; limitation, not negative evidence |
| grep.app queries for exact name and theorem name | HTTP 429 | security checkpoint; limitation, not negative evidence |
| Sourcegraph global exact-name query including forks and archives | 0 | done with no skipped results: 11 matches in 6 files/3 repos; mathlib declaration plus downstream Atlas/FLT uses |
| immutable raw metadata inspection of Atlas `34ffed...fb50` and FLT `c541dd...706` | 0 | Atlas pins Lean 4.29/mathlib `8a178...`; FLT pins Lean 4.31-rc2/mathlib `96fd0...`; neither contains an independent exact proof |
| `lake env lean ../../Stage1_Instances/THM-M-0030/AnchorAudit.lean` from `Formalizations/Lean` | 0 | exact wrapper elaborated; body printed; three sorry-free and four expected axiom reports; stdout SHA-256 `b038ca11...b6c0` |
| `python3 -B Stage1_Instances/THM-M-0030/check_anchor_audit.py` | 0 | identities, current authority hashes, pins, sources, candidate classifications, packet, and Lean replay agreed |
| `python3 -m json.tool` on structured owned files and the root packet | 0 | all structured artifacts parsed |
| scoped prohibited-construct scan over `AnchorAudit.lean` and the pinned proof-body slice | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, declared axiom, unsafe/opaque declaration, oracle/backend marker, or `proof_wanted` |
| `git diff --check -- Stage1_Instances/THM-M-0030 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Status Boundary

This phase supplies provisional self-tested anchor evidence pending master acceptance. The
obligation registry, proof-phase integration, complete transitive trust/TCB closure, primary-source
and readable reconstruction review, hermetic and independent validation, deterministic release
bundle, `AUDIT-Z`, and theorem completion remain open.
