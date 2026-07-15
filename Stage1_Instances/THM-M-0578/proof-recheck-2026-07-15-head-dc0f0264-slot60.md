# THM-M-0578 proof-phase recheck at base dc0f0264 (slot60)

Item: `S56-M-0578-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `dc0f0264c1db312ac95025747d3212b689facb5e`

Base tree: `633bea3a2e72674768ee426a035a1850b9940ae7`

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
`M0578-C-BUNDLE`. The checked local theorem
`ObligationTree.root_of_exoticWitnessPackage` is conditional composition only:
its premise already contains the smooth manifold, homeomorphism, and
nondiffeomorphism certificate. It constructs none of the open packages and
cannot receive root proof credit.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains the exact signature only as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`.
`proof_wanted` elaborates a temporary helper axiom under
`withoutModifyingEnv` and then discards the environment change. A direct
trust-zero import probe confirms that the name is unknown. The locally present
mathlib `master` ref still contains the marker, and local all-ref history finds
only its introduction commit `041fe1fa487`, not a proof-bearing replacement.

A current scoped Lean-source search found 11 relevant files. They are confined
to this dossier, `THM-M-0605`'s duplicate statement and conditional assembly,
legacy metadata/audit files, one neighboring statement probe, and mathlib's
discarded marker. No declaration inhabits the exact root or the complete
`ExoticWitnessPackage`. Mathlib's bordism module also says bordisms and bordism
groups are future work and lists the missing core constructions as TODOs.

The standard-sphere shortcut was rejected by a fresh trust-zero theorem:
`Diffeomorph.refl` inhabits the standard sphere's self-diffeomorphism type, so
that type cannot be `IsEmpty`. Supplying a different atlas together with the
required emptiness certificate would be precisely the missing exotic smooth
structure theorem, not an encoding shortcut.

The repository base advanced after the prior `be2be0df` recheck by integrating
that blocker packet in this target. A proof-input whitelist diff is empty and
all frozen source hashes are unchanged. The mathematical blocker therefore
persists at this base.

Closing the route requires placeholder-free Lean implementations of the Milnor
sphere-bundle construction and boundary conventions, its homeomorphism to the
fixed unit seven-sphere, and distinguishing smooth-invariant computations with
invariance strong enough to derive `IsEmpty Diffeomorph`. Assuming a missing
package, crediting `proof_wanted`, or returning only the conditional composer
would violate the assigned theorem boundary and was not done.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink points at shared canonical artifacts. No
`lake update`, `lake build`, dependency clone/fetch, checkout repair, network
request, or dependency mutation command was issued. Lean outputs were confined
to disposable `/tmp` directories and removed.

The shared `flt-regular` checkout has an invalid `HEAD`, so the prescribed
`lake env lean` route and `check_statement.py` fail before target elaboration.
The pinned Lean 4.29.0 executable and existing dependency oleans remain
available. The exact statement, conditional composition, declaration-absence
probe, and standard-sphere loophole check were therefore replayed directly
against those existing artifacts at trust level zero. This is narrow
nonrelease blocker evidence, not dependency repair or release-grade replay.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0578` | 0 | Rank 622; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0578/check_anchor_audit.py` | 0 | Exact marker and discard semantics passed at the pins; root remains M4 formalization debt. |
| `python3 Stage1_Instances/THM-M-0578/check_obligation_tree.py` | 0 | 13 obligations and 28 typed edges passed; denominator `67da617160dcfef6ea2eb819f105ab0e2a68a351476d55e5761d2e668e63aeda`; root remains open M4. |
| `timeout --foreground 180s python3 Stage1_Instances/THM-M-0578/check_statement.py` | 1 | Shared `flt-regular` failed before elaboration because it cannot resolve `HEAD`; no repair or fetch was attempted. |
| `cd Formalizations/Lean && timeout --foreground 60s lake env lean --version` | 1 | The prescribed Lake route failed on the same missing `flt-regular` `HEAD` artifact before Lean ran. |
| direct pinned-Lean trust-zero replay below | 0 | Exact statement and conditional composition elaborated; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| direct trust-zero probe of the source marker name | 1 | Expected negative evidence: `Unknown identifier exists_homeomorph_isEmpty_diffeomorph_sphere_seven`. The enclosing checked recipe exited 0 after verifying that exact failure. |
| direct trust-zero standard-sphere loophole check | 0 | `Diffeomorph.refl` proves the required self-diffeomorphism type is not empty; axioms were only `propext`, `Classical.choice`, and `Quot.sound`. |
| scoped retained-body search | 0 | 11 relevant files were duplicate/conditional statements, legacy/audit material, or the discarded marker; no eligible terminal body was found. |
| pinned marker, local `master`, history, and bordism inspection | 0 | Pinned and local-master sources use `proof_wanted`; history has only introduction commit `041fe1fa487`; bordism groups remain future work. |
| forbidden-construct scan of owned Lean files | 1 | Expected no-match exit; no prohibited proof escape was found. |
| scoped `git diff --name-status be2be0df..HEAD` | 0 | Empty for all proof-input files and Lean pins; the whole-target delta contains only the prior blocker packet. |
| `python3 -m json.tool` on the companion record | 0 | The current-base blocker record is valid JSON. |
| target-local added-file `git diff --no-index --check` and final `git diff --check` | 0 | No whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest is absent because the proof phase is incomplete. |

## Exact Recipes

The direct kernel replay used only the pinned executable and existing olean
closure:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-0578-proof-dc0f0264-slot60.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0578/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0578/ObligationTree.lean "$tmp/ObligationTree.lean"
lean="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
lean_path="$root/Formalizations/Lean/.lake/build/lib/lean:$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
for d in "$root"/Formalizations/Lean/.lake/packages/*/.lake/build/lib/lean; do
  if [ -d "$d" ]; then lean_path="$lean_path:$d"; fi
done
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 600s \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 600s \
  "$lean" --trust=0 -t0 -R "$tmp" "$tmp/ObligationTree.lean"
```

The expected-negative declaration probe imported the same pinned Poincare
module and checked the source-only name with that executable, `LEAN_PATH`,
trust level, timeout, and cleanup pattern. It exited 1 with `Unknown
identifier`; the enclosing shell recipe verified that status and text before
exiting 0.

The loophole check used the same environment on this disposable theorem:

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
```

## Retry Condition

Resume after placeholder-free implementations of `M0578-C-BUNDLE`,
`M0578-T-HOMEO`, and `M0578-O-NONDIFF` with their frozen child obligations.
Alternatively, integrate an immutable compatible Lean 4 proof-bearing
declaration of the exact root with a complete dependency lock, license record,
and terminal-body provenance, then rerun node-scoped exact-type, trust,
provenance, and composition checks. Separately restore the scheduler-provided
pinned `flt-regular` checkout before requiring `lake env` replay.

This is a current-base nonrelease blocker record. It is not a proof receipt,
does not satisfy `S56-M-0578-PROOF`, proposes no state change, and supports
neither root closure nor theorem completion. Because the assigned proof phase
is incomplete, `.stage1-worker-selftest.json` is intentionally absent.
