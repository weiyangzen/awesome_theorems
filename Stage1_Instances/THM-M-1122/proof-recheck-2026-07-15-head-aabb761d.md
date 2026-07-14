# THM-M-1122 proof-phase recheck at current base

Item: `S56-M-1122-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `aabb761d975829b09920d981edc8220edb90e8c3`

Base tree: `a988020866eb03a08cd23d18d5e7711cb5d03742`

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
`true` on `Unit`. Under Dirac measures at `false` and `()`, `IdentDistrib.measure_preimage_eq` for
the measurable singleton `{true}` would equate measures zero and one.

This refutes the frozen Lean encoding, not Schramm's mathematical theorem. Repairing or strengthening
the target in this proof item would be a forbidden theorem substitution. The checked declaration
`root_of_conditionalIdentification` also supplies no root proof credit: its extra
`ConditionalIdentification` premise is definitionally the substantive conclusion being sought.

The assigned item remains `[ ]`. No positive proof receipt, state transition, audit completion,
theorem completion, validation completion, release, or master-acceptance claim is made. Because the
requested proof phase is not genuinely complete, `.stage1-worker-selftest.json` is deliberately
absent.

## Failed Gate And Retry

The first failed semantic gate is `S56-5.1-EXACT-TARGET-CONSISTENCY /
M1122-S-INTERFACES`. The frozen opaque interfaces permit the checked finite countermodel. The
remaining frozen proof cut is `M1122-L-IDENTIFICATION`, and the root remains open at `M3`. The
authoritative prerequisite `S56-M-1122-OBLIGATION_TREE` also remains worker-provisional `[_]`, not
master-accepted `[x]`.

Retry only after reopening `S56-M-1122-STATEMENT`, replacing the opaque interfaces with fixed,
source-faithful definitions and sufficient noncircular hypotheses, accepting a new statement
fingerprint, and freezing a new obligation-registry version. The statement, anchor-audit, and
obligation-tree phases must then be rerun before positive proof execution resumes. Alternatively,
redirect the work explicitly to the checked counterexample target.

The dossier has pre-existing projection inconsistencies that this proof-only worker did not alter:
`instance.json` reports root `M4` while the frozen registry and validator report `M3`, and
`task-dag.json` retains stale intake-era task prose. Those inconsistencies provide no proof credit.

## Validation

All checks ran in this worker clone using the existing symlink to the canonical pinned Lake
artifacts. No `lake update`, `lake build`, dependency clone/fetch, network action, or `.lake`
mutation was performed. Lean output was confined to a fresh directory under `/tmp` and removed.
The pre-existing untracked `.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1122` | 0 | Rank 562; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1122/check_obligation_tree.py` | 0 | 11 obligations and 19 typed edges passed; denominator `1d0de239...863fd`; root open at `M3`, `ConditionalIdentification` at `M4`. |
| Isolated trust-zero `lake env lean` recipe below | 0 | The exact statement, conditional composition, and concrete negation elaborated. The two checked theorems report only `[propext, Classical.choice, Quot.sound]`; Lean emitted one non-failing `unnecessarySimpa` warning. |
| Scoped prohibited-declaration scan | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, `native_decide`, bodyless declaration, unsafe/oracle escape, `implemented_by`, or `extern` occurs in the three checked Lean sources. |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1122/proof-recheck-2026-07-15-head-aabb761d.json` | 0 | Structured blocker packet parsed successfully. |
| Current-base blocker invariant assertions | 0 | Item/base identity, source hashes, kernel result, empty receipt lists, false completion flags, and deliberate self-test absence agree. |
| Scoped whitespace-check wrapper | 0 | Tracked `git diff --check` exited 0. Each new-file `git diff --no-index --check` exited 1, the expected different-file status, with empty diagnostic output. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No worker-completion manifest for the blocked phase. |

The isolated Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-1122
tmp=$(mktemp -d /tmp/s56m1122-aabb761d-capture.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$target/ObligationTree.lean" \
  "$target/ProofCountermodel.lean" "$tmp/"
cd "$repo/Formalizations/Lean"
base_path=$(timeout --foreground 600 lake env printenv LEAN_PATH)
lean_bin=$(timeout --foreground 600 lake env which lean)
LEAN_NUM_THREADS=1 LEAN_PATH="$base_path" timeout --foreground 600 \
  "$lean_bin" --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean" >"$tmp/kernel-output.txt" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" timeout --foreground 600 \
  "$lean_bin" --trust=0 -t0 --root="$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean" >>"$tmp/kernel-output.txt" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" timeout --foreground 600 \
  "$lean_bin" --trust=0 -t0 --root="$tmp" "$tmp/ProofCountermodel.lean" \
  >>"$tmp/kernel-output.txt" 2>&1
cat "$tmp/kernel-output.txt"
sha256sum "$tmp/kernel-output.txt" "$tmp/Statement.olean" \
  "$tmp/ObligationTree.olean"
```

It produced SHA-256 values `376843e93e4a23a60acfba9116f56f7b42726cc690a909a1383b81631e986103`
for the combined kernel output, `88f36fe6436c03754a145ec6c4958e668428a969a6ac2c5d9b30af2240fc6578`
for `Statement.olean`, and `9ee3f8cf2221d4dc1a245ce4fa7fa5fa4920cb22629b31c1ba9bf477320c5c06`
for `ObligationTree.olean`.

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
