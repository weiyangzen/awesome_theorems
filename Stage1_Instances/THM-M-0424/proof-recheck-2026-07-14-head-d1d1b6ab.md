# THM-M-0424 proof recheck at `d1d1b6ab`

Item: `S56-M-0424-PROOF`

Intent: `prove`

Recorded at: `2026-07-14T02:57:19+08:00`

Base revision: `d1d1b6abb3bf227c43ebb3ce0513779bc96d6294`

Base tree: `c8009994d3b72ece76326dd39eaf0262255cb6a1`

## Verdict

`blocked`. No positive proof body can inhabit the exact frozen Lean target. The
owned, placeholder-free declaration

```text
Stage1Instances.THM_M_0424.UniverseCounterexample.not_brauerGroupStatement :
  Not Stage1Instances.THM_M_0424.BrauerGroupStatement.{1,0}
```

was replayed against this base at Lean trust level zero. Therefore a
universe-polymorphic proof of the frozen target would specialize to `{1,0}` and
contradict a kernel-checked theorem.

At this specialization, take `K := Type 0 : Type 1` with the field structure
provided by `Infinite.nonempty_field`. Any
`BrauerGroupLawData.{1,0} K` contains `oneRep : CSA.{1,0} K` and an algebra
equivalence from its carrier in `Type 0` to `K`. Its underlying equivalence
would prove `Small.{0} (Type 0)`, contradicting `not_small_type`.

This refutes only the frozen Lean encoding, not the classical Brauer-group
theorem. The first failed gate is exact-target consistency at
`S56-5.1-EXACT-TARGET-CONSISTENCY / M0424-S-BOUNDARY`, witnessed through
`M0424-C-ONE`. The statement phase must be reopened to relate the field and
representative universes, for example with `CSA.{u,u} K`. A repaired statement
requires a new expression fingerprint and a versioned refreeze of the anchor
audit, obligation registry, typed graphs, and validation specifications; this
proof worker may not silently substitute it.

There is also an independent downstream blocker. Pinned
`Mathlib.Algebra.BrauerGroup.Defs` defines the quotient but explicitly leaves
the tensor-product abelian group structure as TODO 1. The pinned closure has no
terminal bodies for tensor-CSA packaging, stable-equivalence congruence,
quotient descent, associativity, commutativity, unit, or opposite inverse.

No positive proof body or receipt was added. Lifecycle remains `planned`; the
root vector remains `[H1, M3, R3]`; the proof item remains `[ ]`; theorem
completion remains false. `M5` is only the proposed diagnosis of this frozen
encoding. This packet claims no audit completion, validation, release, master
acceptance, or refutation of the mathematical Brauer-group theorem.

## Scoped validation

All Lean checks used the automation-provided pre-existing pinned `.lake`
symlink read-only. Lean output was written to a fresh `/tmp` directory and
removed by a trap. No `lake update`, `lake build`, dependency clone/fetch,
network access, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0424` | 0 | Rank 78; lifecycle planned; theorem incomplete. |
| Isolated trust-zero Lean recipe below | 0 | The exact target was refuted at `{1,0}`; all four counterexample declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`; every `assert_no_sorry` passed. |
| `python3 Stage1_Instances/THM-M-0424/check_anchor_audit.py` | 0 | Six immutable candidates classified; exact root remains M3. |
| `python3 Stage1_Instances/THM-M-0424/check_obligation_tree.py` | 0 | 18 obligations and 35 typed edges passed; denominator `83afccaebaea7322e89808dde65a4cff0cd758498ff63f70fbf8b00cf1e42a00`; root open M3. |
| Prohibited-construct scan of all owned `*.lean` files | 0 | No `sorry`, `admit`, `sorryAx`, declared axiom, opaque/unsafe/external declaration, `native_decide`, or `implemented_by`. |
| `python3 -m json.tool Stage1_Instances/THM-M-0424/proof-recheck-2026-07-14-head-d1d1b6ab.json` | 0 | This structured blocker packet parsed as valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0424` | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

Exact Lean recipe, run from the repository root:

```bash
set -euo pipefail
target="$PWD/Stage1_Instances/THM-M-0424"
lean_root="$PWD/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-0424-d1d1b6ab.XXXXXX)
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

Because the assigned positive proof phase is not genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent. Retry only after the
statement repair and dependent refreeze are accepted, followed by real
placeholder-free construction/group-law bodies or immutable compatible pinned
proofs.
