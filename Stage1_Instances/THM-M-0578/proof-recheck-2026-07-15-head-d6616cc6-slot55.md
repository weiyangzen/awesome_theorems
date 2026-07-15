# THM-M-0578 proof-phase recheck at base d6616cc6 (slot55)

Item: `S56-M-0578-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `d6616cc60ad980c635f22ef840e9c5db2ebcab50`

Base tree: `d6f3c3aedec26191f09878fd6eb1fec666adf318`

## Verdict

`blocked`. The exact frozen target
`Stage1Instances.THM_M_0578.MilnorExoticSphereTarget` still has no eligible
terminal Lean 4 proof body in the repository or pinned dependency closure. No
root proof body was added. The proof item remains `[ ]`, the root vector
remains `[H3, M4, R4]`, and root closure, audit completion, validation,
release, and theorem completion remain false.

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
contains the exact signature only as the discarded source marker
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`. Batteries
elaborates this syntax under `withoutModifyingEnv` and removes it. The owned
trust-zero probe reports the name as unknown and absent from the imported
environment. Local history contains only its introduction commit
`041fe1fa487`, not a proof-bearing replacement.

A current-base scoped search across target instances, local formalizations,
and all 9,676 existing pinned-package Lean files found no retained declaration
inhabiting the exact target or `ExoticWitnessPackage`. `THM-M-0605` is only an
analogue: it uses analytic smoothness `omega`, not the target's infinity
smoothness, and its assembler is conditional too. No Milnor bundle, clutching,
Eells-Kuiper, Kervaire-Milnor, or comparable exotic-sphere implementation was
found. Mathlib's bordism module still leaves bordisms and bordism groups as
future work.

`ProofBlockerProbe.lean` now records two kernel-checked negative boundaries.
First, `Diffeomorph.refl` inhabits the standard sphere's infinity-smooth
self-diffeomorphism type, so the standard sphere cannot be the witness.
Second, the source marker is unavailable as a declaration after import.
Neither negative theorem constructs an exotic sphere or changes the root
machine state.

Closing the route requires placeholder-free Lean implementations of the
Milnor sphere-bundle construction and boundary conventions, its homeomorphism
to the fixed unit seven-sphere, and distinguishing smooth-invariant
computations with invariance strong enough to derive `IsEmpty Diffeomorph`.
Assuming that package, crediting the discarded marker, or returning only the
conditional composer would violate the exact theorem boundary and was not
done. This assignment has exceeded the rev-5.6 five-tick split threshold;
further meaningful execution requires dedicated child proof tasks for the
already frozen open packages.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink points at shared canonical pinned
artifacts. It was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, checkout repair, network request, or dependency mutation command
was issued. Lean outputs were confined to a disposable `/tmp` directory and
removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check && python3 scripts/stage1_target.py show THM-M-0578` | 0 | 1546 unique ranked targets passed; rank 622 is planned, L0/rework-required, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0578/check_statement.py` | 0 | Exact target elaborated; four structural mutations were distinguished; expression digest `c9d29902fc3b1bd25c4a83aa5daaa4ce201798576d7b5e16e9bbc05e76a9d32c`. |
| `python3 Stage1_Instances/THM-M-0578/check_anchor_audit.py` | 0 | Exact source marker and discard semantics passed at the pins; root remains M4 formalization debt. |
| `python3 Stage1_Instances/THM-M-0578/check_obligation_tree.py` | 0 | 13 obligations and 28 typed edges passed; denominator `67da617160dcfef6ea2eb819f105ab0e2a68a351476d55e5761d2e668e63aeda`; root remains open M4. |
| `cd Formalizations/Lean && timeout --foreground --kill-after=5s 120s lake env lean --version` plus executable digest | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; executable SHA-256 `3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`. |
| Isolated trust-zero `lake env` replay | 0 | Exact statement, conditional composition, and both blocker probes elaborated. Both checked theorems report only `propext`, `Classical.choice`, and `Quot.sound`; the discarded name reports `Unknown identifier`. Disposable `Statement.olean` SHA-256 was `83dcfaec38f0d842614531d19db521eb5f8496fa2d891fe59c6e2fc189d3d3a7`. |
| Scoped retained-body/prerequisite searches | 0 / 1 | The broad search found 33 statement, conditional, metadata, marker, or negative-probe lines in 12 files; the pinned prerequisite search had the expected no-match exit. No eligible terminal body was found. |
| Pinned marker/history/bordism inspection | 0 | The marker is discarded; history contains only introduction commit `041fe1fa487`; bordisms and bordism groups remain future work. |
| Forbidden-construct scan of `ProofBlockerProbe.lean` | 1 | Expected no-match exit; no prohibited proof escape was found. |
| Scoped diff from `3862149a` | 0 | No canonical statement, composition, registry, graph, audit input, validation spec, target manifest, toolchain, or dependency pin changed. |
| `python3 -m json.tool` on the paired record | 0 | The current-base blocker record is valid JSON. |
| Added-file and final target-local `git diff --check` | 0 | Expected added-file difference statuses, no whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest is absent because the proof phase is incomplete. |

## Exact Recipe

The isolated kernel replay used the pinned Lake environment:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0578-proof-d6616cc6-slot55.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0578/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0578/ObligationTree.lean "$tmp/ObligationTree.lean"
cp Stage1_Instances/THM-M-0578/ProofBlockerProbe.lean "$tmp/ProofBlockerProbe.lean"
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout --foreground --kill-after=5s 600s \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground --kill-after=5s 600s \
  "$lean" --trust=0 -t0 -R "$tmp" "$tmp/ObligationTree.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout --foreground --kill-after=5s 600s \
  "$lean" --trust=0 -t0 -R "$tmp" "$tmp/ProofBlockerProbe.lean"
```

## Retry Condition

Resume after placeholder-free implementations of `M0578-C-BUNDLE`,
`M0578-T-HOMEO`, and `M0578-O-NONDIFF` with their frozen child obligations.
Alternatively, integrate an immutable compatible Lean 4 proof-bearing
declaration of the exact root with a complete dependency lock, license record,
and terminal-body provenance, then rerun node-scoped exact-type, trust,
provenance, and composition checks.

This is current-base nonrelease blocker evidence. It is not a proof receipt,
does not satisfy `S56-M-0578-PROOF`, proposes no state change, and supports
neither root closure nor theorem completion. Because the assigned proof phase
is incomplete, `.stage1-worker-selftest.json` is intentionally absent.
