# THM-M-1122 proof-phase recheck at current base

Item: `S56-M-1122-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `a4326e8ef38c6a0531f5a13052a3d4a4103de22e`

Base tree: `2ed5201ce8e2dee08900ee12b1a2a575de53fc1c`

## Verdict

`blocked`. No legal positive proof body can inhabit the universal closure of the exact frozen
target. The existing placeholder-free declaration

```text
Stage1Instances.THM_M_1122.proofPhaseCountermodel :
  Not (SchrammLoewnerEvolutionTarget
    (Measure.dirac ()) (Measure.dirac false) True
    (fun _ : Unit => true)
    (fun _ : Bool -> Real -> Unit => True)
    (fun _ : NegativeTime -> Unit => fun _ : Bool => True))
```

kernel-checks at trust level zero against a freshly elaborated `Statement.olean`. The target leaves
`lerwScalingLimit` arbitrary and represents circle Brownian motion and the radial Loewner solution
by arbitrary predicates. The countermodel makes both predicates true, takes the Brownian-side curve
to be the identity on `Bool`, and takes the alleged LERW limit to be constantly `true` on `Unit`.
Under Dirac measures at `false` and `()`, `IdentDistrib.measure_preimage_eq` for the measurable
singleton `{true}` would equate measures zero and one.

This refutes the universal closure of the abstract Lean encoding, not Schramm's mathematical
theorem and not every application of the parameterized proposition. Repairing or strengthening the
target in this proof item would be a forbidden theorem substitution. The checked declaration
`root_of_conditionalIdentification` supplies no root proof credit because its additional
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
`instance.json` reports root `M4` while the frozen registry and validator report `M3`;
`task-dag.json` retains stale intake-era task prose; and `scope-map.md` and
`source-statement-crosswalk.md` discuss a chordal-characterization route while the frozen statement
selects the radial LERW identification. Those inconsistencies provide no proof credit.

## Validation

All checks ran in this worker clone using the existing symlink to canonical pinned Lake artifacts.
No `lake update`, `lake build`, dependency clone/fetch/checkout, network action, or `.lake` mutation
was performed. Lean output was confined to a fresh directory under `/tmp` and removed. The
pre-existing untracked `.lake` symlink makes this nonrelease evidence.

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

The isolated Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-1122
tmp=$(mktemp -d /tmp/s56m1122-a4326e8-slot49.XXXXXX)
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

Replay output hashes were unchanged from the preceding pinned-base rechecks:

| Output | SHA-256 |
|---|---|
| `Statement.olean` | `88f36fe6436c03754a145ec6c4958e668428a969a6ac2c5d9b30af2240fc6578` |
| `ObligationTree.olean` | `9ee3f8cf2221d4dc1a245ce4fa7fa5fa4920cb22629b31c1ba9bf477320c5c06` |
| `ProofCountermodel.olean` | `435977135a1829aa059464bcfc2711b5b16d5e9ca962020234eca099bba99b9d` |

This is durable current-base blocker evidence, not a proof receipt.
