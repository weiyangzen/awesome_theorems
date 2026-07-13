# THM-M-1058 proof-phase recheck at `f510617d`: blocked

Item: `S56-M-1058-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `f510617dd7a5509521db0a7ee0e5080a341b0a49`

Base tree: `eeb5ae2931cc805f85de886f026ff61b02e28521`

Lifecycle: `planned -> planned`

## Verdict

`blocked`. This run first fails worker evidence integrity: a delegated
`lake env` validation attempt found the manifest-pinned `flt-regular`
dependency absent, automatically cloned it, and checked out pinned revision
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` through the worker symlink into the
shared canonical `.lake`. That mutation violates the task constraint and makes
this run invalid as pinned worker evidence. It was not reverted.

The mathematical target is independently blocked. The frozen canonical Lean expression is the predicate
`LargeDeviationPrinciple E D` for supplied data `D`; it is not a closed theorem
until data are fixed or binders are added. `LargeDeviationData` provides
probability measures, a positive speed tending to infinity, and a nonnegative
lower-semicontinuous rate. Those fields provide neither a concrete model nor
hypotheses from which either LDP inequality follows.

The tracked placeholder-free `Proof.lean` makes this nonimplication
kernel-visible. It constructs data on `PUnit` with the default probability
measure, speed `n + 1`, and constant rate `1`, then checks:

```text
Stage1Instances.THM_M_1058.not_largeDeviationPrinciple_counterexample :
  Not (LargeDeviationPrinciple PUnit counterexampleData)

Stage1Instances.THM_M_1058.not_all_largeDeviationPrinciple :
  Not (forall D : LargeDeviationData PUnit,
    LargeDeviationPrinciple PUnit D)
```

On `Set.univ`, the scaled log probability is zero while the negated rate
infimum is negative one. The current record fields therefore cannot entail an
LDP uniformly. This neither proves a positive LDP for specified data nor
refutes a source-faithful large-deviation theorem with substantive
model-specific hypotheses.

The frozen root cut remains `M1058-UPPER` and `M1058-LOWER`. The historical
repository wrapper assumes those exact branches and projects their conjunction,
so it is circular as a terminal candidate. A bounded query found no matching
terminal source in the pinned Lake packages; this is scoped negative evidence,
not an exhaustive discovery claim. The local Cramer surface is a different
target whose analytic packages remain open.

