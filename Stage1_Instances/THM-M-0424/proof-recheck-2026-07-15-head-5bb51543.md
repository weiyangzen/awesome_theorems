# THM-M-0424 proof recheck at `5bb51543`

Item: `S56-M-0424-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T07:59:35+08:00`

Base revision: `5bb515438bd0e1d53584e5243c5d434dfde7158e`

Base tree: `8055b8d863f0978f110a628ab3ccc7ab1e146b12`

## Verdict

`blocked`. A positive proof body cannot inhabit the exact frozen Lean target.
The owned, placeholder-free declaration

```text
Stage1Instances.THM_M_0424.UniverseCounterexample.not_brauerGroupStatement :
  Not Stage1Instances.THM_M_0424.BrauerGroupStatement.{1,0}
```

was replayed at Lean trust level zero against this base. A universe-polymorphic
positive proof would specialize to `{1,0}` and contradict that kernel-checked
theorem.

At this specialization, take `K := Type 0 : Type 1` with the field structure
provided by `Infinite.nonempty_field`. Any
`BrauerGroupLawData.{1,0} K` contains `oneRep : CSA.{1,0} K` and an algebra
equivalence from its carrier in `Type 0` to `K`. Its underlying equivalence
would prove `Small.{0} (Type 0)`, contradicting `not_small_type`.

This refutes only the frozen Lean encoding, not the classical Brauer-group
theorem. Exact-target consistency first fails at
`S56-5.1-EXACT-TARGET-CONSISTENCY / M0424-S-BOUNDARY`, witnessed through
`M0424-C-ONE`. Repair requires reopening the statement phase to relate the
field and representative universes, publishing a new expression fingerprint,
and refreezing all dependent artifacts. This proof worker cannot silently
substitute such a repaired target.

An independent downstream blocker remains. Pinned
`Mathlib.Algebra.BrauerGroup.Defs` explicitly leaves the tensor-product
abelian-group structure as TODO 1. The pinned dependency closure contains no
`CommGroup (BrauerGroup K)` instance or terminal bodies for tensor-CSA
packaging, stable-equivalence congruence, quotient descent, the group laws, or
the opposite-algebra inverse.

No positive proof body or receipt was added. Lifecycle remains `planned`; the
accepted root vector remains `[H1, M3, R3]`; the proof item remains `[ ]`; and
theorem completion remains false. This is the nineteenth unresolved
head-specific retry in the owned dossier. The rev-5.6 five-tick split threshold
has been exceeded, so the master or scheduler must split or reopen the invalid
statement dependency before another proof retry. This worker does not own the
execution DAG. Because the assigned phase is not complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Scoped validation

All checks ran in this worker clone. The automation-provided `.lake` symlink to
the canonical pinned artifacts was used read-only. Lean outputs were confined
to a disposable `/tmp` directory and removed after their hashes were captured.
No `lake update`, `lake build`, dependency clone or fetch, network access, or
`.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0424` | 0 | Rank 78; lifecycle planned; theorem incomplete. |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0424/check_statement.py` | 0 | Exact statement hash `62cfee70820b2f8bc4e924505b8984993322f623109868957b726b3446fc3aa8`; all four mutations killed. |
| `python3 Stage1_Instances/THM-M-0424/check_anchor_audit.py` | 0 | Six immutable candidates verified; exact root remains M3. |
| `python3 Stage1_Instances/THM-M-0424/check_obligation_tree.py` | 0 | 18 obligations and 35 typed edges passed; denominator `83afccaebaea7322e89808dde65a4cff0cd758498ff63f70fbf8b00cf1e42a00`; root open M3. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| Isolated trust-zero `lake env lean` recipe below | 0 | Exact target refuted at `{1,0}`; all four counterexample declarations reported exactly `propext`, `Classical.choice`, and `Quot.sound`; every `assert_no_sorry` passed. |
| `rg` prohibited-construct scan of all owned Lean files, excluding the identifier `assert_no_sorry` | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, declared `axiom`, `constant`, `opaque`, `unsafe`, `external`, `native_decide`, or `implemented_by`. |
| `rg -n 'CommGroup[[:space:]]*\([^\n]*BrauerGroup\|instance[^\n]*BrauerGroup' Formalizations/Lean/.lake/packages --glob '*.lean'` | 1 | Expected no-match; the audited definitions file leaves this construction open. |
| `python3 -m json.tool Stage1_Instances/THM-M-0424/proof-recheck-2026-07-15-head-5bb51543.json` | 0 | The current-base structured blocker packet parsed as valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0424` | 0 | No whitespace errors. |
| `rg -n '[[:blank:]]+$' Stage1_Instances/THM-M-0424/proof-recheck-2026-07-15-head-5bb51543.{json,md}` | 1 | Expected no-match; no trailing whitespace in either blocker deliverable. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The successful narrow Lean replay used a fresh `/tmp` output directory:

```bash
set -euo pipefail
repo="$PWD"
target="$repo/Stage1_Instances/THM-M-0424"
lean_root="$repo/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-0424-head5bb51543.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
base_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
(cd "$lean_root" && LEAN_NUM_THREADS=1 lake env lean --trust=0 -t0 \
  --root="$target" -o "$tmp/Statement.olean" "$target/Statement.lean")
(cd "$lean_root" && LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" \
  lake env lean --trust=0 -t0 --root="$target" \
  -o "$tmp/UniverseCounterexample.olean" \
  "$target/UniverseCounterexample-2026-07-14-head-5753c6ed.lean")
```

The statement output SHA-256 was
`efa2ea0ea05ce852276dd67e3abe1c6f3c705670f8c435bebcf57be1456b4e51`;
the counterexample output SHA-256 was
`c309037999d6b2be51e46f3e5a1e3ce8f67255764f213671c71f0df4696e8dcb`.
The corresponding `.olean` SHA-256 values were
`3cf07b674053f73ba89b4b05c86e12c87cece6b588f3ee71ff389db747a1c2c2`
and
`73972a794d9812a5d5398ecf4b35ab924352e1d526e1a8d77ebca72bdd5177a2`.

Pinned environment: Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; Lake manifest SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Resume only after statement repair and dependent rev-5.6 refreezing are
accepted, followed by real placeholder-free construction and group-law bodies
or an immutable compatible pinned proof. This artifact claims no proof-node
state transition, audit completion, validation, release, or master acceptance.
