# THM-M-0468 proof blocker at `6ac589f0`

## Verdict

`S56-M-0468-PROOF` is blocked. No positive proof body was added, and this
packet does not claim worker self-test, audit completion, validation, release,
theorem completion, or master acceptance.

The frozen target quantifies over every `BogomolovData` record, but that
structure has no laws connecting its addition, height, torsion, membership,
or density fields. The existing placeholder-free `ProofBlocker.lean` makes
all ambient hypotheses and density claims true on singleton carriers while
making `isTorsionPoint` false everywhere. Lean therefore checks

```text
Stage1Instances.THM_M_0468.not_bogomolovTarget :
  Not Stage1Instances.THM_M_0468.BogomolovTarget
```

under trust level zero. A positive inhabitant of the exact target would make
the environment inconsistent. This refutes only the overbroad Lean encoding,
not the mathematical Ullmo--Zhang theorem. The conditional
`root_of_direction_packages` theorem assumes the two missing directions and
earns no positive proof-body credit. The honest proposed machine-debt change
is `M4 -> M5`, subject to master reconciliation.

## Failed Gates

The first workflow failure is dependency acceptance:
`S56-M-0468-OBLIGATION_TREE` remains worker-provisional `[_]`, not
master-accepted `[x]`. Independently, exact-target consistency fails at
`M0468-S-DOMAINS` because the frozen root has a kernel-checked countermodel.

The predecessor statement evidence is incomplete as well. Its checker kills
four removed-predicate mutations, while rev-5.6 section 5.1 also requires a
changed domain, changed binder scope, and boundary-case mutation.

Positive proof work may resume only after an accepted statement repair
replaces the unconstrained semantic surface with concrete pinned definitions
or source-justified, noncircular compatibility laws. The repair must rule out
the countermodel without assuming either direction of the desired
equivalence. Statement mutations, anchor audit, obligation-tree freeze, and
proof execution must then rerun in dependency order.

There were already 27 target-scoped proof-blocker or proof-recheck JSON
packets before this packet, while the authoritative proof item still records
zero attempts and no children. Rev-5.6 section 10.2 requires splitting after
five unresolved execution ticks. The scheduler should reconcile attempts and
redirect or split this work into statement repair rather than dispatching
another positive-proof retry.

## Scoped Validation

All commands ran in this worker clone. The automation-provided symlink to the
canonical pinned `.lake` artifacts was reused read-only. No `lake update`,
`lake build`, dependency clone/fetch, checkout repair, network command, or
`.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0468` | 0 | Rank 314; lane `hard_mathlib_anchor_and_wrapper`; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0468/check_statement.py` | 0 | Fingerprint `def6574...fa0e`; all four recorded predicate-removal mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0468/check_anchor_audit.py` | 0 | Target fingerprint, exact pin, module hash, and four candidate classifications passed. |
| `python3 Stage1_Instances/THM-M-0468/check_obligation_tree.py` | 0 | 20 obligations and 44 typed edges passed; denominator `0b324115...6c4`; root remains open at `M4`. |
| Direct pinned `lake env lean --trust=0 -t0` replay below | 0 | The target, conditional composition, and exact negation elaborated; both `assert_no_sorry` probes passed; both proof declarations depend on `[propext, Classical.choice, Quot.sound]`. |
| `rg -n '\\b(sorry\|admit\|sorryAx\|native_decide)\\b\|^[[:space:]]*(axiom\|unsafe\|external)[[:space:]]'` over the three checked Lean sources | 1 | No match; exit 1 is ripgrep's expected no-match result. |

Exact narrow Lean recipe, run from the repository root:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-0468-head6ac589f0-slot31.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
sed 's/^import Statement$/import M0468Statement/' \
  "$root/Stage1_Instances/THM-M-0468/ObligationTree.lean" \
  > "$tmp/M0468ObligationTree.lean"
sed 's/^import Statement$/import M0468Statement/' \
  "$root/Stage1_Instances/THM-M-0468/ProofBlocker.lean" \
  > "$tmp/M0468ProofBlocker.lean"
cp "$root/Stage1_Instances/THM-M-0468/Statement.lean" \
  "$tmp/M0468Statement.lean"
printf '%s\n' \
  'import M0468ObligationTree' \
  'import M0468ProofBlocker' \
  'import Mathlib.Util.AssertNoSorry' \
  '' \
  'open Stage1Instances.THM_M_0468' \
  '' \
  '#check BogomolovTarget' \
  '#check root_of_direction_packages' \
  '#check not_bogomolovTarget' \
  'assert_no_sorry root_of_direction_packages' \
  'assert_no_sorry not_bogomolovTarget' \
  '#print sorries root_of_direction_packages' \
  '#print sorries not_bogomolovTarget' \
  '#print axioms root_of_direction_packages' \
  '#print axioms not_bogomolovTarget' > "$tmp/Probe.lean"
cd "$root/Formalizations/Lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" \
  timeout --foreground --kill-after=10s 300 \
  lake env lean --trust=0 -t0 -R "$tmp" \
  -o "$tmp/M0468Statement.olean" "$tmp/M0468Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" \
  timeout --foreground --kill-after=10s 300 \
  lake env lean --trust=0 -t0 -R "$tmp" \
  -o "$tmp/M0468ObligationTree.olean" "$tmp/M0468ObligationTree.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" \
  timeout --foreground --kill-after=10s 300 \
  lake env lean --trust=0 -t0 -R "$tmp" \
  -o "$tmp/M0468ProofBlocker.olean" "$tmp/M0468ProofBlocker.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" \
  timeout --foreground --kill-after=10s 300 \
  lake env lean --trust=0 -t0 -R "$tmp" \
  -o "$tmp/Probe.olean" "$tmp/Probe.lean"
sha256sum "$tmp/M0468Statement.olean" \
  "$tmp/M0468ObligationTree.olean" \
  "$tmp/M0468ProofBlocker.olean" "$tmp/Probe.olean"
```

The four temporary olean hashes were, respectively,
`ceaf7430cba2e39a950d7684b0ba6278f2d95b6df695ad3ae0c3fbcd87e6c689`,
`5d46f876330d38723ff860d92dd85c4ff230ef3cca8ec2157e320fed2ff47841`,
`a4afb48af34b95c7b20e22f352cac526a32084532083bace11358507c5fa8c17`,
and `6c60263d9c8044afed458d2b63b7f0c478cb41062516e5643d5006e211eead13`.
The trap removed all temporary outputs.

Pinned identities are Lean `4.29.0` at
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, mathlib commit/tree
`8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`, and flt-regular commit/tree
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` /
`32c9eace926573a9981787ae97643e520353c893`.

The pre-existing untracked `.lake` symlink makes this nonrelease evidence.
This is an actionable current-base blocker, not a proof receipt or item-state
claim. No `.stage1-worker-selftest.json` was written.