No positive proof body or receipt was added, no obligation was closed, and the
proof item remains `[ ]` at `[H1, M3, R3]`. Because the assigned proof phase is
not complete, `.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed gate for this run is worker evidence integrity because the
shared `.lake` was mutated. The mathematical gate then fails at `M1058-UPPER`:
the frozen input has neither a concrete family nor assumptions implying the
all-closed-set upper bound. `M1058-LOWER` is independently open, so both nodes
remain the root cut.

First rerun in a fresh worker environment with an already provisioned pinned
cache that remains unmodified. Mathematical execution can resume only after an
authorized statement repair binds the target to specified
data with substantive source-faithful hypotheses and publishes a new accepted
statement fingerprint and obligation registry. The other legal route is to pin
and check an immutable exact compatible Lean 4 proof. Adding the desired bounds
as assumptions would only recreate the circular historical wrapper.

## Validation

Checks ran in this worker clone. Some checks below completed before the
delegated mutation was disclosed; their outputs are retained for transparency,
not credited as compliant worker evidence. A delegated `lake env` attempt automatically
performed the prohibited pinned dependency clone described above. Subsequent
narrow elaboration used the absolute pinned Lean binary and explicit dependency
paths, with temporary Lean objects and logs under `/tmp`; its mathematical
result is reported transparently but cannot repair the procedural failure.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD` and `git rev-parse HEAD^{tree}` | 0 | Base `f510617dd7a5509521db0a7ee0e5080a341b0a49`; tree `eeb5ae2931cc805f85de886f026ff61b02e28521`. |
| `git status --short` | 0 | Only `?? Formalizations/Lean/.lake` was present at preflight. |
| Delegated `lake env` attempt while `flt-regular` was absent | stopped after automatic materialization | Prohibited mutation: Lake cloned `https://github.com/leanprover-community/flt-regular.git` and checked out manifest-pinned revision `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` in the shared canonical `.lake`; reflog records clone and checkout at 2026-07-14 02:53:44 +0800. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed; all are L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1058` | 0 | Rank 250; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1058/check_statement.py` | 0 | Expression SHA-256 `60a04b08693660e1b050384acab58541f1a768cc7dfa32da65ac587e47876a33`; all four statement mutations were killed. |
| `python3 Stage1_Instances/THM-M-1058/check_obligation_tree.py` | 0 | 16 obligations and 26 typed edges passed; denominator `603b6a62d345eb0be098c815ee9b1d743faad5f11a5c7bd503fb58a3318973f2`; root remains open M3. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1058/AnchorAudit.lean` | 0 | Probability-measure, limsup/liminf, lower-semicontinuity, and extended-log probes elaborated. |
| Direct absolute-Lean `--trust=0 -t 0` elaboration with explicit dependency paths | 0 | After the mutation, the exact statement and both negative declarations elaborated; axiom reports were exactly `[propext, Classical.choice, Quot.sound]`. Statement olean SHA-256 `2d13244d880314c945570a53549a646e7e62ef3ceaa871ce53ee22034af97d6b`; proof output SHA-256 `b8cb7767f4f4144f5897c72744ac29db8b9d9e0af1eaf6c150e4631b7b1b9701`. This cannot count as compliant worker evidence. |
| `rg -l -i --glob '*.lean' 'LargeDeviationPrinciple\|LargeDeviation\|large deviation\|large-deviation\|LDPUpperBound\|LDPLowerBound\|LaplacePrinciple\|Sanov\|GartnerEllis\|Gärtner.?Ellis\|Varadhan' Formalizations/Lean/.lake/packages` | 1 | Expected no-match exit in pinned package sources. |
| The same bounded query under `Formalizations/Lean/AwesomeTheorems` | 0 | Seven textual hits; the historical wrapper and open Cramer surface are nonterminal, and the rest are unrelated or excluded. |
| `rg -n -i --glob '*.lean' '\b(sorry\|admit\|sorryAx\|native_decide)\b\|^[[:space:]]*(axiom\|unsafe\|external)[[:space:]]\|implemented_by' Stage1_Instances/THM-M-1058` | 1 | Expected no-match exit: no prohibited proof boundary in owned Lean sources. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The successful follow-up invoked
`/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean` directly
with `--trust=0 -t0`, a temporary `Statement.olean`, and this explicit base
`LEAN_PATH` (line-broken here for readability):

```text
/home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake/packages/Cli/.lake/build/lib/lean:
/home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake/packages/batteries/.lake/build/lib/lean:
/home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake/packages/Qq/.lake/build/lib/lean:
/home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake/packages/aesop/.lake/build/lib/lean:
/home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake/packages/proofwidgets/.lake/build/lib/lean:
/home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake/packages/importGraph/.lake/build/lib/lean:
/home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake/packages/LeanSearchClient/.lake/build/lib/lean:
/home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake/packages/plausible/.lake/build/lib/lean:
/home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake/packages/checkdecls/.lake/build/lib/lean:
/home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake/packages/mathlib/.lake/build/lib/lean:
/home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake/packages/flt-regular/.lake/build/lib/lean:
/home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake/build/lib/lean:
/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean
```

The exact direct commands were:

```bash
cd /home/sansha-2/external/awesome_theorems/.cron/stage1-rev56/workers/slot44/Stage1_Instances/THM-M-1058
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE" timeout 300 \
  /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
  --trust=0 -t0 -R "$PWD" -o /tmp/m1058-direct.1GNJzd/Statement.olean \
  Statement.lean >/tmp/m1058-direct.1GNJzd/statement.log 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="/tmp/m1058-direct.1GNJzd:$BASE" timeout 300 \
  /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
  --trust=0 -t0 -R "$PWD" Proof.lean \
  >/tmp/m1058-direct.1GNJzd/proof.log 2>&1
```

Here `BASE` denotes the single colon-joined path printed above. The temporary
directory was removed after recording its hashes. The direct commands did not
invoke Lake, but they ran after the prohibited dependency materialization and
cannot turn the run into valid pinned worker evidence.

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Current input hashes and exact
results are recorded in the adjacent JSON artifact.

This is an actionable blocker report, not valid pinned worker evidence or a
proof receipt. It does not satisfy `S56-M-1058-PROOF`, complete the audit or
theorem, or authorize validation, release, or master acceptance.
