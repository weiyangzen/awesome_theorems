# THM-M-0578 proof-phase recheck at base ab6974ae (slot54)

Item: `S56-M-0578-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `ab6974ae3bcabe677e7138ff057a7c005aac12d4`

Base tree: `c640af240d44f02c83a29dfa2f985f601a0dfcc2`

## Verdict

`blocked`. The exact frozen proposition
`Stage1Instances.THM_M_0578.MilnorExoticSphereTarget` still has no eligible
terminal Lean 4 proof body in the repository or pinned dependency closure. No
proof body was added. The proof item remains `[ ]`, the root vector remains
`[H3, M4, R4]`, and root closure, validation, release, audit completion, and
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
cannot receive root proof credit.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains the exact signature only as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`.
`proof_wanted` does not retain a declaration in the environment. A fresh
trust-zero import probe reports the name as unknown. The local mathlib
`master` ref still contains the marker, and all-ref history finds only its
introduction commit `041fe1fa487`, not a proof-bearing replacement.

A current scoped Lean-source search found 11 relevant files. They are this
dossier, `THM-M-0605`'s duplicate statement and conditional assembly, legacy
metadata/audit files, one neighboring statement probe, and mathlib's discarded
marker. No declaration inhabits the exact root or complete
`ExoticWitnessPackage`. Mathlib's bordism module also records bordisms and
bordism groups as future work.

The standard-sphere shortcut was rejected by a trust-zero theorem:
`Diffeomorph.refl` inhabits the standard sphere's self-diffeomorphism type, so
that type cannot be `IsEmpty`. Supplying a different atlas together with the
required emptiness certificate would be the missing exotic-smooth-structure
theorem, not a definitional shortcut.

The repository base advanced after the prior `dc0f0264` recheck by integrating
that blocker packet. A proof-input whitelist diff is empty and all frozen
source hashes are unchanged. The mathematical blocker therefore persists.

Closing the route requires placeholder-free Lean implementations of the
Milnor sphere-bundle construction and boundary conventions, its homeomorphism
to the fixed unit seven-sphere, and distinguishing smooth-invariant
computations with invariance strong enough to derive `IsEmpty Diffeomorph`.
Assuming a missing package, crediting `proof_wanted`, or returning only the
conditional composer would violate the exact theorem boundary and was not
done. The obligation registry has already split this work; after repeated
unresolved proof ticks, the master lane should schedule its open child
obligations rather than repeatedly treating the root cut as one task.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink points at shared canonical artifacts. No
`lake update`, `lake build`, dependency clone/fetch, checkout repair, network
request, or dependency mutation command was issued. Lean outputs were confined
to disposable `/tmp` directories and removed.

The shared `flt-regular` checkout cannot resolve `HEAD`, and a bounded
prescribed `lake env lean --version` preflight timed out after 30 seconds with
no output. The pinned Lean 4.29.0 executable and existing dependency oleans
remain available. The exact statement, conditional composition,
declaration-absence probe, and standard-sphere loophole check were therefore
replayed directly against those artifacts at trust level zero. This is narrow
nonrelease blocker evidence, not dependency repair or release-grade replay.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0578` | 0 | Rank 622; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0578/check_anchor_audit.py` | 0 | Exact marker and discard semantics passed at the pins; root remains M4 formalization debt. |
| `python3 Stage1_Instances/THM-M-0578/check_obligation_tree.py` | 0 | 13 obligations and 28 typed edges passed; denominator `67da617160dcfef6ea2eb819f105ab0e2a68a351476d55e5761d2e668e63aeda`; root remains open M4. |
| bounded `cd Formalizations/Lean && lake env lean --version` | 124 | Timed out after 30 seconds with no output; the shared `flt-regular` checkout independently failed to resolve `HEAD`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 128 | `fatal: ambiguous argument 'HEAD'`; the shared dependency checkout has no resolvable `HEAD`. |
| direct pinned-Lean trust-zero replay below | 0 | Exact statement and conditional composition elaborated; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound`; disposable statement olean SHA-256 was `83dcfaec38f0d842614531d19db521eb5f8496fa2d891fe59c6e2fc189d3d3a7`. |
| direct trust-zero probe of the source marker name | 1 | Expected negative evidence: `Unknown identifier exists_homeomorph_isEmpty_diffeomorph_sphere_seven`; the enclosing recipe verified the failure and exited 0. |
| direct trust-zero standard-sphere loophole check | 0 | `Diffeomorph.refl` refutes emptiness for the standard witness; axioms were the same three expected foundation axioms. |
| scoped retained-body search | 0 | 11 relevant files were duplicate/conditional statements, legacy/audit material, or the discarded marker; no eligible terminal body was found. |
| pinned marker, local `master`, history, and bordism inspection | 0 | Pinned and local-master sources use `proof_wanted`; history has only introduction commit `041fe1fa487`; bordism groups remain future work. |
| forbidden-construct scan of owned Lean files | 1 | Expected no-match exit; no prohibited proof escape was found. |
| scoped `git diff --name-status dc0f0264..HEAD` | 0 | Empty for all proof-input files, target manifest, and Lean pins; the whole-target delta contains only the prior blocker packet. |
| `python3 -m json.tool` on the companion record | 0 | The current-base blocker record is valid JSON. |
| added-file `git diff --no-index --check` and final target-local `git diff --check` | 0 | No whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest is absent because the proof phase is incomplete. |

## Exact Recipes

The direct kernel replay used only the pinned executable and existing olean
closure:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-0578-proof-ab6974ae-slot54.XXXXXX)
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
