# THM-M-0468 proof phase: current-base blocker

Item: `S56-M-0468-PROOF`

Base revision: `69f012f979c7114db1ee4a877c5742d4742cadba`

Base tree: `a4415d1a7f473d7540904dd4fd84d17ac0f99820`

Validated: `2026-07-15T20:13:50+08:00` (`Asia/Shanghai`)

## Verdict

`blocked`: no consistent positive proof body can inhabit the exact frozen Lean
target. The proof item remains `[ ]`; no proof, provisional state, validation,
release, theorem completion, receipt acceptance, or master acceptance is
claimed. A root `.stage1-worker-selftest.json` is deliberately absent.

`Statement.lean` quantifies over every `BogomolovData`, but that record has no
laws connecting height, torsion, translation, membership, or Zariski density.
The placeholder-free `ProofBlocker.lean` instantiates singleton carriers for
which every ambient hypothesis and density claim is true while
`isTorsionPoint` is false everywhere. Trust-zero Lean checks the exact negation

```text
Stage1Instances.THM_M_0468.not_bogomolovTarget :
  Not Stage1Instances.THM_M_0468.BogomolovTarget
```

The declaration is sorry-free and depends only on `propext`,
`Classical.choice`, and `Quot.sound`. Adding a positive inhabitant of the
frozen root would therefore make the environment inconsistent. This refutes
only the overbroad abstract Lean encoding, not the mathematical Ullmo--Zhang
theorem. The checked `root_of_direction_packages` theorem assumes both missing
directions and earns no proof-body credit for either.

The materialized pinned mathlib search found no declaration matching
`bogomolov`, Neron--Tate or canonical height, small points, or equidistribution.
Repo-local matches outside this dossier are statement or interface artifacts,
not terminal proof bodies. Independently, no consistent import could inhabit a
kernel-refuted target.

The first workflow failure is that `S56-M-0468-OBLIGATION_TREE` is only
worker-provisional `[_]`, not master-accepted `[x]`. Independently, the first
semantic proof failure is exact-target consistency at `M0468-S-DOMAINS`. The
statement checker also records only four predicate-removal mutations and does
not cover the changed-domain, binder-scope, and boundary-case classes required
by rev-5.6. The 20 frozen validation recipes cover no Lean declaration and
replay only the structural graph checker.

## Retry Condition

Reopen `S56-M-0468-STATEMENT`. Replace the unconstrained semantic record with
concrete pinned definitions, or add source-justified noncircular compatibility
laws connecting height, torsion, translation, subvariety membership, and
Zariski density. The repair must exclude this countermodel without assuming
either direction of the desired equivalence. Add the missing mutation classes,
freeze a new statement fingerprint and obligation-registry version, and rerun
statement, anchor-audit, obligation-tree, and proof phases in dependency order.

Before this packet the directory already contained 36 head-bound proof blocker
JSON packets and 39 blocker JSON packets in total, while the authoritative item
still records `attempts: 0` and no children. Rev-5.6 requires a split after five
unresolved execution ticks. The integration lane should reconcile the attempt
ledger and redirect work to statement repair rather than schedule another
unchanged positive-proof attempt. This worker did not edit the authoritative
DAG or generated blueprint checklist.

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
| `LEAN_NUM_THREADS=1 timeout --foreground --kill-after=10s 300 python3 Stage1_Instances/THM-M-0468/check_statement.py` | 0 | Fingerprint `def6574...fa0e`; all four recorded predicate-removal mutations passed. |
| `python3 Stage1_Instances/THM-M-0468/check_anchor_audit.py` | 0 | Target fingerprint, exact pin, module hash, and four candidate classifications passed. |
| `python3 Stage1_Instances/THM-M-0468/check_obligation_tree.py` | 0 | 20 obligations and 44 typed edges passed; denominator `0b324115...6c4`; root and both direction packages remain open at `M4`. |
| Pinned `lake env lean --trust=0 -t0` replay below | 0 | Exact target, conditional composition, exact negation, and contradiction probe elaborated; all three proof declarations were sorry-free and used only `[propext, Classical.choice, Quot.sound]`. |
| `rg -in --glob '*.lean' 'bogomolov\|neron.?tate\|canonical.?height\|small.?points\|equidistribution' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | No matches in the materialized pinned mathlib source; exit 1 is ripgrep's expected no-match result. |
| Placeholder scan over the three Lean sources | 1 | No forbidden construct; exit 1 is ripgrep's expected no-match result. |
| `python3 -m json.tool Stage1_Instances/THM-M-0468/proof-blocker-head-69f012f9-slot27-2026-07-15.json` | 0 | Structured blocker packet parsed successfully. |
| `git diff --no-index --check /dev/null FILE` for each new packet | 1 each | Expected new-file differences with empty diagnostics; no whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Self-test manifest is absent because the proof phase is blocked. |

The Lean replay used collision-free copies in a fresh `/tmp` directory, removed
by a trap, and ran only the existing pinned Lake environment:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-0468-69f012f9-slot27.XXXXXX)
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
  'open Stage1Instances.THM_M_0468' \
  '#check BogomolovTarget' \
  '#check root_of_direction_packages' \
  '#check not_bogomolovTarget' \
  'assert_no_sorry root_of_direction_packages' \
  'assert_no_sorry not_bogomolovTarget' \
  '#print sorries root_of_direction_packages' \
  '#print sorries not_bogomolovTarget' \
  '#print axioms root_of_direction_packages' \
  '#print axioms not_bogomolovTarget' \
  'theorem positive_root_is_impossible (h : BogomolovTarget) : False :=' \
  '  not_bogomolovTarget h' \
  'assert_no_sorry positive_root_is_impossible' \
  '#print sorries positive_root_is_impossible' \
  '#print axioms positive_root_is_impossible' > "$tmp/Probe.lean"
cd "$root/Formalizations/Lean"
for module in M0468Statement M0468ObligationTree M0468ProofBlocker Probe; do
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" \
    timeout --foreground --kill-after=10s 300 lake env lean \
    --trust=0 -t0 -R "$tmp" -o "$tmp/$module.olean" \
    "$tmp/$module.lean"
done
sha256sum "$tmp/M0468Statement.olean" \
  "$tmp/M0468ObligationTree.olean" "$tmp/M0468ProofBlocker.olean" \
  "$tmp/Probe.olean"
```

The temporary olean hashes were
`ceaf7430cba2e39a950d7684b0ba6278f2d95b6df695ad3ae0c3fbcd87e6c689`,
`5d46f876330d38723ff860d92dd85c4ff230ef3cca8ec2157e320fed2ff47841`,
`a4afb48af34b95c7b20e22f352cac526a32084532083bace11358507c5fa8c17`,
and `04d9f8f752310ed31f24a6293365d143025cc143b49bf64bfb465006929186bf`.
All temporary outputs were removed by the trap.

Pinned identities are Lean `4.29.0` at
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, mathlib commit/tree
`8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`, and flt-regular manifest
commit/tree `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` /
`32c9eace926573a9981787ae97643e520353c893`.

This is actionable, current-base negative kernel evidence. It is not a proof
receipt or an item-state transition.
