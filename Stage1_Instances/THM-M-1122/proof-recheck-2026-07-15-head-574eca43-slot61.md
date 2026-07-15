# THM-M-1122 proof-phase recheck at current base

Item: `S56-M-1122-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `574eca43855f5fe61884391d47d88b068e37538d`

Base tree: `652bed0686a42a63c3be4dfebc5fbe802f919c85`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target uniformly over its
explicit parameters. The target leaves `lerwScalingLimit` arbitrary and represents circle Brownian
motion and the radial Loewner solution by arbitrary predicates. The existing placeholder-free
declaration

```text
Stage1Instances.THM_M_1122.proofPhaseCountermodel :
  Not (SchrammLoewnerEvolutionTarget
    (Measure.dirac ()) (Measure.dirac false) True
    (fun _ : Unit => true)
    (fun _ : Bool -> Real -> Unit => True)
    (fun _ : NegativeTime -> Unit => fun _ : Bool => True))
```

uses the identity curve on `Bool` under `Measure.dirac false` and the constant-`true` curve on
`Unit` under `Measure.dirac ()`. Making both opaque predicates true would force
`IdentDistrib.measure_preimage_eq` to equate the measures zero and one of the measurable singleton
`{true}`. This refutes the frozen Lean encoding, not Schramm's mathematical theorem.

The checked transport `root_of_conditionalIdentification` supplies no root proof credit because
its `ConditionalIdentification` premise is definitionally the substantive conclusion being sought.
Repairing the target in this proof item would be a forbidden theorem substitution. The assigned
item therefore remains `[ ]`; no proof, state transition, audit completion, theorem completion,
validation completion, release, or master-acceptance claim is made. Because the proof phase is not
genuinely complete, `.stage1-worker-selftest.json` is deliberately absent.

## Failed Gates And Retry

The first semantic failure is `S56-M-1122-PROOF / M1122-S-INTERFACES` exact-target provability:
the opaque interfaces permit the finite Dirac countermodel. The remaining frozen proof cut is
`M1122-L-IDENTIFICATION`; the registry validator reports the root open at `M3`. The workflow
prerequisite `S56-M-1122-OBLIGATION_TREE` is also only worker-provisional `[_]`, not master-accepted
`[x]`.

The current pinned Lake closure has an independent validation blocker. The automation-provided
`.lake` symlink resolves to the canonical checkout, but package `flt-regular` has no resolvable
`HEAD` (`.git/HEAD` names `refs/heads/.invalid`). Consequently `lake env printenv LEAN_PATH` and
`lake env lean --version` fail. Per worker policy, this run did not fetch, clone, update, build,
checkout, or otherwise repair or mutate `.lake`. A direct trust-zero check using only the existing
pinned package output directories did elaborate all three local modules, but it is diagnostic only:
it does not cure the required `lake env lean` gate.

Retry proof execution only after reopening `S56-M-1122-STATEMENT`, replacing the opaque interfaces
with fixed source-faithful definitions and sufficient noncircular hypotheses, accepting a new
statement fingerprint, and freezing a new obligation-registry version. Then rerun statement,
anchor-audit, obligation-tree, and proof phases. The automation owner must separately restore the
pinned `flt-regular` checkout at manifest revision
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` before a conforming `lake env lean` replay.

## Validation

No network action or `.lake` mutation was requested or performed. Lean outputs from the diagnostic
fallback were confined to a fresh `/tmp` directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1122` | 0 | Rank 562; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1122/check_obligation_tree.py` | 0 | 11 obligations and 19 typed edges passed; denominator `1d0de239...863fd`; root open at `M3`, `ConditionalIdentification` at `M4`. |
| `(cd Formalizations/Lean && timeout --foreground 120 lake env printenv LEAN_PATH)` | 1 | `flt-regular: could not resolve 'HEAD' to a commit`; required pinned Lake validation unavailable. |
| `(cd Formalizations/Lean && timeout --foreground 120 lake env lean --version)` | 1 | Same unresolved-`HEAD` package error; Lean was not invoked by Lake. This is the required smallest real validation, not a separate prerequisite. |
| Trust-zero direct-Lean diagnostic below | 0 | Statement, conditional composition, and exact countermodel elaborated using existing pinned `.olean` directories; declarations report only `[propext, Classical.choice, Quot.sound]`; one non-failing `unnecessarySimpa` warning. |
| Scoped prohibited-declaration scan | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, `native_decide`, bodyless declaration, unsafe/oracle escape, `implemented_by`, or `extern` occurs in the checked Lean sources. |
| `/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |

The diagnostic command, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-1122
tmp=$(mktemp -d /tmp/s56m1122-574eca43-slot61.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$target/ObligationTree.lean" \
  "$target/ProofCountermodel.lean" "$tmp/"
lean_bin=/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
base_path=$(find "$repo/Formalizations/Lean/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d -print | paste -sd: -)
LEAN_PATH="$base_path" LEAN_NUM_THREADS=1 timeout --foreground 600 \
  "$lean_bin" --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
LEAN_PATH="$tmp:$base_path" LEAN_NUM_THREADS=1 timeout --foreground 600 \
  "$lean_bin" --trust=0 -t0 --root="$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean"
LEAN_PATH="$tmp:$base_path" LEAN_NUM_THREADS=1 timeout --foreground 600 \
  "$lean_bin" --trust=0 -t0 --root="$tmp" -o "$tmp/ProofCountermodel.olean" \
  "$tmp/ProofCountermodel.lean"
sha256sum "$tmp/Statement.olean" "$tmp/ObligationTree.olean" \
  "$tmp/ProofCountermodel.olean"
```

The diagnostic output hashes were:

| Output | SHA-256 |
|---|---|
| `Statement.olean` | `88f36fe6436c03754a145ec6c4958e668428a969a6ac2c5d9b30af2240fc6578` |
| `ObligationTree.olean` | `9ee3f8cf2221d4dc1a245ce4fa7fa5fa4920cb22629b31c1ba9bf477320c5c06` |
| `ProofCountermodel.olean` | `435977135a1829aa059464bcfc2711b5b16d5e9ca962020234eca099bba99b9d` |

The checked source hashes are:

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `8f6087a0c3bcf79a73348ccf978fd4761406bbe8314113b4f3b1a309f7591057` |
| `ObligationTree.lean` | `55e2616243844c3bc8bb453bf1dc007e2deaa9ef129872c4fc9dfe97545e7a1` |
| `ProofCountermodel.lean` | `8d0c657c535ce046881b9fee5af80785dc79ac4c4275af19bb15a3673167dd1f` |
| `obligation-registry.json` | `9bd28d167236090c1acf756f0c877c52c8095245626bc89ef55a070b338af300` |
| `typed-graphs.json` | `e9da2608d87b3315438d2eca842453c82ca717cedc5ee7aadecdf7f04814d0be` |
| `anchor-audit.json` | `f6dfa8a45faa5f5631500d5356c0b8c31624e5d1c28cb33f5ed8c4cf9d5309bb` |
| `validation-specs.json` | `b87288aa846f365fdf0141a1baae6e91881fe34becb16d403bc898ec4532adde` |
| `Formalizations/Lean/lake-manifest.json` | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `Formalizations/Lean/lean-toolchain` | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` |

This is durable current-base blocker evidence, not a proof receipt.
