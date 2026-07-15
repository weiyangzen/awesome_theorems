# THM-M-1058 proof-phase recheck at `57fa141a`: blocked

Item: `S56-M-1058-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `57fa141a484940bb1ac5f9d098793eac5635e8ae`

Base tree: `306345ea426e418691a782c3bdae35271120e142`

Lifecycle: `planned -> planned`

## Verdict

`blocked`. The frozen expression `LargeDeviationPrinciple E D` is an open
property of supplied data `D`, not a closed positive theorem. The fields of
`LargeDeviationData` constrain the measures, speed, and rate regularity, but
they imply neither the all-closed-set upper bound nor the all-open-set lower
bound.

The tracked placeholder-free `Proof.lean` supplies kernel-checked negative
evidence. On `PUnit`, take the default probability measure, speed `n + 1`, and
constant rate `1`. The upper bound at `Set.univ` would require `0 <= -1`.
Pinned Lean checks:

```text
Stage1Instances.THM_M_1058.not_largeDeviationPrinciple_counterexample :
  Not (LargeDeviationPrinciple PUnit counterexampleData)

Stage1Instances.THM_M_1058.not_all_largeDeviationPrinciple :
  Not (forall D : LargeDeviationData PUnit,
    LargeDeviationPrinciple PUnit D)
```

This refutes uniform derivability from the frozen data interface. It does not
prove a positive LDP for specified data, and it does not refute any
model-specific LDP theorem with substantive hypotheses. The historical local
wrapper assumes the same upper and lower bounds and merely forms their
conjunction, so it is circular as a terminal proof candidate. A bounded search
of the existing pinned package sources found no exact terminal LDP theorem.

The root remains `M3`; the cut set is `M1058-UPPER` and `M1058-LOWER`. No
positive proof body, composition certificate, obligation closure, or receipt
was added. The prerequisite obligation-tree item is provisional `[_]`, not
master-accepted `[x]`. This is the forty-seventh tracked proof recheck of the
same impasse, well beyond the five-tick restructuring threshold. Because the
assigned proof phase is not complete, `.stage1-worker-selftest.json` remains
absent.

Resume positive proof work only after an authorized statement repair selects
specified data with source-faithful hypotheses and publishes a new accepted
statement fingerprint and obligation registry, or after an immutable exact
compatible Lean 4 proof becomes available to pin and check. Adding the desired
bounds as assumptions is not a terminal proof.

## Validation

Checks ran in this worker clone against the already provisioned pinned Lake
artifacts. No `lake update`, `lake build`, dependency clone/fetch/checkout, or
other `.lake` mutation was run. Temporary elaboration outputs were written
under `/tmp` and removed. The automation-provided untracked `.lake` symlink
makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}` | 0 | Commit `57fa141a484940bb1ac5f9d098793eac5635e8ae`; tree `306345ea426e418691a782c3bdae35271120e142`. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed; all are L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1058` | 0 | Rank 250; lifecycle `planned`; baseline L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout --foreground 900 python3 Stage1_Instances/THM-M-1058/check_statement.py` | 0 | Expression SHA-256 `60a04b08693660e1b050384acab58541f1a768cc7dfa32da65ac587e47876a33`; all four registered mutations were killed. |
| `python3 Stage1_Instances/THM-M-1058/check_obligation_tree.py` | 0 | 16 obligations and 26 typed edges passed; denominator `603b6a62d345eb0be098c815ee9b1d743faad5f11a5c7bd503fb58a3318973f2`; root remains open M3. |
| Narrow pinned-Lean `--trust=0 -t0` recipe below | 0 | `Statement.lean` and both negative declarations in `Proof.lean` elaborated. The negative declarations reported `[propext, Classical.choice, Quot.sound]`. Statement/proof olean SHA-256: `2d13244d880314c945570a53549a646e7e62ef3ceaa871ce53ee22034af97d6b` / `523c73d38dccef8cf3778b742a328f6a1bbc32691e96506fa87e78a280db4414`; output SHA-256: `80b6228c91ad80643ad5da80de7cd817b1dc5f6f4f313b215147f883044e610a` / `b8cb7767f4f4144f5897c72744ac29db8b9d9e0af1eaf6c150e4631b7b1b9701`. |
| Bounded LDP query under `Formalizations/Lean/.lake/packages` | 1 | Expected no-match exit; zero existing pinned-package Lean source matches. |
| The same query under `Formalizations/Lean/AwesomeTheorems` | 0 | Seven textual matches were inspected; none supplies an exact terminal proof body. |
| Prohibited-token scan over owned Lean sources | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, `native_decide`, axiom, unsafe/external declaration, or `implemented_by`. |
| Pin revision, cleanliness, and tool digest checks | 0 | Lean is 4.29.0; mathlib is `8a178386ffc0f5fef0b77738bb5449d50efeea95`; `flt-regular` is `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`; both package worktrees are clean. |
| Post-write JSON, blocker-invariant, whitespace, and self-test-absence checks | 0 | Both blocker artifacts are well-formed; the state remains `[ ]`, no positive proof or root closure is claimed, touched files have no whitespace errors, and `.stage1-worker-selftest.json` is absent. |

The exact narrow Lean recipe was:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-1058
tmp=$(mktemp -d /tmp/thm-m-1058-slot20-57fa141a.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$target/Proof.lean" "$tmp/"
cd "$root/Formalizations/Lean"
base=$(timeout --foreground 120 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout --foreground 900 lake env lean --trust=0 -t0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base" timeout --foreground 900 \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/Proof.olean" \
  "$tmp/Proof.lean" >"$tmp/proof.out" 2>&1
cat "$tmp/statement.out" "$tmp/proof.out"
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean" \
  "$tmp/statement.out" "$tmp/proof.out"
```

Pinned environment: Lean 4.29.0 at
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `flt-regular`
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. Network was not used.

## Status Boundary

This is current-base nonrelease blocker and negative kernel evidence only. It
does not satisfy `S56-M-1058-PROOF`, close an obligation, propose a state
transition, or claim audit completion, theorem completion, validation,
release, or master acceptance. There are no accepted receipt IDs.
