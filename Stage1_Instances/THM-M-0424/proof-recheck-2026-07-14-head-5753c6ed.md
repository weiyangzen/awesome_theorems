# THM-M-0424 proof-phase recheck at head 5753c6ed

Item: `S56-M-0424-PROOF`

Intent: `prove`

Base revision: `5753c6edda31c1a6b98c5b1e6e9f8c28f0b4383b`

Base tree: `2bb3d19341e7c0465228fa7fe95232afd89a2f5f`

Recheck date: 2026-07-14 (Asia/Shanghai)

## Verdict

`blocked`. The requested positive proof cannot exist for the exact frozen Lean
target because that target is false. The new placeholder-free declaration

```text
Stage1Instances.THM_M_0424.UniverseCounterexample.not_brauerGroupStatement :
  Not Stage1Instances.THM_M_0424.BrauerGroupStatement.{1,0}
```

kernel-checks at trust level zero. A universe-polymorphic positive proof would
specialize to `{1,0}` and contradict this declaration.

For the specialization `u = 1`, `v = 0`, choose `K := Type 0 : Type 1` and
equip it with the field structure supplied by mathlib's
`Infinite.nonempty_field`. Any `BrauerGroupLawData.{1,0} K` contains
`oneRep : CSA.{1,0} K` and an algebra equivalence from its carrier in `Type 0`
to `K`. The underlying equivalence proves `Small.{0} K`, contradicting
`not_small_type : Not (Small.{0} (Type 0))`.

This is a refutation of the frozen encoding, not the classical Brauer-group
theorem. The first failed gate is exact-target consistency at
`M0424-S-BOUNDARY`, witnessed through `M0424-C-ONE`. Repair requires reopening
the statement phase, relating the field and CSA carrier universes (for example
by using `CSA.{u,u} K`), and publishing a new exact statement fingerprint,
anchor audit, obligation registry, typed graphs, and validation specs. A proof
phase worker cannot silently make that replacement.

Even after this statement repair, pinned
`Mathlib.Algebra.BrauerGroup.Defs` explicitly leaves the tensor-product
abelian group law as TODO 1. The current closure contains no terminal bodies
for the tensor-CSA construction, congruence, quotient descent, group laws, or
opposite inverse.

No positive proof body, receipt, or obligation closure was added. Lifecycle
remains `planned`; the accepted root vector remains `[H1, M3, R3]`; the proof
item remains `[ ]`; theorem completion remains false. `M5` is only the proposed
machine diagnosis for the false encoding. No audit completion, validation,
release, master acceptance, or classical-theorem refutation is claimed.

## Validation

All commands ran in this worker clone using the pre-existing pinned Lake
artifacts read-only. Lean output was confined to a fresh `/tmp` directory and
removed by a shell trap. No `lake update`, `lake build`, dependency clone or
fetch, network access, or `.lake` mutation occurred.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0424` | 0 | Rank 78; lifecycle planned; theorem incomplete. |
| Isolated trust-zero Lean recipe below | 0 | Exact target refuted at `{1,0}`; all four declarations report exactly `[propext, Classical.choice, Quot.sound]`; `assert_no_sorry` passes. |
| `python3 Stage1_Instances/THM-M-0424/check_anchor_audit.py` | 0 | Six immutable candidates classified; exact root remains M3. |
| `python3 Stage1_Instances/THM-M-0424/check_obligation_tree.py` | 0 | 18 obligations and 35 typed edges passed; denominator `83afccaebaea7322e89808dde65a4cff0cd758498ff63f70fbf8b00cf1e42a00`; root remains open M3. |
| Prohibited-construct scan of every owned `*.lean` | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, declared axiom, opaque/unsafe/external declaration, `native_decide`, or `implemented_by`. |
| `python3 -m json.tool Stage1_Instances/THM-M-0424/proof-recheck-2026-07-14-head-5753c6ed.json` | 0 | Structured blocker record parsed as valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0424` | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest deliberately absent. |

Exact Lean recipe, run from the repository root:

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
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; Lake manifest SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Because the assigned positive proof phase is not genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent. Resume only after the
statement repair and dependent rev-5.6 refreeze are accepted, followed by real
placeholder-free construction and group-law bodies or an immutable compatible
pinned proof.
