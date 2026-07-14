# THM-M-1058 proof-phase recheck at `a1a7e939`: blocked

Item: `S56-M-1058-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`

Base tree: `d881fd9641fa3e5f3ebe5082b35672981e90adcf`

Lifecycle: `planned -> planned`

## Verdict

`blocked`. The exact frozen expression `LargeDeviationPrinciple E D` is a
property of supplied data `D`, not a closed theorem. `LargeDeviationData`
provides probability measures, a positive speed tending to infinity, and a
nonnegative lower-semicontinuous rate. Those fields imply neither the
all-closed-set upper bound nor the all-open-set lower bound.

The existing placeholder-free `Proof.lean` gives a kernel-checked
nonimplication witness. On `PUnit`, take the default probability measure,
speed `n + 1`, and constant rate `1`. The `Set.univ` upper bound would require
`0 <= -1`, and Lean checks:

```text
Stage1Instances.THM_M_1058.not_largeDeviationPrinciple_counterexample :
  Not (LargeDeviationPrinciple PUnit counterexampleData)

Stage1Instances.THM_M_1058.not_all_largeDeviationPrinciple :
  Not (forall D : LargeDeviationData PUnit,
    LargeDeviationPrinciple PUnit D)
```

This refutes only derivability from the under-specified generic data record.
It neither proves a positive LDP for specified data nor refutes a
source-faithful model-specific LDP theorem with substantive hypotheses.

The remaining root cut is `M1058-UPPER` and `M1058-LOWER`. The historical
local wrapper assumes those two bounds and projects their conjunction, so it
is circular as a terminal proof candidate. A bounded search found no exact
terminal LDP body in the pinned package sources; the nearby Cramer surface is
a different open target.

No positive proof body or receipt was added, no obligation closed, and the
item remains `[ ]` at `[H1, M3, R3]`. Since the assigned proof phase is not
complete, `.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed gate is `M1058-UPPER`: the frozen input supplies neither a
concrete probability model nor hypotheses implying the closed-set upper
bound. `M1058-LOWER` is independently open.

Resume only after an authorized statement repair binds the target to
specified data with substantive source-faithful hypotheses and publishes a
new accepted statement fingerprint and obligation registry. The other legal
route is an immutable exact compatible Lean 4 terminal proof that can be
pinned and checked. Adding the desired bounds as assumptions would only
recreate the circular wrapper.

## Validation

Checks ran in this worker clone against the already provisioned pinned Lake
artifacts. No `lake update`, `lake build`, dependency clone/fetch, or network
operation was run. Temporary Lean sources, output, and the statement olean
were created under `/tmp` and removed. The automation-provided untracked
`Formalizations/Lean/.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD^{commit} HEAD^{tree}` | 0 | Base commit `a1a7e939e58f103f5ff5d23af51437fa8658aa04`; tree `d881fd9641fa3e5f3ebe5082b35672981e90adcf`. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed; all are L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1058` | 0 | Rank 250; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1058/check_statement.py` | 0 | Expression SHA-256 `60a04b08693660e1b050384acab58541f1a768cc7dfa32da65ac587e47876a33`; all four registered mutations were killed. |
| `python3 Stage1_Instances/THM-M-1058/check_obligation_tree.py` | 0 | 16 obligations and 26 typed edges passed; denominator `603b6a62d345eb0be098c815ee9b1d743faad5f11a5c7bd503fb58a3318973f2`; root remains open M3. |
| Narrow pinned-Lean `--trust=0 -t0` recipe below | 0 | `Statement.lean` and the negative declarations in `Proof.lean` elaborated. Both negative declarations reported `[propext, Classical.choice, Quot.sound]`. Statement olean SHA-256: `2d13244d880314c945570a53549a646e7e62ef3ceaa871ce53ee22034af97d6b`; proof output SHA-256: `b8cb7767f4f4144f5897c72744ac29db8b9d9e0af1eaf6c150e4631b7b1b9701`. |
| Bounded LDP query under `Formalizations/Lean/.lake/packages` | 1 | Expected no-match exit in pinned package Lean sources. |
| The same query under `Formalizations/Lean/AwesomeTheorems` | 0 | Seven textual matches; none is an exact terminal proof body. |
| Prohibited-token scan over owned Lean sources | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, `native_decide`, axiom, unsafe/external declaration, or `implemented_by`. |
| Pin revision and cleanliness checks | 0 | Mathlib is `8a178386ffc0f5fef0b77738bb5449d50efeea95`; `flt-regular` is `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`; every pinned package worktree is clean. |
| Preliminary parallel `check_statement.py` attempt | terminated, not credited | Shared-host contention left the checker running after its launcher returned no result. Its process tree was terminated and its temporary owned source `tmpqdtuhxam.lean` was removed. The later bounded rerun above passed. |
| Delegated `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1058/Proof.lean` | 1, not credited | `import Statement` could not resolve without a temporary statement olean, so downstream names were unknown. No output file was requested. |
| Delegated isolated proof-search attempt | 130, not credited | The attempt was interrupted under host contention before statement elaboration completed. It left only an empty log under `/tmp/thm-m-1058-proof-search.3Gdv3T`; that directory was removed, and no matching process or path remained. It did not mutate the repository or pinned packages. |
| `git diff --no-index --check /dev/null <new-artifact>` for this JSON and Markdown report | 1 each | Expected new-file difference exits with no whitespace diagnostics. |
| `git diff --check -- Stage1_Instances/THM-M-1058 .stage1-worker-selftest.json` | 0 | No tracked scoped whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |
| Final `git status --short --branch` | 0 | Detached HEAD; the pre-existing untracked `.lake` symlink and only the two new owned blocker artifacts are present. |

The exact narrow Lean recipe was:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-1058
tmp=$(mktemp -d /tmp/thm-m-1058-slot36-a1a7e939.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$target/Proof.lean" "$tmp/"
cd "$root/Formalizations/Lean"
base=$(timeout 120 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout 900 lake env lean --trust=0 -t0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base" timeout 900 lake env lean \
  --trust=0 -t0 --root="$tmp" "$tmp/Proof.lean"
```

Pinned environment: Lean `4.29.0` at
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `flt-regular`
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`.

This is current-base blocker evidence, not a positive proof receipt. It does
not satisfy `S56-M-1058-PROOF`, complete the audit or theorem, or authorize
validation, release, or master acceptance.
