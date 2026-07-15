# THM-M-0578 proof-phase recheck at base 3862149a (slot65)

Item: `S56-M-0578-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `3862149a6bcf2a64e19fabdced9dd80a706f288e`

Base tree: `d3e57e661c2326a97c8b48580abe1f4a3797cd98`

## Verdict

`blocked`. The exact frozen target
`Stage1Instances.THM_M_0578.MilnorExoticSphereTarget` still has no eligible
terminal Lean 4 proof body in the repository or pinned dependency closure. No
proof body was added. The proof item remains `[ ]`, the root vector remains
`[H3, M4, R4]`, and root closure, audit completion, validation, release, and
theorem completion remain false.

The frozen immediate root cut remains:

- `M0578-C-BUNDLE`: construct the selected smooth Milnor bundle total space;
- `M0578-T-HOMEO`: identify it with the fixed unit seven-sphere by a homeomorphism;
- `M0578-O-NONDIFF`: exclude every smooth diffeomorphism to that sphere.

The first failed proof gate is terminal proof-body availability for
`M0578-C-BUNDLE`. The checked theorem
`ObligationTree.root_of_exoticWitnessPackage` is conditional composition only:
its premise already contains the smooth manifold, homeomorphism, and
nondiffeomorphism certificate. It constructs none of the open packages and
therefore supplies no root proof credit.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains the exact signature only as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`.
`proof_wanted` elaborates a helper axiom inside `withoutModifyingEnv` and then
discards it. Fresh trust-zero probes report the name as unknown and absent from
the imported environment. Local all-ref history contains only its introduction
commit `041fe1fa487`, not a proof-bearing replacement.

A fresh scoped search across target instances, local formalizations, and all
9,676 existing pinned-package Lean files found only this dossier,
`THM-M-0605`'s duplicate statement and conditional assembly, a neighboring
statement probe, and mathlib's discarded marker. No declaration inhabits the
exact root or complete `ExoticWitnessPackage`; no usable Milnor-bundle,
Eells-Kuiper, or Kervaire-Milnor formalization was found. Mathlib's bordism
module still leaves bordisms and bordism groups as future work.

The standard-sphere shortcut was rejected by a trust-zero theorem:
`Diffeomorph.refl` inhabits the standard sphere's self-diffeomorphism type, so
that type cannot be `IsEmpty`. Supplying a different atlas together with the
required emptiness certificate is precisely the missing exotic-smooth-
structure theorem, not an encoding shortcut.

The repository base advanced after the prior `4159121c` recheck and integrated
that blocker packet. The canonical proof-input and pin whitelist is unchanged,
and every frozen target source hash is unchanged. The exact statement,
conditional composition, and negative probes were replayed afresh at trust
level zero. This rebases the persistent formalization blocker to the current
source tree; it does not turn conditional composition into a proof.

