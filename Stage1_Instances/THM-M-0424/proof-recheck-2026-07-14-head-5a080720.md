# THM-M-0424 proof recheck at `5a080720`

Item: `S56-M-0424-PROOF`

Intent: `prove`

Recorded at: `2026-07-14T03:24:52+08:00`

Base revision: `5a080720059200b542aa35ee17a748b3251fe8d0`

Base tree: `d7029aa7599db39fbcc55e968a4fe70376143f27`

## Verdict

`blocked`. A positive proof body cannot inhabit the exact frozen Lean target.
The owned placeholder-free declaration

```text
Stage1Instances.THM_M_0424.UniverseCounterexample.not_brauerGroupStatement :
  Not Stage1Instances.THM_M_0424.BrauerGroupStatement.{1,0}
```

was replayed with `lake env lean --trust=0` against this base. Hence a
universe-polymorphic proof of the frozen target would specialize to `{1,0}`
and contradict a kernel-checked theorem.

At that specialization, take `K := Type 0 : Type 1` with the field structure
from `Infinite.nonempty_field`. Any `BrauerGroupLawData.{1,0} K` contains
`oneRep : CSA.{1,0} K` and an algebra equivalence from its carrier in `Type 0`
to `K`. The underlying equivalence proves `Small.{0} (Type 0)`, contradicting
`not_small_type`.

This refutes the frozen Lean encoding, not the classical Brauer-group theorem.
Exact-target consistency first fails at
`S56-5.1-EXACT-TARGET-CONSISTENCY / M0424-S-BOUNDARY`, witnessed through
`M0424-C-ONE`. The statement phase must relate the field and representative
universes, publish a new expression fingerprint, and refreeze all dependent
artifacts. This proof worker may not silently substitute that repaired target.

An independent downstream blocker remains: pinned
`Mathlib.Algebra.BrauerGroup.Defs` defines the quotient but explicitly leaves
the tensor-product abelian-group structure as TODO 1. There are no terminal
bodies for tensor-CSA packaging, stable-equivalence congruence, quotient
descent, associativity, commutativity, unit, or opposite inverse.

No positive proof body or receipt was added. Lifecycle stays `planned`, the
root vector stays `[H1, M3, R3]`, the proof item stays `[ ]`, and theorem
completion stays false. Because the assigned phase is not complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Scoped validation

The automation-provided `.lake` link was treated as read-only. No Lake update
or build, dependency clone or fetch, network access, or `.lake` mutation was
performed. Lean outputs were confined to disposable `/tmp` directories and
removed after replay.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0424` | 0 | Rank 78; lifecycle planned; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0424/check_anchor_audit.py` | 0 | Six immutable candidates verified; exact root remains M3. |
| `python3 Stage1_Instances/THM-M-0424/check_obligation_tree.py` | 0 | 18 obligations and 35 typed edges passed; denominator `83afccaebaea7322e89808dde65a4cff0cd758498ff63f70fbf8b00cf1e42a00`; root open M3. |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| Isolated trust-zero `lake env lean` recipe below | 0 | Exact target refuted at `{1,0}`; all four counterexample declarations reported exactly `propext`, `Classical.choice`, and `Quot.sound`; every `assert_no_sorry` passed. |
| Scoped prohibited-construct scan of owned `*.lean` files | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, declared `axiom`, `opaque`, `unsafe`, `external`, `native_decide`, or `implemented_by`. |
| `python3 -m json.tool Stage1_Instances/THM-M-0424/proof-recheck-2026-07-14-head-5a080720.json` | 0 | This current-base structured blocker packet is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0424` | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The successful narrow Lean replay used a fresh `/tmp` output directory:

```bash
set -u
repo="$PWD"
target="$repo/Stage1_Instances/THM-M-0424"
lean_root="$repo/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-0424-head5a080720.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
base_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
(cd "$lean_root" && LEAN_NUM_THREADS=1 lake env lean --trust=0 -t0 \
  --root="$target" -o "$tmp/Statement.olean" "$target/Statement.lean")
(cd "$lean_root" && LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" \
  lake env lean --trust=0 -t0 --root="$target" \
  "$target/UniverseCounterexample-2026-07-14-head-5753c6ed.lean")
```

The statement output SHA-256 was
`efa2ea0ea05ce852276dd67e3abe1c6f3c705670f8c435bebcf57be1456b4e51`;
the counterexample output SHA-256 was
`c309037999d6b2be51e46f3e5a1e3ce8f67255764f213671c71f0df4696e8dcb`.

Pinned environment: Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; Lake manifest SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Resume only after statement repair and dependent rev-5.6 refreezing are
accepted, followed by real placeholder-free construction/group-law bodies or
an immutable compatible pinned proof. This artifact claims no proof-node state
transition, audit completion, validation, release, or master acceptance.
