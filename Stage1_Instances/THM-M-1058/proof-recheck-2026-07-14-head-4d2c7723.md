# THM-M-1058 proof-phase recheck at `4d2c7723`: blocked

Item: `S56-M-1058-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `4d2c77230343716176b4192dc38e26f4c20c7547`

Base tree: `9eebdfdfda6b289fea0b6e778fae8e13327395b2`

Lifecycle: `planned -> planned`

## Verdict

`blocked`. This run first fails worker evidence integrity. The initial
`check_statement.py` / top-level `lake env` invocation automatically began
materializing the absent manifest-pinned `flt-regular` dependency through the
worker symlink into the shared canonical `.lake`, leaving an incomplete
checkout. A later diagnostic `lake env` probe from `/tmp` also automatically
began cloning mathlib there before timing out; its partial temporary directory
was removed. Both automatic operations violate the no-clone/no-fetch rule, so
none of this run can be accepted as pinned worker evidence.

The mathematical target is independently blocked. The frozen canonical expression is the predicate
`LargeDeviationPrinciple E D` for supplied data `D`; it is not a closed
universally valid theorem. `LargeDeviationData` supplies probability measures,
a positive speed tending to infinity, and a nonnegative lower-semicontinuous
rate. These fields provide neither a concrete probabilistic model nor
hypotheses from which either large-deviation inequality follows.

The tracked placeholder-free `Proof.lean` makes the nonimplication
kernel-visible. It constructs data on `PUnit` with the default probability
measure, speed `n + 1`, and constant rate `1`, and proves:

```text
Stage1Instances.THM_M_1058.not_largeDeviationPrinciple_counterexample :
  Not (LargeDeviationPrinciple PUnit counterexampleData)

Stage1Instances.THM_M_1058.not_all_largeDeviationPrinciple :
  Not (forall D : LargeDeviationData PUnit,
    LargeDeviationPrinciple PUnit D)
```

On `Set.univ`, the scaled log probability is zero while the negated rate
infimum is negative one. This rules out treating the current record fields as
a generic LDP theorem. It neither proves a positive LDP for specified data nor
refutes a model-specific theorem with substantive analytic hypotheses.

The frozen root cut therefore remains `M1058-UPPER` and `M1058-LOWER`. The
historical repository wrapper assumes those exact branches and projects their
conjunction, so it is circular as a terminal candidate. A bounded query found
no matching terminal source in the existing pinned package trees. The local
Cramer surface is a different target whose analytic packages remain open.

The automation-provided `.lake` points to a concurrently shared cache. Another
process later materialized the pinned `flt-regular` checkout, after which a
target recipe stalled in `lake env which lean` and was terminated. Narrow
elaboration using the absolute pinned Lean binary and existing compiled paths
succeeded, but cannot repair the earlier procedural violations.

No positive proof body or receipt was added, no obligation was closed, and the
proof item remains `[ ]` at `[H1, M3, R3]`. Because the assigned phase is not
complete, `.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failure is worker evidence integrity because prohibited automatic
dependency operations occurred. The first mathematical failure is
`M1058-UPPER`: the frozen input contains
neither a concrete family nor assumptions implying the all-closed-set upper
bound. `M1058-LOWER` is independently open, so both nodes remain the root cut.
The validation surface additionally lacks a stable Lake replay because its
shared cache changed during the run.

First rerun in a fresh immutable worker cache in which every manifest-pinned
dependency is already complete and no concurrent process changes or locks it;
do not invoke Lake when a required artifact is absent.
Mathematical execution can then resume only
after an authorized statement repair binds the target to specified data with
substantive source-faithful hypotheses and publishes a new accepted statement
fingerprint and obligation registry. The other legal route is to pin and check
an immutable exact compatible Lean 4 proof. Adding the upper and lower bounds
as assumptions merely recreates the circular historical wrapper.

## Validation

