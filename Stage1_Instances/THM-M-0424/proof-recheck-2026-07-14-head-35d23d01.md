# THM-M-0424 proof recheck at `35d23d01`

Item: `S56-M-0424-PROOF`

Date: `2026-07-14T02:42:52+08:00`

Base revision: `35d23d0193cd7c8fccb1d09f22534c6eba066b02`

Base tree: `4325d20b5ec8db888f28fcedc79cc1b7745c0c68`

## Verdict

`blocked`. No positive proof can exist for the exact frozen Lean target. The
already-owned placeholder-free declaration

```text
Stage1Instances.THM_M_0424.UniverseCounterexample.not_brauerGroupStatement :
  Not Stage1Instances.THM_M_0424.BrauerGroupStatement.{1,0}
```

kernel-checks at trust level zero. A universe-polymorphic positive proof would
specialize to `{1,0}` and contradict it.

At `u = 1`, `v = 0`, take `K := Type 0 : Type 1` with the field structure
provided by `Infinite.nonempty_field`. Any
`BrauerGroupLawData.{1,0} K` contains `oneRep : CSA.{1,0} K` and an algebra
equivalence from its carrier in `Type 0` to `K`. The underlying equivalence
would prove `Small.{0} (Type 0)`, contradicting `not_small_type`.

This refutes the frozen encoding, not the classical Brauer-group theorem. The
first failed gate is exact-target consistency at `M0424-S-BOUNDARY`, witnessed
through `M0424-C-ONE`. The statement phase must be reopened to relate the field
and representative universes, followed by a new statement fingerprint and a
versioned refreeze of the anchor audit, obligation registry, typed graphs, and
validation specs. A proof worker cannot silently substitute that repaired
target.

There is an independent downstream blocker even after statement repair.
Pinned `Mathlib.Algebra.BrauerGroup.Defs` defines the CSA quotient but
explicitly leaves the tensor-product abelian group structure as TODO 1. The
pinned dependency closure has no terminal bodies for tensor-CSA packaging,
stable-equivalence congruence, quotient descent, the group laws, or the
opposite-algebra inverse.

No positive proof body or receipt was added. Lifecycle remains `planned`, the
root vector remains `[H1, M3, R3]`, and theorem completion remains false.
Because this proof phase cannot be genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All validation reused the automation-provided pinned Lake artifacts read-only.
No `lake update`, `lake build`, dependency clone/fetch, network access, or
`.lake` mutation was performed. The untracked `.lake` symlink makes this
nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0424` | 0 | Rank 78; lifecycle planned; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0424/check_anchor_audit.py` | 0 | Six immutable candidates classified; exact root remains M3 |
| `python3 Stage1_Instances/THM-M-0424/check_obligation_tree.py` | 0 | 18 obligations and 35 typed edges passed; denominator `83afccaebaea7322e89808dde65a4cff0cd758498ff63f70fbf8b00cf1e42a00`; root open M3 |
| Isolated trust-zero Lean recipe below | 0 | Exact target refuted at `{1,0}`; all four counterexample declarations report `[propext, Classical.choice, Quot.sound]`; `assert_no_sorry` passes |
| Prohibited-construct scan of every owned `*.lean` | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, declared axiom, opaque/unsafe/external declaration, `native_decide`, or `implemented_by` |
| JSON parse of the current-base blocker | 0 | Structured record is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0424` | 0 | No whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest deliberately absent |

The narrow Lean replay uses a disposable output directory. The successful
current run invoked the pinned executable directly with `LEAN_PATH` assembled
from the existing pinned Lake package outputs; this is equivalent to the
following ordinary `lake env` recipe, which was also independently replayed in
this clone:

```bash
set -euo pipefail
target="$PWD/Stage1_Instances/THM-M-0424"
lean_root="$PWD/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-0424-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
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
accepted, then after real placeholder-free construction/group-law bodies or an
immutable compatible pinned proof become available. This artifact claims no
proof-node completion, scheduler state, audit completion, validation, release,
or master acceptance.
