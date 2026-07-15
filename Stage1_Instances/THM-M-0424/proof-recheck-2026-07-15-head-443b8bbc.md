# THM-M-0424 proof recheck at `443b8bbc`

Item: `S56-M-0424-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T11:39:12+08:00`

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

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
abelian-group structure as TODO 1. The current source search found no
`CommGroup (BrauerGroup K)` instance, and the bounded pinned anchor audit found
no compatible terminal bodies for tensor-CSA packaging, stable-equivalence
congruence, quotient descent, the group laws, or the opposite-algebra inverse.

No positive proof body or receipt was added. Lifecycle remains `planned`; the
provisional anchor/obligation-tree vector remains `[H1, M3, R3]`; the proof
item remains `[ ]`; and theorem completion remains false. This is the
twenty-third unresolved head-specific retry recorded in the owned dossier.
The rev-5.6 five-tick split threshold has been exceeded, so the master or
scheduler must split or reopen the invalid statement dependency before another
proof retry. This worker does not own the execution DAG. Because the assigned
phase is not complete, `.stage1-worker-selftest.json` is deliberately absent.

## Scoped validation

All checks ran in this worker clone. The automation-provided `.lake` symlink to
the canonical pinned artifacts was treated as read-only. No `lake update`,
`lake build`, dependency clone/fetch, checkout, or repair command was issued.
The failed required `lake env` probe entered Lake dependency resolution while
the shared cache was being changed concurrently, so this run cannot truthfully
attest that the failed probe caused no network or cache side effect; it was
interrupted and no result from it is credited. The shared canonical
`flt-regular` package checkout was left with
`.git/HEAD -> refs/heads/.invalid`; its pinned commit object is present, but the
checkout has no resolvable `HEAD`. Consequently ordinary `lake env` validation
was unavailable and was recorded as a current shared-artifact failure rather
than repaired or fetched by this worker.

The theorem-specific trust-zero replay was still possible read-only by invoking
the exact pinned Lean binary directly and constructing `LEAN_PATH` exclusively
from the existing pinned build directories. Outputs went to a disposable
`/tmp` directory and were removed by a trap. This direct replay is supporting
kernel evidence; it does not pretend that the required ordinary Lake gate
passed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0424` | 0 | Rank 78; lifecycle planned; theorem incomplete. |
| `git status --short` | 0 | Before editing, only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present; the owned path was clean. |
| `cd Formalizations/Lean && lake env lean --version` | 130 | Manually stopped after about 100 seconds with no output while Lake was blocked in dependency resolution against the concurrently damaged shared `flt-regular` checkout; no version result is credited. |
| `cd Formalizations/Lean && timeout 300 python3 ../../Stage1_Instances/THM-M-0424/check_statement.py` | 1 | Current ordinary-Lake check failed with `error: external command 'git' exited with code 255`; no statement-checker pass is credited for this run. |
| `python3 Stage1_Instances/THM-M-0424/check_anchor_audit.py` | 0 | Six immutable candidates verified; exact root remains M3. |
| `python3 Stage1_Instances/THM-M-0424/check_obligation_tree.py` | 0 | 18 obligations and 35 typed edges passed; denominator `83afccaebaea7322e89808dde65a4cff0cd758498ff63f70fbf8b00cf1e42a00`; root open M3. |
| Direct pinned-Lean trust-zero recipe below | 0 | Exact target refuted at `{1,0}`; all four counterexample declarations reported exactly `propext`, `Classical.choice`, and `Quot.sound`; every `assert_no_sorry` passed. |
| Scoped prohibited-construct scan of all owned Lean files | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, declared `axiom`, `constant`, `opaque`, `unsafe`, `external`, `native_decide`, or `implemented_by`. |
| Search for a `CommGroup (BrauerGroup ...)` instance in the pinned dependency closure | 1 | Expected no-match; the audited definitions file still leaves this construction open. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 128 | Shared checkout has no resolvable `HEAD`; it was not changed or repaired by this worker. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular cat-file -t 56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` | 0 | The manifest-pinned commit object is present despite the invalid checkout state. |
| `python3 -m json.tool Stage1_Instances/THM-M-0424/proof-recheck-2026-07-15-head-443b8bbc.json` | 0 | The current-base structured blocker packet parsed as valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0424` | 0 | No whitespace errors in tracked diffs; the two new untracked deliverables were separately covered by a trailing-whitespace scan. |
| `rg -n '[[:blank:]]+$' Stage1_Instances/THM-M-0424/proof-recheck-2026-07-15-head-443b8bbc.{json,md}` | 1 | Expected no-match; no trailing whitespace in either blocker deliverable. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The successful supporting replay used:

```bash
set -euo pipefail
repo="$PWD"
target="$repo/Stage1_Instances/THM-M-0424"
tmp=$(mktemp -d /tmp/thm-m-0424-head443b8bbc-direct.XXXXXX)
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
or an immutable compatible pinned proof. Restore the canonical pinned Lake
artifact separately before requiring an ordinary `lake env lean` replay. This
artifact claims no proof-node state transition, audit completion, validation,
release, or master acceptance.
