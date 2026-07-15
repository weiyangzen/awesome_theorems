# THM-M-0468 proof phase: current-base blocker

Item: `S56-M-0468-PROOF`

Base revision: `ebfa067f2385ca03cc0a0eeecf151993a994962c`

Base tree: `4d482bdb45ec4ff17c128d712608f7c7eea1ffc8`

Validated: `2026-07-15T21:08:07+08:00` (`Asia/Shanghai`)

## Verdict

`blocked`: the exact frozen Lean target cannot have a consistent positive proof
body. The proof item stays `[ ]`. No `.stage1-worker-selftest.json` is written,
and no proof, receipt acceptance, validation, release, or theorem completion is
claimed.

`BogomolovData` is an unconstrained collection of carriers, operations, and
predicates. It has no laws connecting height, torsion, translation, membership,
or Zariski density. The existing placeholder-free `ProofBlocker.lean` therefore
instantiates singleton carriers with every ambient hypothesis and density claim
true and `isTorsionPoint` false. Pinned Lean checks the exact negation:

```text
Stage1Instances.THM_M_0468.not_bogomolovTarget :
  Not Stage1Instances.THM_M_0468.BogomolovTarget
```

The declaration is sorry-free under `--trust=0` and depends only on `propext`,
`Classical.choice`, and `Quot.sound`. Any positive inhabitant of the frozen root
would yield `False`. This refutes only the overbroad abstract encoding, not the
mathematical Ullmo-Zhang theorem.

`root_of_direction_packages` is only a checked conditional assembly. It takes
`DenseSmallPointsImplySpecial` and `SpecialImplyDenseSmallPoints` as premises;
neither direction has a proof body. The pinned mathlib search found no
Bogomolov, Neron-Tate, canonical-height, small-points, or equidistribution proof
anchor.

The first workflow failure is also upstream: `S56-M-0468-OBLIGATION_TREE` is
only worker-provisional `[_]`, not master-accepted `[x]`. The first semantic
failure is exact-target consistency at `M0468-S-DOMAINS`.

## Retry Condition

Reopen `S56-M-0468-STATEMENT`. Replace the unconstrained record with concrete
pinned definitions, or add source-justified noncircular laws that exclude the
countermodel without assuming either direction of the desired equivalence.
Then add the missing changed-domain, binder-scope, and boundary-case mutations,
freeze a new statement and registry version, and rerun statement, anchor-audit,
obligation-tree, and proof phases in dependency order.

Before this packet the directory contained 36 head-bound blocker JSON packets
and 42 proof blocker/recheck JSON packets, while the authoritative proof item
still recorded zero attempts and no child nodes. The integration lane should
reconcile the attempt ledger and apply the rev-5.6 five-tick split rule rather
than schedule another unchanged positive proof attempt. This worker did not edit
the authoritative DAG or checklist.

## Scoped Validation

All commands ran in this worker clone. The pre-existing `.lake` symlink to the
canonical pinned artifacts was reused read-only. No update, build, clone, fetch,
checkout repair, network command, or dependency mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0468` | 0 | Rank 314; lane `hard_mathlib_anchor_and_wrapper`; lifecycle `planned`; theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0468/check_statement.py` | 0 | Fingerprint `def6574...fa0e`; the four recorded removed-predicate mutations passed. |
| `python3 Stage1_Instances/THM-M-0468/check_anchor_audit.py` | 0 | Target fingerprint, exact pin, module hash, and four candidate classifications passed. |
| `python3 Stage1_Instances/THM-M-0468/check_obligation_tree.py` | 0 | 20 obligations and 44 typed edges passed; denominator `0b324115...6c4`; root and both directions remain open at `M4`. |
| Pinned `lake env lean --trust=0 -t0` replay below | 0 | Exact target, conditional composition, exact negation, and contradiction probe elaborated; all three proof declarations were sorry-free and used only `[propext, Classical.choice, Quot.sound]`. |
| `rg -in --glob '*.lean' 'bogomolov\|neron.?tate\|canonical.?height\|small.?points\|equidistribution' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | No matches; exit 1 is ripgrep's expected no-match result. |
| Placeholder scan over the three Lean sources | 1 | No forbidden construct; exit 1 is ripgrep's expected no-match result. |
| Packet JSON/semantic/whitespace checks and `test ! -e .stage1-worker-selftest.json` | 0 | `packet_semantics_ok`; `packet_validation_ok`; the self-test manifest is absent because the proof phase is blocked. |

The trust-zero replay used collision-free module names in a fresh temporary
directory and removed all outputs by trap:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-0468-ebfa067f-slot36.XXXXXX)
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
  'theorem frozen_target_inconsistent (h : BogomolovTarget) : False :=' \
  '  not_bogomolovTarget h' \
  'assert_no_sorry root_of_direction_packages' \
  'assert_no_sorry not_bogomolovTarget' \
  'assert_no_sorry frozen_target_inconsistent' \
  '#print sorries root_of_direction_packages' \
  '#print sorries not_bogomolovTarget' \
  '#print sorries frozen_target_inconsistent' \
  '#print axioms root_of_direction_packages' \
  '#print axioms not_bogomolovTarget' \
  '#print axioms frozen_target_inconsistent' > "$tmp/Probe.lean"
cd "$root/Formalizations/Lean"
for module in M0468Statement M0468ObligationTree M0468ProofBlocker Probe; do
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" \
    timeout --foreground --kill-after=10s 300s lake env lean \
    --trust=0 -t0 -R "$tmp" -o "$tmp/$module.olean" "$tmp/$module.lean"
done
sha256sum "$tmp/M0468Statement.olean" \
  "$tmp/M0468ObligationTree.olean" "$tmp/M0468ProofBlocker.olean" \
  "$tmp/Probe.lean" "$tmp/Probe.olean"
printf 'temporary_outputs_removed_by_exit_trap=true\n'
```

The temporary hashes were
`ceaf7430cba2e39a950d7684b0ba6278f2d95b6df695ad3ae0c3fbcd87e6c689`,
`5d46f876330d38723ff860d92dd85c4ff230ef3cca8ec2157e320fed2ff47841`,
`a4afb48af34b95c7b20e22f352cac526a32084532083bace11358507c5fa8c17`,
`acad4877efd209f8a1a91339cd936960a1598f8fbcacd5bc32ec64944d11a252`,
and `6c2433d467a1027d5802be15bb2cf7a81cebfaf648886afa4c0829e8915e8cdb`.

Pinned identities are Lean `4.29.0` at
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, mathlib commit/tree
`8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`, and flt-regular commit/tree
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` /
`32c9eace926573a9981787ae97643e520353c893`.

This is actionable current-base negative kernel evidence. It is not a proof
receipt or an item-state transition.
