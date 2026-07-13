# THM-M-1058 proof-phase recheck at `a86029b3`

Item: `S56-M-1058-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `a86029b30f12acc3537f70ab1c167cc25702c09b`

Base tree: `ab12055e811b574338987391b59b010338c120d2`

Lifecycle: `planned -> planned`

## Verdict

`blocked`. The frozen expression `LargeDeviationPrinciple E D` is a property
of supplied data `D`, not a closed theorem with a model and hypotheses from
which its conclusion follows. `LargeDeviationData` supplies probability
measures, a positive speed tending to infinity, and a nonnegative
lower-semicontinuous rate. It supplies neither the all-closed-set upper bound
nor the all-open-set lower bound.

The tracked, placeholder-free `Proof.lean` makes that nonimplication
kernel-visible. On `PUnit`, it uses the default probability measure, speed
`n + 1`, and constant rate `1` to prove:

```text
Stage1Instances.THM_M_1058.not_largeDeviationPrinciple_counterexample :
  Not (LargeDeviationPrinciple PUnit counterexampleData)

Stage1Instances.THM_M_1058.not_all_largeDeviationPrinciple :
  Not (forall D : LargeDeviationData PUnit,
    LargeDeviationPrinciple PUnit D)
```

For `Set.univ`, the scaled log probability is zero while the negated rate
infimum is negative one. Thus a universal completion from the current record
fields would require `0 <= -1`. This refutes only the under-specified generic
encoding; it neither proves a positive LDP for selected data nor refutes a
source-faithful model-specific large-deviation theorem.

The root cut remains `M1058-UPPER` and `M1058-LOWER`. The historical local
wrapper assumes both branches and merely projects their conjunction, so it is
circular as a terminal proof. A bounded pinned-package search found no exact
terminal LDP body, and the local Cramer surface is a different open target.

No positive proof body or receipt was added, no obligation was closed, and the
item remains `[ ]` at `[H1, M3, R3]`. Because the assigned proof phase is not
complete, `.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed gate is `M1058-UPPER`: the frozen input contains neither a
concrete probabilistic family nor hypotheses implying the closed-set upper
bound. `M1058-LOWER` is independently open.

Resume only after an authorized statement repair binds the target to specified
data with substantive source-faithful hypotheses and publishes a new accepted
statement fingerprint and obligation registry. The other legal route is an
immutable exact compatible Lean 4 terminal proof that can be pinned and
checked. Adding the two desired bounds as assumptions would only create a
circular wrapper.

## Validation

Checks ran in this worker clone against the already provisioned pinned Lake
artifacts. No `lake update`, `lake build`, dependency clone/fetch, network
operation, or `.lake` mutation was performed. Temporary Lean output was
written below `/tmp` and removed. The automation-provided untracked
`Formalizations/Lean/.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed; all are L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1058` | 0 | Rank 250; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1058/check_statement.py` | 0 | Expression SHA-256 `60a04b08693660e1b050384acab58541f1a768cc7dfa32da65ac587e47876a33`; removed-hypothesis, changed-domain, changed-binder-scope, and weak-LDP mutations all killed. |
| `python3 Stage1_Instances/THM-M-1058/check_obligation_tree.py` | 0 | 16 obligations and 26 typed edges passed; denominator `603b6a62d345eb0be098c815ee9b1d743faad5f11a5c7bd503fb58a3318973f2`; root remains open M3. |
| Narrow pinned-Lean `--trust=0 -t0` recipe below | 0 | `Statement.lean` and the negative `Proof.lean` declarations elaborated. Both negative declarations reported `[propext, Classical.choice, Quot.sound]`. Statement olean SHA-256: `2d13244d880314c945570a53549a646e7e62ef3ceaa871ce53ee22034af97d6b`; proof output SHA-256: `b8cb7767f4f4144f5897c72744ac29db8b9d9e0af1eaf6c150e4631b7b1b9701`. |
| `rg -l -i --glob '*.lean' 'LargeDeviationPrinciple\|LargeDeviation\|large deviation\|large-deviation\|LDPUpperBound\|LDPLowerBound\|LaplacePrinciple\|Sanov\|GartnerEllis\|Gärtner.?Ellis\|Varadhan' Formalizations/Lean/.lake/packages` | 1 | Expected no-match exit in the pinned package sources. |
| The same bounded query under `Formalizations/Lean/AwesomeTheorems` | 0 | Seven textual matches; none is an exact terminal proof body. |
| `rg -n -i --glob '*.lean' '\b(sorry\|admit\|sorryAx\|native_decide)\b\|^[[:space:]]*(axiom\|unsafe\|external)[[:space:]]\|implemented_by' Stage1_Instances/THM-M-1058` | 1 | Expected no-match: no prohibited proof boundary in owned Lean sources. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 0 | `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. |
| `python3 -m json.tool` plus a target-specific invariant check on the adjacent JSON record | 0 | The blocker record parses; identity, base, blocked state, unchanged vector, false completion flags, empty receipts, and root cut agree. |
| `git diff --no-index --check /dev/null` against each new artifact | 1 each | Expected new-file difference exits with no whitespace diagnostics for JSON and Markdown. |
| `git diff --check -- Stage1_Instances/THM-M-1058 .stage1-worker-selftest.json` | 0 | No tracked scoped whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The exact narrow Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-1058
tmp=$(mktemp -d /tmp/thm-m-1058-slot47-current.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600 \
  "$lean" --trust=0 -t0 -R "$target" \
  -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 600 \
  "$lean" --trust=0 -t0 -R "$target" Proof.lean
```

Pinned environment: Lean `4.29.0` at
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `flt-regular`
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`.

This is current-base blocker evidence, not a positive proof receipt. It does
not satisfy `S56-M-1058-PROOF`, complete the audit or theorem, or authorize
validation, release, or master acceptance.
