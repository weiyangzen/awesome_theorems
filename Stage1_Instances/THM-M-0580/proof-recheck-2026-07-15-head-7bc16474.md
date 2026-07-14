# THM-M-0580 proof-phase recheck at base 7bc16474

Item: `S56-M-0580-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `7bc16474ba6a97ad369a618990b1ffbec170db3c`

Base tree: `d911a4fe236f270edbd1521a474442e0de79c6b3`

## Verdict

`blocked`. No eligible terminal Lean 4 proof body exists in the repository, pinned mathlib, or
audited external candidates for the exact proposition
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. No proof body or receipt was added. The proof
item remains `[ ]`, the root vector remains `[H2, M4, R4]`, and the audit, root, and theorem remain
incomplete.

The frozen immediate root cut set is still:

- `M0580-N-SMOOTH`, the proposed topological smoothing package;
- `M0580-T-SMOOTH-POINCARE`, the full smooth three-dimensional Poincare package.

The checked theorem `root_of_smoothing_and_smooth_poincare` assumes both packages and only composes
them into the exact root. It constructs neither. The diagnostic
`smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` goes in the converse direction, from the
root to the frozen smooth package. Using it to produce a root premise would therefore be circular.

Pinned mathlib contains the matching generalized, topological, and smooth Poincare signatures only
as `proof_wanted` markers. Importing their module retains none of the three declarations, as the
trust-zero probe confirms. A current repository and dependency search found no alternate terminal
body. The prerequisite immutable audit found only a three-dimensional statement and a
dimension-zero special-case proof.

A newly discovered external repository, `frenzymath/Poincare-Conjecture` at archive revision prefix
`6d573ad`, is also ineligible. Its Lean root imports only early blueprint chapters; later
canonical-neighborhood, surgery, extinction, and completion material is prose. Its Lean sources
contain `sorry`, no exact terminal Poincare/Perelman theorem was found, and the archive has no
license file. It was inspected as a moving external lead only; it was not fetched into `.lake`,
imported, or credited.

Two additional bounded leads also fail closed. `Spring-1211/OPenPoincare` at archive revision
prefix `36a5155` exposes a Poincare-named theorem, but its transitive classification and endgame
dependencies have literal `sorry` bodies and its toolchain is Lean 4.31.0-rc2, not the pinned
4.29.0. `gullapallirishi/RicciFlowLean` at revision prefix `17e40ed` contains only basic Ricci-flow
code with five `sorry` bodies and no Poincare target. These searches locate proof-route blueprints,
not admissible terminal proof bodies.

There is an earlier fail-closed defect in `M0580-N-SMOOTH`. Its Lean contract receives an already
selected `ChartedSpace Euclidean3 M` and requires `Nonempty (IsManifold ... infinity M)` for that
same atlas. Wrapping the proposition in `Nonempty` does not select a replacement compatible smooth
atlas. Correcting this belongs to the prerequisite obligation-tree authority and requires an
append-only graph revision carrying a new atlas, a smoothness proof, and a checked compatibility
bridge. This proof worker did not alter the frozen registry.

## Validation

All commands ran in this worker clone. Lean outputs were written only to a disposable `/tmp`
directory and removed. The automation-provided `.lake` symlink was reused read-only. No `lake
update`, `lake build`, dependency clone/fetch, or dependency mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; planned; L0/rework-required; theorem incomplete |
| isolated trust-zero `lake env lean` chain below | 0 | exact statement, conditional composition, and blocker probe elaborated; axiom reports were `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were absent |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root remains open at M4 |
| inverted forbidden-construct `rg` scan of the four owned Lean modules | 0 | no `sorry`, `admit`, `axiom`, `unsafe`, or `sorryAx` token |
| `cd Formalizations/Lean && timeout 60 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git diff --check -- Stage1_Instances/THM-M-0580` | 0 | no whitespace error |

The narrow Lean check was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot21-head7bc16474.XXXXXX)
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

The source hashes reproduced at this base are recorded in the companion JSON. The canonical `.lake`
symlink remains the only pre-existing untracked path outside this owned directory, making this
nonrelease evidence.

## Retry Condition

First return `M0580-N-SMOOTH` to the obligation-tree authority for an append-only correction. Then
implement the corrected smoothing package and complete smooth-Poincare package without placeholders.
Alternatively, integrate an immutable, licensed, compatible Lean 4 terminal proof of the exact root
with a complete dependency lock after a graph revision is accepted.

Assuming either missing package, treating `proof_wanted` as an axiom, importing placeholder-bearing
blueprint code, or presenting conditional composition as root closure would violate the exact-target
and proof-body gates. This is an owned blocker artifact, not a proof receipt; it does not satisfy
`S56-M-0580-PROOF` or support theorem completion. Because the phase is not genuinely complete,
`.stage1-worker-selftest.json` remains absent.
