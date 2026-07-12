# Anchor audit

Item: `S56-M-0319-ANCHOR_AUDIT`  
Audit date: 2026-07-12  
Base revision: `ba66c12eb0b1828b8aa19b6fa8eb2171a454e162`

## Result

The pinned mathlib tree at `8a178386ffc0f5fef0b77738bb5449d50efeea95` has no Brouwer
fixed-point terminal theorem. Its nearby fixed-point results are the one-dimensional interval
theorem, contraction mapping results, and unrelated order/dynamics APIs. None has the canonical
nonempty compact convex finite-dimensional Euclidean statement.

One exact Lean 4 completion candidate was located at immutable commit
`harfe/fixed-point-theorems-lean4@11a9f041246d28374edae384241757f9a0cbd5e4`:
`FixedPointTheorems.brouwer.brouwer_fixed_point`. It quantifies over an arbitrary finite-dimensional
real normed space and a continuous subtype self-map. `AnchorAudit.lean` reproduces that exact type
without its body and kernel-checks the adapter to the frozen ambient-map target. Thus its statement
is strong enough and not a substituted ball, cube, interval, or contraction theorem.

The candidate is only `E3 / M3`. Its immutable source uses Lean `4.21.0-rc3` and mathlib
`c873c5d1d1eb371ddca7f0f5eab48e80ed10b7cb`; neither is in this worker's pinned dependency closure.
The downloaded immutable source snapshot was inspected under `/tmp`: the terminal body calls
`homeo_unit_cube_of_convex_compact` and `fixed_point_unit_cube`, and its transitive Lean source has
no `sorry`, `admit`, declaration-level `axiom`, or `unsafe` token. That source scan is not a kernel
receipt. Attempting a narrow check with the existing environment first failed because the external
module oleans do not exist. A candidate-native invocation then attempted to download its missing
toolchain, so it was immediately terminated; fetching/building missing artifacts is prohibited.
There is no external axiom report or independent immutable build receipt, so `M1` is not credited.

The other repository results are Lean 3 projects: `mmasdeu/brouwerfixedpoint` at
`548270f79ecf12d7e20a256806ccb9fcf57b87e2`, and `mlavrent/brouwer-fp-formalization` at
`94a23ed613d5aa7224b48f17a4c67f52a3496251`. They are excluded from the Lean 4 candidate pool;
the latter also describes unfinished proof obligations. Repo-local hits outside this dossier are
different fixed-point theorems or special cases and provide no root proof.

## Search and validation

| Command | Exit | Result |
|---|---:|---|
| `rg -n -i "brouwer|fixed.?point" Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | no Brouwer terminal theorem; only unrelated Brouwerian vocabulary and non-Brouwer fixed-point APIs |
| repo-local `rg` over Lean sources excluding this target | 0 | no exact root proof; different theorem and special-case hits only |
| GitHub repository API query `brouwer fixed point lean theorem` | 0 | three repositories found: one Lean 4 candidate and two Lean 3 projects |
| `git ls-remote` for all three repositories | 0 | immutable heads recorded in `anchor-audit.json` |
| immutable GitHub source tarball inspection under `/tmp` | 0 | exact files, toolchains, dependency pins, terminal bodies, and source hashes inspected; no dependency installed |
| GitHub unauthenticated code search | HTTP 403 | rate limit; recorded negative search limitation |
| grep.app Lean searches | HTTP 503 | service unavailable; recorded negative search limitation |
| `lake env lean ../../Stage1_Instances/THM-M-0319/AnchorAudit.lean` | 0 | candidate type and exact-target adapter elaborated; axiom report printed |
| `python3 ../../Stage1_Instances/THM-M-0319/check_anchor_audit.py` | 0 | structured invariants and Lean adapter passed |

The adapter's `#print axioms` output includes `sorryAx` inherited through the current mathlib
environment, alongside `propext`, `Classical.choice`, and `Quot.sound`. This prevents treating the
adapter check itself as release-grade trust closure; it remains type/transport audit evidence.

## Status boundary

This phase freezes and classifies the discovered candidates and supplies a checked statement
transport. It does not import the external body, prove Brouwer's theorem, establish `M1` or `M0-P`,
complete provenance/trust closure, or claim theorem completion. The root remains `M3`; integration
requires an approved immutable dependency plus a local exact wrapper and axiom/provenance checks.
