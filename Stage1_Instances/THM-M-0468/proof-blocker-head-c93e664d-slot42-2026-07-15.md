# THM-M-0468 proof phase: current-base blocker

Item: `S56-M-0468-PROOF`

Base revision: `c93e664d3a7e0383b037cfa2d5e47ba14adfb2cb`

Base tree: `d8ea21a05ed52ff43d984128352a07f479aae6e6`

Validated: `2026-07-15T17:35:34+08:00` (`Asia/Shanghai`)

## Verdict

`blocked`: no consistent positive proof body can inhabit the exact frozen Lean
target. The proof item remains `[ ]`; no proof, provisional state, validation,
release, theorem completion, receipt acceptance, or master acceptance is
claimed. A root `.stage1-worker-selftest.json` is deliberately absent.

`Statement.lean` quantifies over every `BogomolovData`, but that record has no
laws connecting height, torsion, translation, membership, or Zariski density.
The placeholder-free `ProofBlocker.lean` instantiates singleton carriers for
which every ambient hypothesis and every density claim is true while
`isTorsionPoint` is false everywhere. Trust-zero Lean checks

```text
Stage1Instances.THM_M_0468.not_bogomolovTarget :
  Not Stage1Instances.THM_M_0468.BogomolovTarget
```

and the probe

```text
frozen_target_inconsistent (h : BogomolovTarget) : False
```

Both are sorry-free and depend only on `propext`, `Classical.choice`, and
`Quot.sound`. Thus adding a positive inhabitant of the frozen root would make
the environment inconsistent. This refutes only the overbroad abstract Lean
encoding, not the mathematical Ullmo-Zhang theorem. The checked
`root_of_direction_packages` theorem assumes both missing directions and earns
no proof-body credit for either.

The first workflow failure is that `S56-M-0468-OBLIGATION_TREE` is only
worker-provisional `[_]`, not master-accepted `[x]`. Independently, the first
semantic proof failure is exact-target consistency at `M0468-S-DOMAINS`.
The statement checker also records only four predicate-removal mutations and
does not cover the changed-domain, binder-scope, and boundary-case classes
required by rev-5.6. The 20 frozen validation recipes cover no Lean declaration
and replay only the structural graph checker.

## Retry Condition

Reopen `S56-M-0468-STATEMENT`. Replace the unconstrained semantic record with
concrete pinned definitions, or add source-justified noncircular compatibility
laws connecting height, torsion, translation, subvariety membership, and
Zariski density. The repair must exclude this countermodel without assuming
either direction of the desired equivalence. Add the missing mutation classes,
freeze a new statement fingerprint and obligation-registry version, and rerun
statement, anchor-audit, obligation-tree, and proof phases in dependency order.

Before this packet the directory already contained 27 head-bound proof blocker
JSON packets and 30 blocker JSON packets in total, while the authoritative item
still records `attempts: 0` and no children. Rev-5.6 requires a split after five
unresolved execution ticks. The integration lane should reconcile the attempt
ledger and redirect work to statement repair rather than schedule another
unchanged positive-proof attempt. This worker did not edit the authoritative
DAG or blueprint checklist.

## Scoped Validation

All commands ran in this worker clone. The automation-provided untracked
`.lake` symlink to canonical pinned artifacts was reused read-only. No `lake
update`, `lake build`, dependency clone/fetch, checkout repair, network command,
or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0468` | 0 | Rank 314; lane `hard_mathlib_anchor_and_wrapper`; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0468/check_statement.py` | 0 | Fingerprint `def6574...fa0e`; all four recorded predicate-removal mutations passed. |
| `python3 Stage1_Instances/THM-M-0468/check_anchor_audit.py` | 0 | Target fingerprint, exact pin, module hash, and four candidate classifications passed. |
| `python3 Stage1_Instances/THM-M-0468/check_obligation_tree.py` | 0 | 20 obligations and 44 typed edges passed; denominator `0b324115...6c4`; root and both direction packages remain open at `M4`. |
| Pinned `lake env lean --trust=0 -t0` replay below | 0 | Exact target, conditional composition, exact negation, and contradiction probe elaborated; all three proof declarations were sorry-free and used only `[propext, Classical.choice, Quot.sound]`. |
| Placeholder scan over the three Lean sources | 1 | No forbidden construct; exit 1 is ripgrep's expected no-match result. |

The Lean replay used collision-free copies in a fresh `/tmp` directory, removed
by a trap. It constructed `LEAN_PATH` only from already materialized build
libraries, then ran the existing pinned toolchain from the mathlib checkout:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-0468-head-c93e664d-slot42.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$root/Stage1_Instances/THM-M-0468/Statement.lean" \
  "$tmp/M0468Statement.lean"
sed 's/^import Statement$/import M0468Statement/' \
  "$root/Stage1_Instances/THM-M-0468/ObligationTree.lean" \
  > "$tmp/M0468ObligationTree.lean"
sed 's/^import Statement$/import M0468Statement/' \
  "$root/Stage1_Instances/THM-M-0468/ProofBlocker.lean" \
  > "$tmp/M0468ProofBlocker.lean"
paths=("$tmp" "$root/Formalizations/Lean/.lake/build/lib/lean")
while IFS= read -r p; do paths+=("$p"); done < <(
  find -L "$root/Formalizations/Lean/.lake/packages" -type d \
    -path '*/.lake/build/lib/lean' | sort
)
lean_path=$(IFS=:; printf '%s' "${paths[*]}")
cd "$root/Formalizations/Lean/.lake/packages/mathlib"
for module in M0468Statement M0468ObligationTree M0468ProofBlocker; do
  LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
    timeout --foreground --kill-after=5s 300s lake env lean \
    --trust=0 -t0 -R "$tmp" -o "$tmp/$module.olean" "$tmp/$module.lean"
done
printf '%s\n' \
  'import M0468ObligationTree' \
  'import M0468ProofBlocker' \
  'import Mathlib.Util.AssertNoSorry' \
  'open Stage1Instances.THM_M_0468' \
  '#check BogomolovTarget' \
  '#check root_of_direction_packages' \
  '#check not_bogomolovTarget' \
  'assert_no_sorry root_of_direction_packages' \
  'assert_no_sorry not_bogomolovTarget' \
  'theorem frozen_target_inconsistent (h : BogomolovTarget) : False :=' \
  '  not_bogomolovTarget h' \
  'assert_no_sorry frozen_target_inconsistent' \
  '#print axioms root_of_direction_packages' \
  '#print axioms not_bogomolovTarget' \
  '#print axioms frozen_target_inconsistent' > "$tmp/Probe.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean \
  --trust=0 -t0 -R "$tmp" -o "$tmp/Probe.olean" "$tmp/Probe.lean"
sha256sum "$tmp/M0468Statement.olean" \
  "$tmp/M0468ObligationTree.olean" "$tmp/M0468ProofBlocker.olean" \
  "$tmp/Probe.lean" "$tmp/Probe.olean"
```

The output hashes were `ceaf7430...e6c689`, `5d46f876...47841`,
`a4afb48a...95c17`, `49b65260...27836`, and `86f59f62...fd497`, in
the order shown. Pinned identities are Lean `4.29.0` at
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, mathlib commit/tree
`8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`, and flt-regular manifest
commit/tree `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` /
`32c9eace926573a9981787ae97643e520353c893`.

This is actionable, current-base negative kernel evidence. It is not a proof
receipt or an item-state transition.