Closing the route requires placeholder-free Lean implementations of the Milnor
sphere-bundle construction and boundary conventions, its homeomorphism to the
fixed unit seven-sphere, and distinguishing smooth-invariant computations with
invariance strong enough to derive `IsEmpty Diffeomorph`. Assuming a missing
package, crediting `proof_wanted`, or returning only the conditional composer
would violate the exact theorem boundary and was not done. This root assignment
has exceeded the rev-5.6 five-tick split threshold; further meaningful work
requires dedicated child proof tasks for the already frozen open packages.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink points at shared canonical pinned
artifacts. It was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, checkout repair, network request, or dependency mutation command
was issued. Lean outputs were confined to disposable `/tmp` paths and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0578` | 0 | Rank 622; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0578/check_statement.py` | 0 | Exact target elaborated; all four structural mutations were distinguished; expression digest `c9d29902fc3b1bd25c4a83aa5daaa4ce201798576d7b5e16e9bbc05e76a9d32c`. |
| `python3 Stage1_Instances/THM-M-0578/check_anchor_audit.py` | 0 | Exact marker and discard semantics passed at the pins; root remains M4 formalization debt. |
| `python3 Stage1_Instances/THM-M-0578/check_obligation_tree.py` | 0 | 13 obligations and 28 typed edges passed; denominator `67da617160dcfef6ea2eb819f105ab0e2a68a351476d55e5761d2e668e63aeda`; root remains open M4. |
| `cd Formalizations/Lean && timeout --foreground 120s lake env lean --version` plus executable digest | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; executable SHA-256 `3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`. |
| isolated trust-zero `lake env` replay | 0 | Exact statement and conditional composition elaborated; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound`; disposable statement olean SHA-256 `83dcfaec38f0d842614531d19db521eb5f8496fa2d891fe59c6e2fc189d3d3a7`. |
| trust-zero standard-sphere, name, and environment probes | 0 | `Diffeomorph.refl` refuted standard-sphere emptiness with the same three axioms; the discarded marker was unknown and environment membership was false; probe source SHA-256 `f3dd6926e6e9f56ac0b3283f9f1037c441a10f28ed2eee34857a05179b388b91`. |
| scoped retained-body/prerequisite search | 0 | Matching lines were duplicate or conditional statements, metadata/audit material, a neighboring probe, or the discarded marker; no eligible terminal body exists. |
| local marker/ProofWanted/history/bordism inspection | 0 | The marker is discarded; history contains only introduction commit `041fe1fa487`; bordisms and bordism groups remain future work. |
| forbidden-construct scan of owned Lean files | 1 | Expected no-match exit; no prohibited proof escape was found. |
| scoped `git diff --name-status 4159121c..HEAD` | 0 | Empty for every canonical proof input and Lean pin; the whole-target delta contains only the prior blocker packet. |
| `python3 -m json.tool` on the paired record | 0 | The current-base blocker record is valid JSON. |
| target-local added-file and final `git diff --check` | 0 | No whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest is absent because the proof phase is incomplete. |

## Exact Recipes

The isolated kernel replay used the pinned Lake environment:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0578-proof-3862149a-slot65.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0578/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0578/ObligationTree.lean "$tmp/ObligationTree.lean"
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground --kill-after=5s 600s \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
sha256sum "$tmp/Statement.olean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground --kill-after=5s 600s \
  "$lean" --trust=0 -t0 -R "$tmp" "$tmp/ObligationTree.lean"
```

The successful loophole/name probe used this disposable Lean source with the
same executable, `LEAN_PATH`, trust level, timeout, and cleanup pattern:

```lean
import Mathlib.Geometry.Manifold.PoincareConjecture
open Lean Elab Command
open scoped Manifold ContDiff
open Metric (sphere)
noncomputable section

theorem standardSphereSelfDiffeomorphNotEmpty :
    ¬ IsEmpty
      (sphere (0 : EuclideanSpace ℝ (Fin (7 + 1))) 1
        ≃ₘ⟮𝓘(ℝ, EuclideanSpace ℝ (Fin 7)),
          𝓘(ℝ, EuclideanSpace ℝ (Fin 7))⟯
        sphere (0 : EuclideanSpace ℝ (Fin (7 + 1))) 1) := by
  intro h
  exact h.false
    (Diffeomorph.refl 𝓘(ℝ, EuclideanSpace ℝ (Fin 7))
      (sphere (0 : EuclideanSpace ℝ (Fin (7 + 1))) 1) ∞)

#print axioms standardSphereSelfDiffeomorphNotEmpty
#check_failure exists_homeomorph_isEmpty_diffeomorph_sphere_seven
run_cmd do
  let retained :=
    (← getEnv).contains `exists_homeomorph_isEmpty_diffeomorph_sphere_seven
  if retained then
    throwError "proof_wanted marker unexpectedly retained"
```

## Retry Condition

Resume after placeholder-free implementations of `M0578-C-BUNDLE`,
`M0578-T-HOMEO`, and `M0578-O-NONDIFF` with their frozen child obligations.
Alternatively, integrate an immutable compatible Lean 4 proof-bearing
declaration of the exact root with a complete dependency lock, license record,
and terminal-body provenance, then rerun node-scoped exact-type, trust,
provenance, and composition checks.

This is a current-base nonrelease blocker record. It is not a proof receipt,
does not satisfy `S56-M-0578-PROOF`, proposes no state change, and supports
neither root closure nor theorem completion. Because the assigned proof phase
is incomplete, `.stage1-worker-selftest.json` is intentionally absent.
