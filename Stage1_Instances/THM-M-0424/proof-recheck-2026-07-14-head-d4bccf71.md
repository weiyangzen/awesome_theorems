# THM-M-0424 proof recheck at `d4bccf71`

Item: `S56-M-0424-PROOF`

Intent: `prove`

Recorded at: `2026-07-14T03:11:01+08:00`

Base revision: `d4bccf713b0e77d6aa9a7cf10d18bffdd2ac4869`

Base tree: `cb4f28f50bc13b710b9dca81c30ab6205d849a91`

## Verdict

`blocked`. A positive proof body cannot inhabit the exact frozen Lean target.
The owned placeholder-free declaration

```text
Stage1Instances.THM_M_0424.UniverseCounterexample.not_brauerGroupStatement :
  Not Stage1Instances.THM_M_0424.BrauerGroupStatement.{1,0}
```

was replayed at Lean trust level zero against this base. Hence a
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
performed. Ordinary `lake env` discovery currently fails because the shared
pinned `flt-regular` checkout has an unresolved `HEAD`; this missing/corrupt
artifact is recorded rather than fetched. The same installed pinned Lean
executable and the pre-existing package oleans were therefore used directly
for the narrow trust-zero replay.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0424` | 0 | Rank 78; lifecycle planned; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0424/check_anchor_audit.py` | 0 | Six immutable candidates verified; exact root remains M3. |
| `python3 Stage1_Instances/THM-M-0424/check_obligation_tree.py` | 0 | 18 obligations and 35 typed edges passed; denominator `83afccaebaea7322e89808dde65a4cff0cd758498ff63f70fbf8b00cf1e42a00`; root open M3. |
| `(cd Formalizations/Lean && lake env which lean)` | 1 | `flt-regular` could not resolve `HEAD`; no dependency repair was attempted. |
| Direct isolated trust-zero Lean recipe below | 0 | Exact target refuted at `{1,0}`; all four counterexample declarations reported exactly `propext`, `Classical.choice`, and `Quot.sound`; every `assert_no_sorry` passed. |
| Scoped prohibited-construct scan of owned `*.lean` files | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, declared `axiom`, `opaque`, `unsafe`, `external`, `native_decide`, or `implemented_by`. |
| `python3 -m json.tool Stage1_Instances/THM-M-0424/proof-recheck-2026-07-14-head-d4bccf71.json` | 0 | The current-base structured blocker packet is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0424` | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The successful narrow Lean replay used a fresh `/tmp` output directory:

```bash
set -euo pipefail
target="$PWD/Stage1_Instances/THM-M-0424"
root="$PWD/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-0424-direct-d4bccf71.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
lean_path="$root/.lake/build/lib/lean"
for d in "$root"/.lake/packages/*/.lake/build/lib/lean; do
  lean_path="$lean_path:$d"
done
LEAN_PATH="$lean_path" "$lean" --trust=0 -t0 --root="$target" \
  -o "$tmp/Statement.olean" "$target/Statement.lean"
LEAN_PATH="$tmp:$lean_path" "$lean" --trust=0 -t0 --root="$target" \
  "$target/UniverseCounterexample-2026-07-14-head-5753c6ed.lean"
```

Pinned environment: Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; Lake manifest SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Resume only after statement repair and dependent rev-5.6 refreezing are
accepted, followed by real placeholder-free construction/group-law bodies or
an immutable compatible pinned proof. This artifact claims no proof-node state
transition, audit completion, validation, release, or master acceptance.
