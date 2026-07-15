# THM-M-1122 proof-phase current-base recheck

Item: `S56-M-1122-PROOF`. Base revision:
`f7b3c872ab727ab689486d74020c11dc5d99869f` (tree
`6c3dc9661349dd7774b23660eb9bde0212918c51`). Worker: `slot43`.

## Verdict

`blocked`. No positive proof body can truthfully inhabit the frozen target uniformly over its
explicit parameters. `ProofCountermodel.lean` remains a kernel-checked countermodel at this base:
instantiate `OmegaLERW = Unit`, `OmegaBrownian = Bool`, `Curve = Bool`, `Driver = Unit`, make both
opaque interface predicates accept every input, use the identity Boolean trace on the Brownian
side, and take the alleged LERW limit to be constantly `true`. With Dirac measures at `false` and
`()`, the target demands an `IdentDistrib` equality whose singleton-`true` preimages have measures
zero and one.

The exact target is therefore not merely missing SLE infrastructure; its opaque interfaces leave
it false for a permitted parameter instance. Adding the desired identification as a premise, as
`root_of_conditionalIdentification` does, strengthens the theorem and supplies no proof credit.
No source, wrapper, or pinned dependency in the local closure supplies the exact positive result.
Creating `sorry`, an axiom, or a broadened/substituted theorem would violate this item's gate.

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY / M1122-S-INTERFACES`. The remaining
frozen proof cut is `M1122-L-IDENTIFICATION`, and the root remains open at `M3`. The authoritative
prerequisite `S56-M-1122-OBLIGATION_TREE` is also only worker-provisional `[_]`, not master-accepted
`[x]`.

Retry only after reopening `S56-M-1122-STATEMENT`, replacing the opaque interfaces with fixed,
source-faithful definitions and sufficient noncircular hypotheses, accepting a new statement
fingerprint, and freezing a new obligation-registry version. The statement, anchor-audit, and
obligation-tree phases must then be rerun before positive proof execution resumes. Alternatively,
the scheduler may explicitly redirect execution to the checked counterexample target.

This proof-only worker did not reconcile pre-existing predecessor projections: `instance.json`
reports root `M4` while the frozen registry validator reports `M3`, and `task-dag.json` retains
intake-era open states. These inconsistencies provide no proof credit.

## Validation

All checks ran in this worker clone using the existing symlink to the canonical pinned Lake
artifacts. No `lake update`, `lake build`, dependency clone/fetch/checkout, network action, or
`.lake` mutation was performed. Lean output was confined to a fresh directory under `/tmp` and
removed. The pre-existing untracked `.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1122` | 0 | Rank 562; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1122/check_obligation_tree.py` | 0 | 11 obligations and 19 typed edges passed; denominator `1d0de239...863fd`; root open at `M3`, `ConditionalIdentification` at `M4`. |
| Isolated trust-zero `lake env lean` recipe below | 0 | The exact statement, conditional composition, and concrete negation elaborated. The checked theorems report only `[propext, Classical.choice, Quot.sound]`; Lean emitted one non-failing `unnecessarySimpa` warning. |
| Scoped prohibited-declaration scan | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, `native_decide`, bodyless declaration, unsafe/oracle escape, `implemented_by`, or `extern` occurs in the checked Lean sources. |
| `(cd Formalizations/Lean && timeout --foreground 600 lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Pinned mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD HEAD^{tree}` | 0 | Manifest-pinned commit `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`, tree `32c9eace926573a9981787ae97643e520353c893`. |
| `python3 -m json.tool ...head-f7b3c872-slot43.json` | 0 | Structured blocker packet parsed successfully. |
| Current-base blocker invariant assertions | 0 | Item/base identity, source hash, open state, empty receipts, false completion flags, changed-path inventory, and deliberate self-test absence agree. |
| Scoped tracked and no-index new-file `git diff --check` wrapper | 0 | No whitespace errors; each new file differed from `/dev/null` with expected status 1 and empty diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion self-test manifest exists for the blocked phase. |

The isolated Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-1122
tmp=$(mktemp -d /tmp/s56m1122-f7b3c872-slot43.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$target/ObligationTree.lean" \
  "$target/ProofCountermodel.lean" "$tmp/"
cd "$repo/Formalizations/Lean"
base_path=$(timeout --foreground 600 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout --foreground 600 lake env lean --trust=0 -t0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
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

This is durable current-base blocker evidence, not a proof receipt. Because the assigned phase is
not complete, `.stage1-worker-selftest.json` is deliberately absent.
