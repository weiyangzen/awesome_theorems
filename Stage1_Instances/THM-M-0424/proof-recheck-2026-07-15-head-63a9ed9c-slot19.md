# THM-M-0424 proof recheck at `63a9ed9c`

Item `S56-M-0424-PROOF` is **blocked**. This current-base handoff adds no
positive proof body and deliberately emits no `.stage1-worker-selftest.json`.
The direct dependency `S56-M-0424-OBLIGATION_TREE` is only provisional `[_]`,
not master-accepted `[x]`.

## First failed gate

The frozen Lean target is false. `Statement.lean` quantifies the field universe
`u` and central-simple-algebra carrier universe `v` independently, while
`BrauerGroupLawData.oneRep_equiv_base` requires an equivalence between the
`Type v` carrier of `oneRep` and `K : Type u`. At `{u, v} = {1, 0}`, take the
field on `K := Type 0 : Type 1` supplied by `Infinite.nonempty_field`. The
equivalence would imply `Small.{0} (Type 0)`, contradicting `not_small_type`.

The existing placeholder-free declaration
`Stage1Instances.THM_M_0424.UniverseCounterexample.not_brauerGroupStatement`
therefore has exact type
`Not Stage1Instances.THM_M_0424.BrauerGroupStatement.{1,0}`. A positive body
for the universe-polymorphic frozen target cannot exist in this foundation.
Changing the target to matched universes here would substitute a different
theorem and is outside this proof item's ownership.

This is `S56-5.1-EXACT-TARGET-CONSISTENCY / M0424-S-BOUNDARY`, exposed through
`M0424-C-ONE`. The proposed machine diagnosis is `M5`; the authoritative
frozen graph remains unchanged at `[H1, M3, R3]` pending master action.

## Secondary blockers

Pinned `Mathlib.Algebra.BrauerGroup.Defs` defines `CSA`, stable Brauer
equivalence, its setoid, and the quotient `BrauerGroup`. Its module header
explicitly lists the tensor-product abelian-group law as TODO 1. A scoped
source search found no `CommGroup (BrauerGroup K)` implementation. Thus even
a repaired statement still needs placeholder-free bodies for tensor-CSA,
congruence, descent, associativity, commutativity, unit, opposite, and inverse
obligations.

Ordinary `lake env lean` is currently unavailable because the shared canonical
`flt-regular` checkout cannot resolve `HEAD`. The manifest-pinned commit object
is present. This worker did not update, build, clone, fetch, check out, repair,
or otherwise mutate `.lake`; it instead replayed the counterexample with the
exact pinned Lean binary and existing read-only package oleans in a disposable
`/tmp` directory.

## Commands and results

| Command | Exit/result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0; 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0; 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0424` | 0; rank 78, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0424/check_anchor_audit.py` | 0; six immutable candidates verified; exact root remains M3 |
| `python3 Stage1_Instances/THM-M-0424/check_obligation_tree.py` | 0; 18 obligations and 35 typed edges passed; root remains open M3 |
| `cd Formalizations/Lean && timeout --foreground 60 lake env lean --version` | 1; shared `flt-regular` checkout could not resolve `HEAD`; no Lake result credited |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 128; unresolved; not repaired |
| `git -C Formalizations/Lean/.lake/packages/flt-regular cat-file -t 56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` | 0; pinned commit object exists |
| Direct pinned-Lean trust-zero recipe below | 0; exact target refuted at `{1,0}`; all four declarations reported exactly `propext`, `Classical.choice`, and `Quot.sound`; every `assert_no_sorry` passed |
| Scoped prohibited-construct scan of all owned Lean files | 1; expected no-match |
| Search for a `CommGroup (BrauerGroup ...)` instance in the pinned closure | 1; expected no-match |
| `python3 -m json.tool` on this blocker packet | 0; parsed as valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0424 .stage1-worker-selftest.json` | 0; no whitespace errors |
| Trailing-whitespace scan of both new blocker artifacts | 1; expected no-match |
| `test ! -e .stage1-worker-selftest.json` | 0; completion self-test manifest deliberately absent |

The successful supporting replay used:

```bash
set -euo pipefail
repo="$PWD"
target="$repo/Stage1_Instances/THM-M-0424"
tmp=$(mktemp -d /tmp/thm-m-0424-head63a9ed9c-direct.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
base=$(printf '%s:' "$repo"/Formalizations/Lean/.lake/packages/\
{Cli,batteries,Qq,aesop,proofwidgets,importGraph,LeanSearchClient,plausible,checkdecls,mathlib}/.lake/build/lib/lean)
base=${base%:}
LEAN_PATH="$base" LEAN_NUM_THREADS=1 timeout --foreground 600 \
  "$lean" --trust=0 -t0 --root="$target" \
  -o "$tmp/Statement.olean" "$target/Statement.lean" \
  >"$tmp/statement-output.txt" 2>&1
LEAN_PATH="$tmp:$base" LEAN_NUM_THREADS=1 timeout --foreground 600 \
  "$lean" --trust=0 -t0 --root="$target" \
  -o "$tmp/UniverseCounterexample.olean" \
  "$target/UniverseCounterexample-2026-07-14-head-5753c6ed.lean" \
  >"$tmp/counterexample-output.txt" 2>&1
```

The statement output SHA-256 is
`efa2ea0ea05ce852276dd67e3abe1c6f3c705670f8c435bebcf57be1456b4e51`;
the counterexample output SHA-256 is
`c309037999d6b2be51e46f3e5a1e3ce8f67255764f213671c71f0df4696e8dcb`.
The corresponding `.olean` SHA-256 values are
`3cf07b674053f73ba89b4b05c86e12c87cece6b588f3ee71ff389db747a1c2c2`
and `73972a794d9812a5d5398ecf4b35ab924352e1d526e1a8d77ebca72bdd5177a2`.

## Retry condition

Reopen the statement phase, relate the field and carrier universes, and issue
a new accepted expression fingerprint plus versioned obligation artifacts.
Split the proof work because the five-unresolved-tick threshold has long been
exceeded. After the repaired dependency is master-accepted, resume only when
the missing tensor-product and group-law packages can be implemented locally
without placeholders or pinned from an immutable compatible proof. Restore the
canonical pinned Lake artifact before ordinary `lake env` validation.

This packet is nonrelease blocker evidence only. It claims no proof-node state
transition, audit completion, theorem completion, validation, release, or
master acceptance.
