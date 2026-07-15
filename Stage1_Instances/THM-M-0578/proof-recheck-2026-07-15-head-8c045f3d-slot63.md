# THM-M-0578 proof-phase recheck at base 8c045f3d (slot63)

Item: `S56-M-0578-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `8c045f3d21e3e747c39dd266f581367b08bddd8b`

Base tree: `9910c8170c82875bd17db434d6a9dbf3ac340d94`

## Verdict

`blocked`. The exact frozen target
`Stage1Instances.THM_M_0578.MilnorExoticSphereTarget` still has no eligible
terminal Lean 4 proof body in the repository or pinned dependency closure. No
proof body was added. The proof item stays `[ ]`, the root vector stays
`[H3, M4, R4]`, and root closure, audit completion, validation, release, and
theorem completion remain false.

The frozen immediate root cut set is unchanged:

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
`withoutModifyingEnv`, then discards the environment change. It leaves no
declaration or proof body to import. Fresh scoped searches found no retained
Milnor-sphere, exotic-sphere, Eells-Kuiper, Kervaire-Milnor, or equivalent
proof body. `THM-M-0605` duplicates the statement and conditional witness
assembly only. No eligible candidate was found in these audited scoped
searches. Mathlib's bordism module still describes bordisms and bordism groups
as future work.

No encoding shortcut closes the target. The standard unit seven-sphere has
`Diffeomorph.refl`, contradicting the required `IsEmpty`. Transporting its
standard smooth structure along a homeomorphism likewise supplies a
diffeomorphism. Providing a different atlas together with the emptiness
certificate is precisely the missing exotic-smooth-structure theorem.

The repository base changed after the prior `557b928b` recheck and integrated
that packet. A whitelist diff and exact hashes show no change to the statement,
composition interface, frozen registry and graphs, anchor ledger, validation
specs, Lean toolchain, or dependency manifest. This packet rebinds the blocker
analysis to the current base rather than treating stale-base evidence as fresh.

Closing the route requires a genuine formalization of the Milnor sphere-bundle
construction and conventions, a homotopy-sphere calculation and topological
identification, and distinguishing smooth-invariant computations with
invariance strong enough to derive `IsEmpty Diffeomorph`. Assuming those
packages, crediting `proof_wanted`, or returning only the conditional composer
would be a placeholder or substituted theorem and was not done.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused
read-only. Lean outputs were confined to disposable paths and removed. No
`lake update`, `lake build`, dependency clone/fetch, network request, or
`.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0578` | 0 | Rank 622; planned lifecycle; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0578/check_statement.py` | 0 | Exact target elaborated; all four structural mutations were distinguished; expression digest `c9d29902...d32c`. |
| `python3 Stage1_Instances/THM-M-0578/check_anchor_audit.py` | 0 | Exact marker, pins, source hash, discard semantics, and M4 formalization-debt boundary passed. |
| `python3 Stage1_Instances/THM-M-0578/check_obligation_tree.py` | 0 | 13 obligations and 28 typed edges passed; denominator `67da617160dcfef6ea2eb819f105ab0e2a68a351476d55e5761d2e668e63aeda`; root remains open M4. |
| isolated trust-zero `lake env lean` replay | 0 | Exact statement and conditional composition elaborated; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| trust-zero standard-sphere/name probe | 0 | `Diffeomorph.refl` refutes emptiness for the standard witness with only the three expected axioms; the discarded marker is absent after import. |
| scoped retained-body and prerequisite searches | 0 | The 31 named-source hits were duplicate statements/conditional assemblies, metadata, prose, or the discarded marker; no eligible candidate was found in this audited scoped search. |
| forbidden-construct scan of owned Lean files | 1 | Expected no-match exit; no prohibited proof escape was found. |
| scoped `git diff --name-status 557b928b..HEAD` | 0 | Empty for all THM-M-0578 proof-input files and Lean pins; the target-local delta added only the prior blocker packet. |
| `python3 -m json.tool Stage1_Instances/THM-M-0578/proof-recheck-2026-07-15-head-8c045f3d-slot63.json` | 0 | Current-base blocker record is valid JSON. |
| owned-path and added-file `git diff --check` recipes | 0 | No whitespace diagnostic; expected added-file difference statuses were handled by the wrapper. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Incomplete proof phase emitted no completion manifest. |

The completed kernel evidence is a fresh isolated trust-zero replay bound to
the unchanged current input hashes: copied `Statement.lean` compiled to a
disposable `Statement.olean`, and copied `ObligationTree.lean` elaborated with
that directory prepended to the pinned `LEAN_PATH`. A separate fresh trust-zero
probe rejected the standard-sphere loophole and confirmed that the discarded
marker is absent. The aggregate statement/mutation script also completed and
distinguished all four frozen structural mutations.

The JSON companion records the literal one-line forms of the replay and
whitespace-check wrappers. The loophole probe is recorded as a complete
disposable-file recipe because its multi-line Lean source is part of the
result description rather than a retained proof input.

## Exact Recipes

The fresh trust-zero replay was run from the repository root as follows:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0578-proof-8c045f3d-slot63.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0578/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0578/ObligationTree.lean "$tmp/ObligationTree.lean"
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600s \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 600s \
  "$lean" --trust=0 -t0 -R "$tmp" "$tmp/ObligationTree.lean"
```

The successful loophole/name probe used this disposable Lean source with the
same pinned executable, `LEAN_PATH`, trust level, timeout, and cleanup pattern:

```lean
import Mathlib.Geometry.Manifold.PoincareConjecture
open scoped Manifold ContDiff
open Metric (sphere)
noncomputable section

theorem standardSphereSelfDiffeomorphNotEmpty : ¬ IsEmpty
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

The exact source, escape, and base-delta checks were:

```bash
rg -n -i '(MilnorExoticSphereTarget|exists_homeomorph_isEmpty_diffeomorph_sphere_seven|ExoticWitnessPackage|ExoticSevenSphereExists|Milnor.{0,40}sphere|exotic.{0,40}(7.?sphere|seven.?sphere)|Eells.?Kuiper|Kervaire.?Milnor|sphere.{0,30}bundle.{0,30}sphere)' Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages --glob '*.lean'
rg -n '\b(sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(axiom|constant|opaque|unsafe|external)([[:space:]]|$)' Stage1_Instances/THM-M-0578 --glob '*.lean'
git diff --name-status 557b928b377b386864527c9fb4831d45857837aa..HEAD -- Stage1_Instances/THM-M-0578/Statement.lean Stage1_Instances/THM-M-0578/ObligationTree.lean Stage1_Instances/THM-M-0578/obligation-registry.json Stage1_Instances/THM-M-0578/typed-graphs.json Stage1_Instances/THM-M-0578/anchor-audit.json Stage1_Instances/THM-M-0578/validation-specs.json Stage1_Instances/THM-M-0578/statement.json Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json
```

## Retry Condition

Resume after placeholder-free implementations of `M0578-C-BUNDLE`,
`M0578-T-HOMEO`, and `M0578-O-NONDIFF` with their frozen child obligations.
Alternatively, integrate an immutable compatible Lean 4 proof-bearing
declaration of the exact root with a complete dependency lock and license, then
rerun the exact-type, trust, provenance, and composition checks.

This is blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0578-PROOF`, proposes no state promotion, and supports neither root
closure nor theorem completion. Because the assigned phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` remains absent.
