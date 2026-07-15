# THM-M-1058 proof-phase recheck at `97cd9c49`: blocked

Item: `S56-M-1058-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `97cd9c492d95baa9b55d2d8b341844107f07e686`

Base tree: `bdd31de5f2fcd38078e4b5793b400a8105a3b8ba`

Lifecycle: `planned -> planned`

## Verdict

`blocked`. The exact frozen expression `LargeDeviationPrinciple E D` is a
property of supplied data `D`, not a closed proposition with a legal proof
body. `LargeDeviationData` supplies probability measures, a positive speed
tending to infinity, and a nonnegative lower-semicontinuous rate. These fields
imply neither the all-closed-set upper bound nor the all-open-set lower bound.

The tracked, placeholder-free `Proof.lean` gives kernel-checked evidence that
the natural universal completion is false. On `PUnit`, take the default
probability measure, speed `n + 1`, and constant rate `1`. Applying the upper
branch to `Set.univ` would require `0 <= -1`. Lean checks:

```text
Stage1Instances.THM_M_1058.not_largeDeviationPrinciple_counterexample :
  Not (LargeDeviationPrinciple PUnit counterexampleData)

Stage1Instances.THM_M_1058.not_all_largeDeviationPrinciple :
  Not (forall D : LargeDeviationData PUnit,
    LargeDeviationPrinciple PUnit D)
```

This refutes only derivability from the present generic record fields. It does
not prove a positive LDP for specified data and does not refute a
source-faithful, model-specific LDP theorem with substantive hypotheses.

The remaining root cut set is `M1058-UPPER` and `M1058-LOWER`. The historical
repo-local wrapper assumes those same two bounds and merely pairs them, so it
is circular as a terminal proof candidate. A bounded search of the existing
pinned package sources found no exact terminal LDP theorem; the nearby Cramer
surface is a distinct open target.

No positive proof body or receipt was added, no obligation closed, and the
item remains `[ ]` at `[H1, M3, R3]`. Its obligation-tree prerequisite remains
provisional `[_]`, not master-accepted `[x]`. This is the thirty-fifth tracked
proof recheck of the same mathematical impasse. Because the proof phase is not
complete, `.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed proof gate is `M1058-UPPER`: the frozen input supplies neither
a concrete probability model nor hypotheses implying the closed-set upper
bound. `M1058-LOWER` is independently open.

Resume positive proof work only after an authorized statement repair binds
the target to specified data with substantive source-faithful hypotheses and
publishes a new accepted statement fingerprint and obligation registry. The
other legal route is an immutable exact compatible Lean 4 terminal proof that
can be pinned and checked. Adding the desired bounds as assumptions would
recreate the circular wrapper.

The same blocker has exceeded the standard's five unresolved execution ticks.
This worker cannot edit the execution DAG, so the master should stop unchanged
proof dispatches and authorize statement repair or another dependency-legal
restructuring.

## Validation

Checks ran in this worker clone against the already provisioned pinned Lake
artifacts. No `lake update`, `lake build`, dependency clone/fetch, checkout, or
other `.lake` mutation was run. Temporary Lean sources and outputs were
created under `/tmp` and removed. The automation-provided untracked
`Formalizations/Lean/.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD^{commit} HEAD^{tree}` | 0 | Commit `97cd9c492d95baa9b55d2d8b341844107f07e686`; tree `bdd31de5f2fcd38078e4b5793b400a8105a3b8ba`. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed; all are L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1058` | 0 | Rank 250; lifecycle `planned`; baseline L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1058/check_statement.py` | 0 | Expression SHA-256 `60a04b08693660e1b050384acab58541f1a768cc7dfa32da65ac587e47876a33`; all four registered mutations were killed. |
| `python3 Stage1_Instances/THM-M-1058/check_obligation_tree.py` | 0 | 16 obligations and 26 typed edges passed; denominator `603b6a62d345eb0be098c815ee9b1d743faad5f11a5c7bd503fb58a3318973f2`; root remains open M3. |
| Temporary-copy `lake env lean --trust=0 -t0` recipe below | 0 | Pinned Lean 4.29.0 elaborated `Statement.lean` and `Proof.lean`. Both negative declarations use `[propext, Classical.choice, Quot.sound]`. Statement/proof olean SHA-256: `2d13244d880314c945570a53549a646e7e62ef3ceaa871ce53ee22034af97d6b` / `523c73d38dccef8cf3778b742a328f6a1bbc32691e96506fa87e78a280db4414`; statement/proof output SHA-256: `80b6228c91ad80643ad5da80de7cd817b1dc5f6f4f313b215147f883044e610a` / `b8cb7767f4f4144f5897c72744ac29db8b9d9e0af1eaf6c150e4631b7b1b9701`. |
| Bounded LDP query under `Formalizations/Lean/.lake/packages` | 1 | Expected no-match exit in the existing pinned-package Lean sources. |
| The same bounded query under `Formalizations/Lean/AwesomeTheorems` | 0 | Seven textual matches were inspected; none supplies an exact terminal proof body. |
| Prohibited-token scan over owned Lean sources | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, `native_decide`, axiom, unsafe/external declaration, or `implemented_by`. |
| Manifest revision, package HEAD/tree, package cleanliness, and tool digest checks | 0 | Lean is 4.29.0; mathlib is `8a178386ffc0f5fef0b77738bb5449d50efeea95`; `flt-regular` is `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`; both package worktrees are clean. |

The exact narrow Lean recipe was:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-1058
tmp=$(mktemp -d /tmp/thm-m-1058-slot42-97cd9c49.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$target/Proof.lean" "$tmp/"
cd "$root/Formalizations/Lean"
base=$(timeout --foreground 120 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout --foreground 900 lake env lean --trust=0 -t0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base" timeout --foreground 900 \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/Proof.olean" \
  "$tmp/Proof.lean"
```

Pinned environment: Lean `4.29.0` at
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `flt-regular`
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`.

This is current-base nonrelease blocker evidence. It does not satisfy
`S56-M-1058-PROOF`, close an obligation, propose a checklist transition, or
claim audit completion, theorem completion, validation, release, or master
acceptance.
