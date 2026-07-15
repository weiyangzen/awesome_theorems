# THM-M-1058 proof-phase recheck at `6bf9ee93`: blocked

Item: `S56-M-1058-PROOF`

Recheck date: 2026-07-16 (Asia/Shanghai)

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Base tree: `24acf86e69ab2e6fca9480c6269b6429874ba295`

Lifecycle: `planned -> planned`

## Dependency Preflight

The v2 node has no direct hard parent, transitive hard ancestor, incoming hard
edge, reuse hint, or shared group. The mandatory target-owned
`dependency-reuse-ledger.json` records that empty audited closure under schema
`stage1-dependency-reuse-ledger/1.1`, graph digest
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`,
and dependency-context digest
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
The repository validator accepted the ledger with zero inspections, zero reuse
decisions, and zero unresolved compatibility obligations.

## Verdict

`blocked`. The exact frozen expression `LargeDeviationPrinciple E D` is a
property of supplied data `D`, not a closed theorem. `LargeDeviationData`
provides probability measures, a positive speed tending to infinity, and a
nonnegative lower-semicontinuous rate. Those fields imply neither the
all-closed-set upper bound nor the all-open-set lower bound.

The tracked placeholder-free `Proof.lean` gives a kernel-checked
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

The remaining root cut set is `M1058-UPPER` and `M1058-LOWER`. The historical
repo-local wrapper assumes those same bounds and merely forms their
conjunction, so it is circular as a terminal candidate. A bounded search of
the existing pinned package sources found no exact terminal LDP body; the
nearby Cramer surface is a different open target.

No positive proof body or receipt was added, no obligation closed, and the
item remains `[ ]` at `[H1, M3, R3]`. Its obligation-tree prerequisite is
only provisional `[_]`. This is the forty-ninth proof-recheck record of the
same mathematical impasse. Since the assigned proof phase is not complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed proof gate is `M1058-UPPER`: the frozen input supplies
neither a concrete probability model nor hypotheses implying the closed-set
upper bound. `M1058-LOWER` is independently open.

Resume positive proof work only after an authorized statement repair binds
the target to specified data with substantive source-faithful hypotheses and
publishes a new accepted statement fingerprint and obligation registry. The
other legal route is an immutable exact compatible Lean 4 terminal proof that
can be pinned and checked. Adding the desired bounds as assumptions would
recreate the circular wrapper.

The same condition has exceeded five unresolved proof ticks. This worker
cannot modify the execution DAG, so the master should stop unchanged proof
dispatches and authorize statement repair or another dependency-legal
restructuring.

## Validation

Checks ran in this worker clone against the already provisioned pinned Lake
artifacts. No `lake update`, `lake build`, dependency clone/fetch, checkout,
or other `.lake` mutation was run. Temporary Lean sources and outputs were
created under `/tmp` and removed. The automation-provided untracked `.lake`
symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD; git rev-parse HEAD^{tree}` | 0 | Base commit `6bf9ee93a322e7d25cf9249226222095f95d1cff`; tree `24acf86e69ab2e6fca9480c6269b6429874ba295`. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed; all are L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1058` | 0 | Rank 250; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| Repository `validate_dependency_reuse_ledger` call | 0 | The schema-1.1 ledger passed with zero required inspections, reuse decisions, and unresolved compatibility obligations. |
| `python3 -m json.tool Stage1_Instances/THM-M-1058/dependency-reuse-ledger.json >/dev/null` | 0 | The mandatory dependency ledger is valid JSON. |
| `python3 Stage1_Instances/THM-M-1058/check_obligation_tree.py` | 0 | 16 obligations and 26 typed edges passed; denominator `603b6a62d345eb0be098c815ee9b1d743faad5f11a5c7bd503fb58a3318973f2`; root remains open M3. |
| Narrow pinned-Lean `--trust=0 -t0` recipe below | 0 | `Statement.lean` and the negative declarations in `Proof.lean` elaborated. Both negative declarations reported `[propext, Classical.choice, Quot.sound]`. Statement olean SHA-256: `2d13244d880314c945570a53549a646e7e62ef3ceaa871ce53ee22034af97d6b`; proof olean SHA-256: `523c73d38dccef8cf3778b742a328f6a1bbc32691e96506fa87e78a280db4414`; statement output SHA-256: `80b6228c91ad80643ad5da80de7cd817b1dc5f6f4f313b215147f883044e610a`; proof output SHA-256: `b8cb7767f4f4144f5897c72744ac29db8b9d9e0af1eaf6c150e4631b7b1b9701`. An independent worker replay also succeeded and reproduced the statement olean digest. |
| Bounded LDP query under `Formalizations/Lean/.lake/packages` | 1 | Expected no-match exit in the existing pinned-package Lean sources. |
| The same query under `Formalizations/Lean/AwesomeTheorems` | 0 | Seven textual matches were inspected; none supplies an exact terminal proof body. |
| Prohibited-token scan over owned Lean sources | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, `native_decide`, axiom, unsafe/external declaration, or `implemented_by`. |
| Pin revision and cleanliness checks | 0 | Mathlib is `8a178386ffc0f5fef0b77738bb5449d50efeea95`; `flt-regular` is `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`; both relevant pinned package worktrees are clean. |

The exact narrow Lean recipe was:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-1058
tmp=$(mktemp -d /tmp/thm-m-1058-slot25-6bf9ee93.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$target/Proof.lean" "$tmp/"
cd "$root/Formalizations/Lean"
base=$(timeout --foreground 120 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout --foreground 900 lake env lean --trust=0 -t0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base" timeout --foreground 900 \
  lake env lean --trust=0 -t0 --root="$tmp" \
  -o "$tmp/Proof.olean" "$tmp/Proof.lean" \
  >"$tmp/proof.out" 2>&1
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean" \
  "$tmp/statement.out" "$tmp/proof.out"
```

The exact ledger validator call was:

```bash
python3 - <<'PY'
import importlib.util
from pathlib import Path

source = Path("scripts/stage1_execution_cron.py")
spec = importlib.util.spec_from_file_location("stage1_execution_cron_local", source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.validate_dependency_reuse_ledger(
    Path("Stage1_Instances/THM-M-1058/dependency-reuse-ledger.json"),
    "THM-M-1058",
    expected_observed_graph_sha256=(
        "73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca"
    ),
    expected_repository_revision="6bf9ee93a322e7d25cf9249226222095f95d1cff",
)
PY
```

The existing proof body prints only the accepted classical dependency set:

```text
'Stage1Instances.THM_M_1058.not_largeDeviationPrinciple_counterexample'
depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1058.not_all_largeDeviationPrinciple'
depends on axioms: [propext, Classical.choice, Quot.sound]
```

These checks validate the negative nonimplication result and the blocker. They
do not turn it into a positive proof of the frozen target.
