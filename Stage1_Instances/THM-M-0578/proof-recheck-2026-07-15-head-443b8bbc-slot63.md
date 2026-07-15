# THM-M-0578 proof-phase recheck at base 443b8bbc (slot63)

Item: `S56-M-0578-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

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
assembly only. Mathlib's bordism module still describes bordisms and bordism
groups as future work. No eligible candidate was found in these bounded
repo-local and pinned-source searches.

No encoding shortcut closes the target. The standard unit seven-sphere has
`Diffeomorph.refl`, contradicting the required `IsEmpty`. Transporting its
standard smooth structure along a homeomorphism likewise supplies a
diffeomorphism. Providing a different atlas together with the emptiness
certificate is precisely the missing exotic-smooth-structure theorem.

The repository base changed after the prior `8c045f3d` recheck and integrated
that packet. A whitelist diff and exact hashes show no change to the statement,
composition interface, frozen registry and graphs, anchor ledger, validation
specs, Lean toolchain, or dependency manifest. This packet rebinds the
mathematical blocker to the current base rather than treating stale-base
evidence as fresh.

Closing the route requires a genuine formalization of the Milnor sphere-bundle
construction and conventions, a homotopy-sphere calculation and topological
identification, and distinguishing smooth-invariant computations with
invariance strong enough to derive `IsEmpty Diffeomorph`. Assuming those
packages, crediting `proof_wanted`, or returning only the conditional composer
would be a placeholder or substituted theorem and was not done.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
request, checkout repair, or `.lake` mutation was performed. Lean outputs were
confined to disposable paths and removed.

The canonical shared `.lake/packages/flt-regular` checkout currently has
`HEAD` set to `refs/heads/.invalid`. Thus `lake env` and the existing
`check_statement.py` fail before target elaboration. The pinned Lean 4.29.0
executable and existing package oleans were available, so the exact statement,
conditional composition, and loophole probe were replayed directly at trust
zero with a `LEAN_PATH` assembled from those existing build artifacts. This is
narrow nonrelease evidence, not a repair or release-grade reproduction.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0578` | 0 | Rank 622; planned; L0/rework-required; theorem_complete=false. |
| `python3 Stage1_Instances/THM-M-0578/check_anchor_audit.py` | 0 | Exact marker, pins, source hash, discard semantics, and M4 formalization-debt boundary passed. |
| `python3 Stage1_Instances/THM-M-0578/check_obligation_tree.py` | 0 | 13 obligations and 28 typed edges passed; denominator `67da617160dcfef6ea2eb819f105ab0e2a68a351476d55e5761d2e668e63aeda`; root remains open M4. |
| `python3 Stage1_Instances/THM-M-0578/check_statement.py` | 1 | Shared canonical `.lake` dependency artifact failed before target elaboration because `flt-regular` has an invalid HEAD; no mutation or fetch was attempted. |
| direct pinned-Lean trust-zero replay | 0 | Exact statement and conditional composition elaborated from existing pinned oleans; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| trust-zero standard-sphere/name probe | 0 | `Diffeomorph.refl` refutes emptiness for the standard witness with only the three expected axioms; the discarded marker is absent after import. |
| scoped retained-body and prerequisite searches | 0 | Named-source hits were duplicate statements or conditional assemblies, metadata probes, or the discarded marker; no eligible candidate was found. |
| forbidden-construct scan of owned Lean files | 1 | Expected no-match exit; no prohibited proof escape was found. |
| scoped `git diff --name-status 8c045f3d..HEAD` | 0 | Empty for all THM-M-0578 proof-input files and Lean pins; the target-local delta added only the prior blocker packet. |
| `python3 -m json.tool` on the companion record | 0 | Current-base blocker record is valid JSON. |
| target-local tracked and added-file `git diff --check` | 0 | No whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest is absent because the proof phase is incomplete. |

The JSON companion records the exact hashes, environment identity, commands,
failure boundary, and retry condition.

## Exact recipes

The direct elaboration used the pinned executable
`$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean` (SHA-256
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`).
It assembled `LEAN_PATH` from `Formalizations/Lean/.lake/build/lib/lean` and
each existing `Formalizations/Lean/.lake/packages/*/.lake/build/lib/lean`,
copied `Statement.lean` and `ObligationTree.lean` into a fresh `/tmp` directory,
and ran:

```text
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" "$lean" --trust=0 -t0 -R "$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" "$lean" --trust=0 -t0 \
  -R "$tmp" "$tmp/ObligationTree.lean"
```

The scratch loophole probe imported the same pinned Poincare module and used:

```lean
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

```text
rg -n -i '(MilnorExoticSphereTarget|exists_homeomorph_isEmpty_diffeomorph_sphere_seven|ExoticWitnessPackage|ExoticSevenSphereExists|Milnor.{0,40}sphere|exotic.{0,40}(7.?sphere|seven.?sphere)|Eells.?Kuiper|Kervaire.?Milnor|sphere.{0,30}bundle.{0,30}sphere)' Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages --glob '*.lean'
rg -n '\b(sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(axiom|constant|opaque|unsafe|external)([[:space:]]|$)' Stage1_Instances/THM-M-0578 --glob '*.lean'
git diff --name-status 8c045f3d21e3e747c39dd266f581367b08bddd8b..HEAD -- Stage1_Instances/THM-M-0578/Statement.lean Stage1_Instances/THM-M-0578/ObligationTree.lean Stage1_Instances/THM-M-0578/obligation-registry.json Stage1_Instances/THM-M-0578/typed-graphs.json Stage1_Instances/THM-M-0578/anchor-audit.json Stage1_Instances/THM-M-0578/validation-specs.json Stage1_Instances/THM-M-0578/statement.json Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json
```

## Retry boundary

Retry when either (a) placeholder-free Lean implementations exist for the
frozen construction, boundary, topology, invariant, and obstruction packages,
or (b) an immutable, license-compatible Lean 4 proof body for the exact target
can be pinned with complete dependency and terminal-body provenance. Separately,
the scheduler-provided pinned `flt-regular` checkout must be restored before a
`lake env` replay can pass.

This artifact is a current-base nonrelease blocker record. It is not a proof
receipt, does not satisfy `S56-M-0578-PROOF`, proposes no state change, and
supports neither root closure, validation, release, audit completion, nor
theorem completion. Because the assigned proof phase is incomplete,
`.stage1-worker-selftest.json` is intentionally absent.
