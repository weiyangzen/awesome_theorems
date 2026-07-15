# THM-M-0578 proof-phase recheck at base e08cfa3f (slot63)

Item: `S56-M-0578-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `e08cfa3f7d7a37ef13682a7bac1e61f054d9522f`

Base tree: `002c1691169181f8d5a99919874237d131e9bd0d`

## Verdict

`blocked`. The exact frozen proposition
`Stage1Instances.THM_M_0578.MilnorExoticSphereTarget` still has no eligible
terminal Lean 4 proof body in the repository or pinned dependency closure. No
proof body was added. The proof item remains `[ ]`, the root vector remains
`[H3, M4, R4]`, and root closure, validation, release, audit completion, and
theorem completion remain false.

The frozen immediate root cut set remains:

- `M0578-C-BUNDLE`: construct the selected smooth Milnor bundle total space;
- `M0578-T-HOMEO`: identify it with the fixed unit seven-sphere by a homeomorphism;
- `M0578-O-NONDIFF`: exclude every smooth diffeomorphism to that sphere.

The first failed proof gate is terminal proof-body availability for
`M0578-C-BUNDLE`. The local theorem
`ObligationTree.root_of_exoticWitnessPackage` is valid checked composition, but
its premise already contains the smooth manifold, homeomorphism, and
nondiffeomorphism certificate. It constructs none of the open packages and
therefore supplies no root proof credit.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains the exact signature only as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`.
`proof_wanted` elaborates a temporary helper axiom under
`withoutModifyingEnv`, then discards the environment change. A direct
trust-zero import probe confirms that the name is unknown. The locally present
mathlib `master` ref still contains the marker, and the local all-ref history
finds only its introduction commit `041fe1fa487`, not a proof-bearing
replacement.

A fresh bounded Lean-source search found 11 relevant files. They are confined
to this dossier, `THM-M-0605`'s duplicate statement and conditional assembly,
legacy statement/audit files, one neighboring statement probe, and mathlib's
discarded marker. No declaration inhabits the exact root or the complete
`ExoticWitnessPackage`.

The standard-sphere shortcut was rejected by a fresh trust-zero check:
`Diffeomorph.refl` inhabits the standard sphere's self-diffeomorphism type, so
that type cannot be `IsEmpty`. Supplying a different smooth atlas together
with the required emptiness certificate is exactly the missing exotic-smooth-
structure theorem, not an encoding shortcut.

The repository base advanced after the prior `443b8bbc` recheck and integrated
that blocker packet. A whitelist diff shows no change to the canonical
statement, conditional composition, frozen registry and graphs, anchor ledger,
validation specs, Lean toolchain, or dependency manifest. The mathematical
blocker therefore persists at this base.

Closing the route requires placeholder-free Lean implementations of the Milnor
sphere-bundle construction and conventions, its homotopy/topological sphere
identification, and distinguishing smooth-invariant computations plus
invariance strong enough to derive `IsEmpty Diffeomorph`. Assuming any missing
package, crediting `proof_wanted`, or returning only the conditional composer
would be a placeholder or substituted theorem and was not done.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink points at shared canonical artifacts. This
run issued no `lake update`, `lake build`, dependency clone/fetch, checkout
repair, or other dependency-mutation command, and made no network request.
Lean outputs were confined to disposable `/tmp` directories and removed.

