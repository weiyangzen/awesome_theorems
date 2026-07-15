# THM-M-1122 proof-phase recheck at current base

Item: `S56-M-1122-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `46320e01d1897482417e7b0d03a15a5b77ae5275`

Base tree: `2260ad94d18a6662ffc00f47b8955ae3a2a18184`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target uniformly over its
explicit parameters. The existing placeholder-free declaration

```text
Stage1Instances.THM_M_1122.proofPhaseCountermodel :
  Not (SchrammLoewnerEvolutionTarget
    (Measure.dirac ()) (Measure.dirac false) True
    (fun _ : Unit => true)
    (fun _ : Bool -> Real -> Unit => True)
    (fun _ : NegativeTime -> Unit => fun _ : Bool => True))
```

kernel-checks at trust level zero against a freshly elaborated `Statement.olean`.

The target leaves `lerwScalingLimit` arbitrary and represents circle Brownian motion and the radial
Loewner solution by arbitrary predicates. The countermodel makes both predicates true, takes the
Brownian-side curve to be the identity on `Bool`, and takes the alleged LERW limit to be constantly
`true` on `Unit`. Under Dirac measures at `false` and `()`,
`IdentDistrib.measure_preimage_eq` for the measurable singleton `{true}` would equate measures zero
and one.

This refutes the frozen Lean encoding, not Schramm's mathematical theorem. Repairing or
strengthening the target in this proof item would be a forbidden theorem substitution. The checked
declaration `root_of_conditionalIdentification` also supplies no root proof credit: its extra
`ConditionalIdentification` premise is definitionally the substantive conclusion being sought.

The assigned item remains `[ ]`. No positive proof receipt, state transition, audit completion,
theorem completion, validation completion, release, or master-acceptance claim is made. Because the
requested proof phase is not genuinely complete, `.stage1-worker-selftest.json` is deliberately
absent.

## Failed Gate And Retry

The first semantic failure is `S56-5.1-EXACT-TARGET-CONSISTENCY / M1122-S-INTERFACES`: the frozen
opaque predicates permit the checked finite countermodel. The remaining frozen proof cut is
`M1122-L-IDENTIFICATION`, and the root remains open. The authoritative prerequisite
`S56-M-1122-OBLIGATION_TREE` also remains worker-provisional `[_]`, not master-accepted `[x]`.

Retry only after reopening `S56-M-1122-STATEMENT`, replacing the opaque interfaces with fixed,
source-faithful definitions and sufficient noncircular hypotheses, accepting a new statement
fingerprint, and freezing a new obligation-registry version. The statement, anchor-audit, and
obligation-tree phases must then be rerun before positive proof execution resumes. Alternatively,
redirect the work explicitly to the checked counterexample target.

The dossier has pre-existing projection inconsistencies that this proof-only worker did not alter:
`instance.json` reports root `M4` while the frozen registry validator reports `M3`, and
`task-dag.json` retains stale intake-era task prose. Those inconsistencies provide no proof credit.

## Validation

All checks ran in this worker clone using the existing symlink to canonical pinned Lake artifacts.
No `lake update`, `lake build`, dependency clone/fetch, network action, checkout, or `.lake`
mutation was performed. Lean output was confined to a fresh directory under `/tmp` and removed.
The pre-existing untracked `.lake` symlink makes this nonrelease evidence.

The requested top-level pinned environment is currently incomplete: `(cd Formalizations/Lean &&
lake env lean --version)` exits `1` before Lean because the pinned `flt-regular` checkout cannot
resolve `HEAD`. This worker recorded that missing artifact rather than repairing or fetching it. The
narrow diagnostic therefore invoked `lake env lean` from the pinned mathlib package and supplied
only already-built, read-only dependency paths from the same canonical `.lake`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1122` | 0 | Rank 562; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1122/check_obligation_tree.py` | 0 | 11 obligations and 19 typed edges passed; denominator `1d0de239...863fd`; root open at `M3`, `ConditionalIdentification` at `M4`. |
| `(cd Formalizations/Lean && timeout --foreground 180 lake env lean --version)` | 1 | Pinned `flt-regular` could not resolve `HEAD`; top-level pinned Lake validation did not reach Lean. |
| Narrow trust-zero `lake env lean` recipe below | 0 | The exact statement, conditional composition, and concrete negation elaborated. Checked theorems report only `[propext, Classical.choice, Quot.sound]`; Lean emitted one non-failing `unnecessarySimpa` warning. |
| Scoped prohibited-declaration scan | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, `native_decide`, bodyless declaration, unsafe/oracle escape, `implemented_by`, or `extern` occurs in the checked Lean sources. |
| `(cd Formalizations/Lean/.lake/packages/mathlib && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Pinned mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `python3 -m json.tool ...head-46320e01-slot50.json` | 0 | Structured current-base blocker packet parsed successfully. |
| Current-base blocker invariant assertions | 0 | Item/base/tree identity, hashes, open state, empty receipts, false completion flags, changed paths, and self-test absence agree. |
| Scoped tracked and no-index new-file `git diff --check` wrapper | 0 | No whitespace diagnostics; both new files had the expected different-file status. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion self-test manifest for the blocked phase. |

The narrow diagnostic recipe, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-1122
tmp=$(mktemp -d /tmp/s56m1122-46320e01-slot50.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$target/ObligationTree.lean" \
  "$target/ProofCountermodel.lean" "$tmp/"
mathlib="$repo/Formalizations/Lean/.lake/packages/mathlib"
base_path=$(cd "$mathlib" && timeout --foreground 600 lake env printenv LEAN_PATH)
for package in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible; do
  base_path="$repo/Formalizations/Lean/.lake/packages/$package/.lake/build/lib/lean:$base_path"
done
cd "$mathlib"
LEAN_PATH="$base_path" LEAN_NUM_THREADS=1 timeout --foreground 600 \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
LEAN_PATH="$tmp:$base_path" LEAN_NUM_THREADS=1 timeout --foreground 600 \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean"
LEAN_PATH="$tmp:$base_path" LEAN_NUM_THREADS=1 timeout --foreground 600 \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/ProofCountermodel.olean" \
  "$tmp/ProofCountermodel.lean"
sha256sum "$tmp/Statement.olean" "$tmp/ObligationTree.olean" \
  "$tmp/ProofCountermodel.olean"
```

Replay-stable output hashes were:

| Output | SHA-256 |
|---|---|
| `Statement.olean` | `88f36fe6436c03754a145ec6c4958e668428a969a6ac2c5d9b30af2240fc6578` |
| `ObligationTree.olean` | `9ee3f8cf2221d4dc1a245ce4fa7fa5fa4920cb22629b31c1ba9bf477320c5c06` |
| `ProofCountermodel.olean` | `435977135a1829aa059464bcfc2711b5b16d5e9ca962020234eca099bba99b9d` |

The checked source SHA-256 values are:

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `8f6087a0c3bcf79a73348ccf978fd4761406bbe8314113b4f3b1a309f7591057` |
| `ObligationTree.lean` | `55e2616243844c3fbc8bb453bf1dc007e2deaa9ef129872c4fc9dfe97545e7a1` |
| `ProofCountermodel.lean` | `8d0c657c535ce046881b9fee5af80785dc79ac4c4275af19bb15a3673167dd1f` |
| `obligation-registry.json` | `9bd28d167236090c1acf756f0c877c52c8095245626bc89ef55a070b338af300` |
| `typed-graphs.json` | `e9da2608d87b3315438d2eca842453c82ca717cedc5ee7aadecdf7f04814d0be` |
| `anchor-audit.json` | `f6dfa8a45faa5f5631500d5356c0b8c31624e5d1c28cb33f5ed8c4cf9d5309bb` |
| `validation-specs.json` | `b87288aa846f365fdf0141a1baae6e91881fe34becb16d403bc898ec4532adde` |
| `Formalizations/Lean/lake-manifest.json` | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `Formalizations/Lean/lean-toolchain` | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` |

This is durable current-base blocker evidence, not a proof receipt.
