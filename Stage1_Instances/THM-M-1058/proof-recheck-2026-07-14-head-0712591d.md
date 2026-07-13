# THM-M-1058 proof-phase recheck at `0712591d`: blocked

Item: `S56-M-1058-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `0712591ddaea6a40a0dc6482670e6129e727f5df`

Base tree: `03a643bf6bd4f35f0d1d6c036afab8b41aa88401`

Lifecycle: `planned -> planned`

## Verdict

`blocked`. The frozen canonical expression is the predicate
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

No positive proof body or receipt was added, no obligation was closed, and the
proof item remains `[ ]` at `[H1, M3, R3]`. Because the assigned phase is not
complete, `.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first mathematical failure is `M1058-UPPER`: the frozen input contains
neither a concrete family nor assumptions implying the all-closed-set upper
bound. `M1058-LOWER` is independently open, so both nodes remain the root cut.

Execution can resume only after an authorized statement repair binds the
target to specified data with substantive source-faithful hypotheses and
publishes a new accepted statement fingerprint and obligation registry. The
other legal route is to pin and check an immutable exact compatible Lean 4
proof. Adding the upper and lower bounds as assumptions merely recreates the
circular historical wrapper.

## Validation

Checks ran in this worker clone against the already provisioned pinned cache.
No `lake update`, `lake build`, dependency clone/fetch, network operation, or
`.lake` content mutation was performed. A preliminary `lake env lean` attempt
failed before elaboration because the target source was outside Lake's root.
For the successful check, `lake env` was used only to resolve the pinned
executable and its existing `LEAN_PATH`; the actual two-step elaboration
invoked the resolved Lean executable directly. A digest over all regular
`.lake` file paths and bytes was identical before and after that successful
check.
Concurrent workers did update shared-cache metadata timestamps during the run,
so this remains nonrelease blocker evidence rather than hermetic release
evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD` and `git rev-parse HEAD^{tree}` | 0 | Base `0712591ddaea6a40a0dc6482670e6129e727f5df`; tree `03a643bf6bd4f35f0d1d6c036afab8b41aa88401`. |
| `git status --short` | 0 | Only `?? Formalizations/Lean/.lake` was present at preflight. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed; all are L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1058` | 0 | Rank 250; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1058/check_obligation_tree.py` | 0 | 16 obligations and 26 typed edges passed; denominator `603b6a62d345eb0be098c815ee9b1d743faad5f11a5c7bd503fb58a3318973f2`; root remains open M3. |
| `cd Formalizations/Lean && lake env lean --trust=0 -t0 -o "$tmp/Statement.olean" ../../Stage1_Instances/THM-M-1058/Statement.lean` | 1 | Preliminary path-layout failure before elaboration: the input file was outside the `Formalizations/Lean` root. It produced no olean and was replaced by the direct-Lean recipe below. |
| Isolated pinned-Lean `--trust=0 -t 0` two-step elaboration | 0 | Exact statement and both negative declarations elaborated; axiom reports were `[propext, Classical.choice, Quot.sound]`. Statement olean SHA-256 `2d13244d880314c945570a53549a646e7e62ef3ceaa871ce53ee22034af97d6b`; proof output SHA-256 `b8cb7767f4f4144f5897c72744ac29db8b9d9e0af1eaf6c150e4631b7b1b9701`. The `.lake` content digest was `4a8253d2e8265f8edbdf4590874617260e2fd4b524c5cd1f62877b7894a96ece` both before and after. |
| `rg -l -i --glob '*.lean' 'LargeDeviationPrinciple\|LargeDeviation\|large deviation\|large-deviation\|LDPUpperBound\|LDPLowerBound\|LaplacePrinciple\|Sanov\|GartnerEllis\|Gärtner.?Ellis\|Varadhan' Formalizations/Lean/.lake/packages` | 1 | Expected no-match exit in pinned package sources. |
| The same bounded query under `Formalizations/Lean/AwesomeTheorems` | 0 | Seven textual hits; none is an exact terminal proof body. |
| `rg -n -i --glob '*.lean' '\b(sorry\|admit\|sorryAx\|native_decide)\b\|^[[:space:]]*(axiom\|unsafe\|external)[[:space:]]\|implemented_by' Stage1_Instances/THM-M-1058` | 1 | Expected no-match exit: no prohibited proof boundary in owned Lean sources. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 0 | `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. |
| `python3 -m json.tool` plus semantic `jq -e` on the adjacent JSON record | 0 | The blocker record parses, and its identity, state, completion flags, and cut set agree. |
| `git diff --no-index --check /dev/null` against each new artifact | 1 each | Expected new-file difference exits with no whitespace diagnostics for JSON and Markdown. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The statement mutation checker was not credited in this run. Its implementation
repeatedly invokes `lake env lean`, and it stalled under heavy concurrent
shared-cache contention. The frozen expression hash and killed mutations remain
predecessor evidence; this proof run independently re-elaborated the exact
tracked `Statement.lean` source under `--trust=0`.

Exact isolated recipe from the repository root (`tmp` was a fresh `/tmp`
directory and was removed after hashing its outputs):

```bash
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
target="$PWD/Stage1_Instances/THM-M-1058"
tmp=$(mktemp -d /tmp/thm-m-1058-slot47.XXXXXX)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600 \
  "$lean" --trust=0 -t0 -R "$target" \
  -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 600 \
  "$lean" --trust=0 -t0 -R "$target" Proof.lean
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `flt-regular`
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. Current input hashes and exact
results are recorded in the adjacent JSON artifact.

This is an actionable blocker report and real negative kernel evidence, not a
positive proof receipt. It does not satisfy `S56-M-1058-PROOF`, complete the
audit or theorem, or authorize validation, release, or master acceptance.
