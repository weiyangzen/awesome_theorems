# THM-M-1143 proof-phase validation

Item: `S56-M-1143-PROOF`. Base revision:
`3bb4cb3ae15dff8b48c93242019edec3bf858e48`.

## Verdict

`partial_proof_self_tested_root_blocked`. `Proof.lean` contains genuine, placeholder-free bodies
for bounded-range normalization, the reciprocal-radius limit, and zero-derivative constancy. It
also checks the composition from one precise open analytic interface to
`VanishingDerivativePackage` and then to the exact canonical root.

The new limit body proves that a continuous linear map whose norm is at most `A / R` for every
positive radius is zero. Combined with differentiability supplied by `HarmonicOnNhd`, it turns the
interior estimate into an everywhere-zero Frechet derivative. The calculus body then proves the
exact `ZeroDerivativeConstantPackage` using mathlib's mean-value theorem.

The frozen nodes have planned rather than elaborated obligation fingerprints, so the provisional
receipt conservatively lists supported subbranches and claims no whole frozen obligation closed.
The exact root remains open at `M1143-T-VANISH`; its first unavailable substantive leaf is
`M1143-L-GRADIENT`, the arbitrary-positive-dimensional interior gradient estimate. Pinned mathlib
provides a bounded-harmonic Liouville theorem only on the complex plane. Its general finite-
dimensional harmonic API has no mean-value, Poisson, maximum-principle, gradient-estimate, or
bounded-harmonic Liouville theorem. A Fourier route likewise lacks the required classical-to-
distributional Laplacian and zero-frequency support chain.

The worker packet proposes only proof-phase state `[_]` for self-tested partial execution. It does
not inhabit `InteriorGradientEstimatePackage`, `VanishingDerivativePackage`, or the canonical root,
and does not claim theorem completion.

## Narrow validation evidence

All commands ran in the worker clone on 2026-07-14 using the pre-existing canonical pinned Lake
artifacts. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `bash Stage1_Instances/THM-M-1143/check_proof.sh` | 0 | Trust-zero isolated statement/tree/proof replay passed; seven local declarations were sorry-free and used only `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Stage1_Instances/THM-M-1143/check_proof.py` | 0 | Receipt, blocker, source, pin, worktree, timeout, hash, and worker-packet checks passed. |
| `python3 Stage1_Instances/THM-M-1143/check_obligation_tree.py` | 0 | Frozen registry passed with 12 obligations and 24 typed edges; its pre-proof closure snapshot remains open at M3. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1143` | 0 | Rank 348, planned lifecycle, theorem incomplete. |
| `rg -n '(^|[^A-Za-z0-9_])(sorry\|admit\|sorryAx\|implemented_by\|native_decide\|extern)([^A-Za-z0-9_]|$)\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)([[:space:]]|$)' Stage1_Instances/THM-M-1143/Proof.lean` | 1 | Expected no-match exit; no prohibited proof device was found. The structured checker additionally scans after excluding the legitimate `assert_no_sorry` command name. |
| `python3 -m json.tool Stage1_Instances/THM-M-1143/proof-receipt.json`, `python3 -m json.tool Stage1_Instances/THM-M-1143/proof-blocker.json`, and `python3 -m json.tool .stage1-worker-selftest.json` | 0 each | All structured artifacts parsed. |
| `git diff --check -- Stage1_Instances/THM-M-1143 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The toolchain is Lean 4.29.0 at commit `98dc76e3...fb04`. Pinned mathlib is
`8a178386...ea95` with tree `bdc39a...5c2b`; its source worktree was clean.

## Reopen condition

Resume after a placeholder-free implementation or immutable compatible import of
`M1143-L-GRADIENT`. Then recheck the derivative-vanishing package, exact root, proof-body
provenance, axiom/TCB closure, and downstream rev-5.6 gates. Until then the exact root remains M3,
audit completion is false, and theorem completion is false.