The shared `flt-regular` dependency checkout has an invalid `HEAD`, so
`lake env` and `check_statement.py` fail before target elaboration. The pinned
Lean 4.29.0 executable and existing dependency oleans remain available. The
exact statement, conditional composition, and loophole probe were therefore
replayed directly against those existing oleans at trust level zero. This is
narrow blocker evidence, not a repair or release-grade reproduction.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0578` | 0 | Rank 622; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0578/check_anchor_audit.py` | 0 | Exact marker, pins, source hash, discard semantics, and M4 formalization-debt boundary passed. |
| `python3 Stage1_Instances/THM-M-0578/check_obligation_tree.py` | 0 | 13 obligations and 28 typed edges passed; denominator `67da617160dcfef6ea2eb819f105ab0e2a68a351476d55e5761d2e668e63aeda`; root remains open M4. |
| `python3 Stage1_Instances/THM-M-0578/check_statement.py` | 1 | Shared pinned artifacts failed before target elaboration because `flt-regular` cannot resolve its invalid `HEAD`; no repair or fetch was attempted. |
| direct pinned-Lean trust-zero replay | 0 | Exact statement and conditional composition elaborated; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| trust-zero standard-sphere/name probe | 0 | `Diffeomorph.refl` refuted emptiness for the standard witness with only the three expected axioms; the discarded marker name was unknown. |
| scoped retained-body/prerequisite search | 0 | 11 relevant Lean files were duplicate/conditional statements, metadata/audit material, or the discarded marker; no eligible terminal body was found. |
| local mathlib `master` and all-ref history inspection | 0 | `master` still uses `proof_wanted`; history contains only introduction commit `041fe1fa487`. |
| forbidden-construct scan of owned Lean files | 1 | Expected no-match exit; no prohibited proof escape was found. |
| scoped `git diff --name-status 443b8bbc..HEAD` | 0 | Empty for all proof-input files and Lean pins; the whole-target delta contains only the prior blocker packet. |
| `python3 -m json.tool` on the companion record | 0 | The current-base blocker record is valid JSON. |
| target-local tracked and added-file `git diff --check` | 0 | No whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest is absent because the proof phase is incomplete. |

## Exact recipes

The direct kernel replay used the pinned executable and existing olean closure:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-0578-proof-e08cfa3f-slot63.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0578/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0578/ObligationTree.lean "$tmp/ObligationTree.lean"
lean="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
lean_path="$root/Formalizations/Lean/.lake/build/lib/lean"
for d in "$root"/Formalizations/Lean/.lake/packages/*/.lake/build/lib/lean; do
  if [ -d "$d" ]; then lean_path="$lean_path:$d"; fi
done
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600s \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 600s \
  "$lean" --trust=0 -t0 -R "$tmp" "$tmp/ObligationTree.lean"
```

The successful loophole/name probe imported the same pinned Poincare module and
used this disposable Lean source with the same direct executable, `LEAN_PATH`,
trust level, timeout, and cleanup pattern:

```lean
import Mathlib.Geometry.Manifold.PoincareConjecture

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
```

The source, escape, and base-delta checks were:

```bash
rg -l -i --glob '*.lean' '(MilnorExoticSphereTarget|exists_homeomorph_isEmpty_diffeomorph_sphere_seven|ExoticWitnessPackage|ExoticSevenSphereExists|Milnor.{0,40}sphere|exotic.{0,40}(7.?sphere|seven.?sphere)|Eells.?Kuiper|Kervaire.?Milnor|sphere.{0,30}bundle.{0,30}sphere)' Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages
rg -n '\b(sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(axiom|constant|opaque|unsafe|extern|external)([[:space:]]|$)' Stage1_Instances/THM-M-0578 --glob '*.lean'
git diff --name-status 443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b..HEAD -- Stage1_Instances/THM-M-0578/Statement.lean Stage1_Instances/THM-M-0578/ObligationTree.lean Stage1_Instances/THM-M-0578/obligation-registry.json Stage1_Instances/THM-M-0578/typed-graphs.json Stage1_Instances/THM-M-0578/anchor-audit.json Stage1_Instances/THM-M-0578/validation-specs.json Stage1_Instances/THM-M-0578/statement.json Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json
```

## Retry boundary

Retry after placeholder-free implementations exist for `M0578-C-BUNDLE`,
`M0578-T-HOMEO`, and `M0578-O-NONDIFF` with their frozen child obligations.
Alternatively, integrate an immutable compatible Lean 4 declaration of the
exact root with a complete dependency lock, license record, and terminal-body
provenance. Separately restore the scheduler-provided pinned `flt-regular`
checkout before requiring `lake env` replay.

This is a current-base nonrelease blocker record. It is not a proof receipt,
does not satisfy `S56-M-0578-PROOF`, proposes no state change, and supports
neither root closure nor theorem completion. Because the assigned proof phase
is incomplete, `.stage1-worker-selftest.json` is intentionally absent.