Checks ran in this worker clone. No explicit `lake update` or `lake build` was
run, but the Lake invocations automatically began the prohibited dependency
operations described above. Results are retained for transparency, not
credited as compliant worker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD` and `git rev-parse HEAD^{tree}` | 0 | Base `4d2c77230343716176b4192dc38e26f4c20c7547`; tree `9eebdfdfda6b289fea0b6e778fae8e13327395b2`. |
| `git status --short` | 0 | Only `?? Formalizations/Lean/.lake` was present at preflight. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed; all are L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1058` | 0 | Rank 250; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1058/check_statement.py` | no shell exit returned | Its top-level `lake env` automatically began materializing absent `flt-regular` in the shared cache and left an incomplete checkout. The checker was terminated and removed its temporary owned source. |
| `python3 Stage1_Instances/THM-M-1058/check_obligation_tree.py` | 0 | 16 obligations and 26 typed edges passed; denominator `603b6a62d345eb0be098c815ee9b1d743faad5f11a5c7bd503fb58a3318973f2`; root remains open M3. |
| `cd Formalizations/Lean && lake env lean --version` | 1, then 0 after external cache change | The initial Lake activity began materializing absent `flt-regular`; the incomplete checkout later could not resolve `HEAD`. Another process subsequently materialized the pinned revision. A later target recipe stalled in `lake env which lean` and was terminated. |
| Diagnostic `lake env lean --version` from `/tmp` | no shell exit returned | It automatically began cloning mathlib under `/tmp` before timing out. The partial temporary directory was removed; this is a prohibited dependency operation, not evidence. |
| Direct absolute-Lean `--trust=0 -t 0` elaboration with existing compiled dependency paths | 0 | Exact statement and both negative declarations elaborated; axiom reports were `[propext, Classical.choice, Quot.sound]`. Statement olean SHA-256 `2d13244d880314c945570a53549a646e7e62ef3ceaa871ce53ee22034af97d6b`; proof output SHA-256 `b8cb7767f4f4144f5897c72744ac29db8b9d9e0af1eaf6c150e4631b7b1b9701`. This cannot count as compliant pinned worker evidence. |
| `rg -l -i --glob '*.lean' 'LargeDeviationPrinciple\|LargeDeviation\|large deviation\|large-deviation\|LDPUpperBound\|LDPLowerBound\|LaplacePrinciple\|Sanov\|GartnerEllis\|Gärtner.?Ellis\|Varadhan' Formalizations/Lean/.lake/packages` | 1 | Expected no-match exit in the existing pinned package sources. |
| The same bounded query under `Formalizations/Lean/AwesomeTheorems` | 0 | Seven textual hits; none is an exact terminal proof body. |
| `rg -n -i --glob '*.lean' '\b(sorry\|admit\|sorryAx\|native_decide)\b\|^[[:space:]]*(axiom\|unsafe\|external)[[:space:]]\|implemented_by' Stage1_Instances/THM-M-1058` | 1 | Expected no-match exit: no prohibited proof boundary in owned Lean sources. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1058/proof-recheck-2026-07-14-head-4d2c7723.json >/dev/null` | 0 | The structured blocker artifact is valid JSON. |
| Semantic `jq -e` check of item, theorem, state, verdict, cut set, and completion flags | 0 | Identity and blocked-state boundaries agree. |
| `git diff --no-index --check /dev/null` against each new artifact | 1 each | Expected new-file difference exits with no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The direct elaboration used
`/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean` with
`--trust=0 -t 0`, a temporary `Statement.olean`, and a `LEAN_PATH` assembled
only from existing `*/.lake/build/lib/lean` directories plus the pinned
toolchain library. It performed no dependency operation.

Exact direct recipe from the repository root (`tmp` was a fresh `/tmp`
directory and was removed after hashing its outputs):

```bash
base=$(find -L Formalizations/Lean/.lake/packages \
  -path '*/.lake/build/lib/lean' -type d -print | sort | paste -sd:)
base="$base:$PWD/Formalizations/Lean/.lake/build/lib/lean:/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
LEAN_PATH="$base" \
  /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
  --trust=0 -t0 --root="$PWD" -o "$tmp/Statement.olean" \
  Stage1_Instances/THM-M-1058/Statement.lean
LEAN_PATH="$tmp:$base" \
  /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
  --trust=0 -t0 --root="$PWD" \
  Stage1_Instances/THM-M-1058/Proof.lean
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Current input hashes and exact
results are recorded in the adjacent JSON artifact.

This is an actionable blocker report, not valid pinned worker evidence or a
proof receipt. It does not satisfy `S56-M-1058-PROOF`, complete the audit or
theorem, or authorize validation, release, or master acceptance.
