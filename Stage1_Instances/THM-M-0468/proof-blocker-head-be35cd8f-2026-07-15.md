# THM-M-0468 proof phase: current-base blocker

Item: `S56-M-0468-PROOF`

Base revision: `be35cd8f5123e9d06247b12859f3843bdd90c66f`

Base tree: `a275a21a449fbcbd6c2333f5cfe737e906b20db6`

Rechecked: `2026-07-15T08:16:38+08:00` (`Asia/Shanghai`)

## Verdict

`blocked`: no consistent positive proof body can inhabit the exact frozen Lean
target. The proof item remains `[ ]`; no proof, provisional state, audit
completion, validation, release, theorem completion, or master acceptance is
claimed. A root `.stage1-worker-selftest.json` is deliberately absent.

`Statement.lean` quantifies over every `BogomolovData`, but that structure has
no laws connecting its operations or predicates to abelian geometry. The
placeholder-free `ProofBlocker.lean` supplies a singleton model in which every
ambient hypothesis and density claim is true while `isTorsionPoint` is false
everywhere. Trust-zero Lean checks

```text
Stage1Instances.THM_M_0468.not_bogomolovTarget :
  Not Stage1Instances.THM_M_0468.BogomolovTarget
```

A positive proof of the frozen target would contradict this theorem. This
refutes only the overbroad formal encoding, not the mathematical Ullmo--Zhang
theorem. The fail-closed proposal is `[H1, M4, R3] -> [H1, M5, R3]`, subject to
master reconciliation. The checked `root_of_direction_packages` declaration
assumes both missing implications and supplies no proof-body credit. The pinned
inventory and current materialized dependency scan contain no exact eligible
Bogomolov proof body.

## Failed Gates

The first workflow failure is prerequisite acceptance:
`S56-M-0468-OBLIGATION_TREE` is only worker-provisional `[_]`, not
master-accepted `[x]`. Independently, the first semantic proof failure is
exact-target consistency at `M0468-S-DOMAINS`.

The predecessor statement evidence is also incomplete. Its checker kills four
removed-predicate mutations, while rev-5.6 section 5.1 additionally requires a
changed domain, changed binder scope, and boundary-case mutation. The dossier
still leaves `X = A` and zero-dimensional behavior open.

Positive work may resume only after the statement phase replaces the
unconstrained semantic surface with concrete pinned definitions or
source-justified, noncircular compatibility laws. The repair must rule out the
countermodel without assuming either direction of the desired equivalence and
must cover height and torsion, translation, subvariety membership, and Zariski
density. It invalidates the present expression fingerprint and architecture,
so statement mutations, anchor audit, obligation-tree freeze, and proof
execution must rerun in dependency order.

## Scoped Validation

All commands ran in this worker clone. The automation-provided symlink to the
canonical pinned `.lake` artifacts was reused read-only. No `lake update`,
`lake build`, dependency clone/fetch, checkout repair, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0468` | 0 | Rank 314; lane `hard_mathlib_anchor_and_wrapper`; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 300 python3 Stage1_Instances/THM-M-0468/check_statement.py` | 0 | Fingerprint `def6574...fa0e`; all four recorded predicate-removal mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0468/check_anchor_audit.py` | 0 | Target fingerprint, exact pin, module hash, and four candidate classifications passed. |
| `python3 Stage1_Instances/THM-M-0468/check_obligation_tree.py` | 0 | 20 obligations and 44 typed edges passed; denominator `0b324115...6c4`; root remains open at `M4`. |
| Direct pinned `lake env lean --trust=0` replay below | 0 | The copied target, conditional composition, and target refutation elaborated; both `assert_no_sorry` probes passed, both declarations were sorry-free, and both axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| `rg -n '\b(sorry\|admit\|sorryAx\|native_decide)\b\|^[[:space:]]*(axiom\|unsafe\|external)[[:space:]]'` over the three checked Lean sources | 1 | No forbidden construct; exit 1 is ripgrep's expected no-match result. |

Exact narrow Lean recipe, run from the repository root:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-0468-be35cd8f.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
sed 's/^import Statement$/import M0468Statement/' \
  "$root/Stage1_Instances/THM-M-0468/ObligationTree.lean" \
  > "$tmp/M0468ObligationTree.lean"
sed 's/^import Statement$/import M0468Statement/' \
  "$root/Stage1_Instances/THM-M-0468/ProofBlocker.lean" \
  > "$tmp/M0468ProofBlocker.lean"
cp "$root/Stage1_Instances/THM-M-0468/Statement.lean" \
  "$tmp/M0468Statement.lean"
cd "$root/Formalizations/Lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" timeout 300 lake env lean --trust=0 \
  -R "$tmp" -o "$tmp/M0468Statement.olean" "$tmp/M0468Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" timeout 300 lake env lean --trust=0 \
  -R "$tmp" -o "$tmp/M0468ObligationTree.olean" \
  "$tmp/M0468ObligationTree.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" timeout 300 lake env lean --trust=0 \
  -R "$tmp" -o "$tmp/M0468ProofBlocker.olean" \
  "$tmp/M0468ProofBlocker.lean"
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
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" timeout 300 lake env lean --trust=0 \
  -R "$tmp" -o "$tmp/Probe.olean" "$tmp/Probe.lean"
sha256sum "$tmp/M0468Statement.olean" \
  "$tmp/M0468ObligationTree.olean" "$tmp/M0468ProofBlocker.olean"
```

The three temporary olean hashes were, respectively,
`ceaf7430cba2e39a950d7684b0ba6278f2d95b6df695ad3ae0c3fbcd87e6c689`,
`5d46f876330d38723ff860d92dd85c4ff230ef3cca8ec2157e320fed2ff47841`,
and `a4afb48af34b95c7b20e22f352cac526a32084532083bace11358507c5fa8c17`.
All temporary outputs were removed by the trap.

Pinned identities are Lean `4.29.0` at
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, and mathlib commit/tree
`8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

The pre-existing untracked `.lake` symlink makes this nonrelease evidence.
This packet is an actionable current-base blocker, not a proof receipt or an
item-state claim.
