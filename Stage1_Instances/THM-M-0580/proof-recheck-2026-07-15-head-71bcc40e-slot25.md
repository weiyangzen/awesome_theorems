# THM-M-0580 proof-phase recheck at base 71bcc40e (slot 25)

Item: `S56-M-0580-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `71bcc40e66b043742dafd4e66c6a868ff2b2a6ad`

Base tree: `741fca489134e06814154a72672b15212ec28c19`

## Verdict

`blocked`. The assigned proof phase is not dependency-legal and no eligible terminal Lean 4 proof
body exists in this checkout or its pinned dependency closure for the exact proposition
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. No proof body or proof receipt was added. The
item remains `[ ]`, the root vector remains `[H2, M4, R4]`, and the audit, exact root, and theorem
remain incomplete.

The task-state authority has `accepted_states: []` and records
`S56-M-0580-OBLIGATION_TREE` as open. The generated checklist's `[_]` is provisional rather than
master acceptance. Independently, the frozen immediate root cut set remains open:

- `M0580-N-SMOOTH`, the proposed topological smoothing package;
- `M0580-T-SMOOTH-POINCARE`, the proposed smooth three-dimensional Poincare package.

The checked theorem `root_of_smoothing_and_smooth_poincare` assumes both packages and only composes
them into the exact root. The diagnostic
`smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` goes from the root to the second package,
so using it to construct a root premise would be circular.

The prerequisite proof architecture also needs an append-only correction. The current
`TopologicalThreeManifoldSmoothable` receives an already selected `ChartedSpace` instance and asks
whether that same atlas is smooth; `Nonempty` around `IsManifold` does not select a compatible
replacement smooth atlas. The smooth-Poincare package then concludes the same homeomorphism as the
root under an additional `IsManifold` instance, rather than stating a distinct smooth result. The
intermediate Ricci-flow, surgery, extinction, and topology nodes have planned fingerprints rather
than exact Lean propositions and no terminal bodies. A proof worker cannot silently repair the
frozen prerequisite graph.

Pinned mathlib contains the generalized, topological, and smooth Poincare signatures only as
`proof_wanted` markers. Importing the module retains none of those constants, as the trust-zero
probe confirms. Current scoped repository searches found no alternate exact-root or cut-set
terminal body. The previously recorded bounded candidate `frenzymath/Poincare-Conjecture` contains
only early Morgan-Tian chapter formalizations, not an exact-root declaration or a compatible,
licensed proof closure. It is not an importable proof.

## Validation

All commands ran in this worker clone. Lean outputs were confined to a disposable `/tmp` directory
and removed. The automation-provided untracked `.lake` symlink was reused read-only. No `lake
update`, `lake build`, dependency clone/fetch, or dependency mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; planned; L0/rework-required; theorem incomplete |
| isolated `lake env lean --trust=0` chain below | 0 | statement, conditional composition, and blocker probe elaborated; both local theorem axiom reports were `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were absent |
| `python3 Stage1_Instances/THM-M-0580/check_statement.py` | 0 | expression hash `938ef54298273a011a66395812b53e6bf8071b0925b84cd94ae5fb4f9a6eb664`; all four statement mutations killed; pinned toolchain and mathlib revision matched |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root open at M4 |
| scoped exact-root and cut-set declaration search | 0 | `PASS: no alternate exact-root or cut-set declaration found` |
| inverted prohibited-construct scan over the four owned Lean modules | 0 | no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` token |
| pinned Poincare-module marker search | 0 | exactly three relevant `proof_wanted` entries at lines 43, 47, and 52 |
| `cd Formalizations/Lean && timeout 60 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |

The narrow Lean check was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot25-head71bcc40e.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
paths=("$lean_root/.lake/build/lib/lean")
for p in "$lean_root"/.lake/packages/*/.lake/build/lib/lean; do paths+=("$p"); done
lean_path=$(IFS=:; printf '%s' "${paths[*]}")
cd "$target"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 -o "$tmp/ObligationTree.olean" ObligationTree.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 ProofBlockerProbe.lean
```

The canonical `.lake` symlink remains the only pre-existing untracked path outside this owned
directory, so this is nonrelease evidence.

## Retry Condition

First reconcile and master-accept the prerequisite task state. Then publish an append-only
obligation-tree revision with a compatible replacement-atlas smoothing contract, faithful smooth
theorem semantics, exact Lean targets for the proof children, checked composition, and
declaration-covering recipes. Implement those corrected packages without placeholders.
Alternatively, integrate an immutable, licensed, compatible exact-root Lean 4 proof with a complete
dependency lock and exact-type/provenance checks.

Assuming either missing package, treating `proof_wanted` as an axiom, or presenting conditional
composition as root closure would violate the exact-target and proof-body gates. This is an owned
blocker artifact, not a proof receipt; it does not satisfy `S56-M-0580-PROOF`, propose state
promotion, or support theorem completion. Because the phase is not genuinely complete,
`.stage1-worker-selftest.json` remains absent.
