# THM-M-0578 proof-phase recheck at base b62c08f2 (slot46)

Item: `S56-M-0578-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `b62c08f262435e44a30ad3fc88a4712e3954afc7`

Base tree: `f7374dcf5690374a2e9e5d13ac124b34c7ecfab1`

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
trust-zero import probe reports the name as unknown. The checked-out mathlib
source still contains the same marker, and all-ref history finds only its
introduction commit `041fe1fa487`, not a proof-bearing replacement.

A current scoped Lean-source search found 11 relevant files. They are this
dossier, `THM-M-0605`'s duplicate statement and conditional assembly, legacy
metadata or audit files, one neighboring statement probe, and mathlib's
discarded marker. No declaration inhabits the exact root or complete
`ExoticWitnessPackage`. Mathlib's bordism module also records bordisms and
bordism groups as future work.

The standard-sphere shortcut was rejected by a trust-zero theorem:
`Diffeomorph.refl` inhabits the standard sphere's self-diffeomorphism type, so
that type cannot be `IsEmpty`. Supplying a different atlas together with the
required emptiness certificate would be the missing exotic-smooth-structure
theorem, not a definitional shortcut.

The repository base advanced after the prior `ab6974ae` recheck by integrating
that blocker packet. A proof-input whitelist diff is empty and all frozen
source hashes are unchanged. The mathematical blocker therefore persists at
this base.

Closing the route requires placeholder-free Lean implementations of the
Milnor sphere-bundle construction and boundary conventions, its homeomorphism
to the fixed unit seven-sphere, and distinguishing smooth-invariant
computations with invariance strong enough to derive `IsEmpty Diffeomorph`.
Assuming a missing package, crediting `proof_wanted`, or returning only the
conditional composer would violate the exact theorem boundary and was not
done. The obligation registry already splits these missing packages; they need
dedicated proof work rather than another root-level substitution.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink points at shared canonical pinned
artifacts. It was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, checkout repair, network request, or dependency mutation command
was issued. Lean outputs were confined to disposable `/tmp` directories and
removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0578` | 0 | Rank 622; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0578/check_statement.py` | 0 | Exact target elaborated; all four structural mutations were distinguished; expression digest `c9d29902...d32c`. |
| `python3 Stage1_Instances/THM-M-0578/check_anchor_audit.py` | 0 | Exact marker and discard semantics passed at the pins; root remains M4 formalization debt. |
| `python3 Stage1_Instances/THM-M-0578/check_obligation_tree.py` | 0 | 13 obligations and 28 typed edges passed; denominator `67da617160dcfef6ea2eb819f105ab0e2a68a351476d55e5761d2e668e63aeda`; root remains open M4. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| isolated trust-zero `lake env` replay below | 0 | Exact statement and conditional composition elaborated; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound`; disposable statement olean SHA-256 was `83dcfaec38f0d842614531d19db521eb5f8496fa2d891fe59c6e2fc189d3d3a7`. |
| direct trust-zero probe of the source marker name | 1 | Expected negative evidence: `Unknown identifier exists_homeomorph_isEmpty_diffeomorph_sphere_seven`; its enclosing recipe checked the status and diagnostic, then exited 0. |
| direct trust-zero standard-sphere loophole check | 0 | `Diffeomorph.refl` refutes `IsEmpty` for the standard witness; the theorem reported only the same three foundation axioms. |
| scoped retained-body search | 0 | 11 relevant Lean files were duplicate or conditional statements, legacy or audit material, or the discarded marker; no eligible terminal body was found. |
| pinned marker, current source, history, and bordism inspection | 0 | Pinned and current sources use `proof_wanted`; history contains only introduction commit `041fe1fa487`; bordism groups remain future work. |
| forbidden-construct scan of owned Lean files | 1 | Expected no-match exit; no prohibited proof escape was found. |
| scoped `git diff --name-status ab6974ae..HEAD` | 0 | Empty for all proof-input files, target manifest, skill, and Lean pins; the whole-target delta contains only the prior blocker packet. |
| `python3 -m json.tool` on the companion record | 0 | Current-base blocker record is valid JSON. |
| added-file and target-local `git diff --check` recipes | 0 | No whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest is absent because the proof phase is incomplete. |

## Exact Recipes

The isolated kernel replay used the pinned executable and existing olean
closure:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-0578-proof-b62c08f2-slot46.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0578/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0578/ObligationTree.lean "$tmp/ObligationTree.lean"
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 600s \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 600s \
  "$lean" --trust=0 -t0 -R "$tmp" "$tmp/ObligationTree.lean"
```

The expected-negative declaration probe imported the same pinned Poincare
module and checked the source-only name with that executable, `LEAN_PATH`,
trust level, timeout, and cleanup pattern. It exited 1 with `Unknown
identifier`; the enclosing shell recipe verified both the status and exact
diagnostic before exiting 0.

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
provenance, and composition checks.

This is a current-base nonrelease blocker record. It is not a proof receipt,
does not satisfy `S56-M-0578-PROOF`, proposes no state change, and supports
neither root closure nor theorem completion. Because the assigned proof phase
is incomplete, `.stage1-worker-selftest.json` is intentionally absent.
