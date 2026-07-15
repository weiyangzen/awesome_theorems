# THM-M-0424 proof-phase recheck at current base

Item: `S56-M-0424-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `9e1db93a3c4b869cc7c1f8ac99b6c1b12cb4c82c`

Base tree: `0499e20448fdcec5b57b47cc034570b35aab32a1`

Worker automation clone: `slot19`.

At preflight the tracked owned path was clean. The sole pre-existing worktree entry was the
automation-provided untracked `Formalizations/Lean/.lake` symlink to the canonical dependency
cache. This worker treated the cache as read-only and did not update, build, clone, fetch,
checkout, or repair it. The cache's `flt-regular` checkout presently has no resolvable `HEAD`, so
the required `lake env lean` entry point stops before Lean starts. A direct trust-zero diagnostic
replay used only the installed pinned Lean executable and existing compiled library directories;
its outputs were confined to `/tmp` and removed. This packet is blocker evidence, not release
evidence.

## Verdict

`blocked`. A placeholder-free positive proof of the exact frozen target cannot exist in this
consistent Lean environment. The existing repo-local declaration

```text
Stage1Instances.THM_M_0424.UniverseCounterexample.not_brauerGroupStatement :
  Not Stage1Instances.THM_M_0424.BrauerGroupStatement.{1,0}
```

elaborates under `--trust=0` against a newly generated temporary `Statement.olean`. Any positive
universe-polymorphic proof would specialize to `{1,0}` and contradict this declaration.

At that specialization, take `K := Type 0 : Type 1` with the field structure supplied by
`Infinite.nonempty_field`. Any `BrauerGroupLawData.{1,0} K` contains
`oneRep : CSA.{1,0} K` and an algebra equivalence from its carrier in `Type 0` to `K`. The
underlying equivalence proves `Small.{0} (Type 0)`, contradicting `not_small_type`.

This refutes the frozen Lean encoding, not the classical Brauer-group theorem. Exact-target
consistency first fails at `S56-5.1-EXACT-TARGET-CONSISTENCY / M0424-S-BOUNDARY`, witnessed through
`M0424-C-ONE`. Adding a universe relation now would change the accepted statement fingerprint and
all dependent frozen artifacts, which this proof-only worker may not substitute silently.

An independent downstream blocker remains. Pinned `Mathlib.Algebra.BrauerGroup.Defs` explicitly
leaves the tensor-product abelian group structure as TODO 1. The pinned closure contains no
`CommGroup (BrauerGroup K)` instance or terminal bodies for tensor-CSA packaging,
stable-equivalence congruence, quotient descent, the group laws, or the opposite-algebra inverse.
The checked `brauerGroupStatement_of_lawData` declaration is only a conditional identity adapter;
it does not inhabit `BrauerGroupLawData` and receives no root closure credit.

No positive proof body, receipt, graph closure, or accepted debt change was added. The item remains
`[ ]`, lifecycle remains `planned`, the provisional root vector remains `[H1, M3, R3]`, and theorem
completion remains false. Twenty-four prior unresolved proof recheck pairs existed at preflight;
this is retry 25. The rev-5.6 five-tick split threshold has long been exceeded, so the master or
scheduler must reopen the invalid statement dependency and split or reconcile this proof item
rather than schedule another identical proof-only retry. This worker did not edit the DAG or
generated checklist. Because the assigned phase is incomplete, `.stage1-worker-selftest.json` is
deliberately absent.

## Failed Gate And Retry

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY / M0424-S-BOUNDARY`. Repair must start by
reopening `S56-M-0424-STATEMENT`, relating the field and representative carrier universes, accepting
a new exact statement fingerprint, and refreezing the obligation registry and typed graphs. The
remaining construction/law cut includes `M0424-C-TENSOR-ALG`, `M0424-C-TENSOR-CSA`,
`M0424-C-TENSOR-CONGR`, `M0424-C-ONE`, `M0424-C-OPPOSITE`, `M0424-L-DESCENT`,
`M0424-L-ASSOC`, `M0424-L-COMM`, `M0424-L-UNIT`, and `M0424-L-INVERSE`.

Resume positive proof execution only after the corrected statement architecture is accepted and
real placeholder-free bodies for those packages exist locally, or an immutable compatible Lean 4
terminal proof is integrated. Independently restore the manifest-pinned `flt-regular` checkout so
ordinary `lake env lean` validation is available without dependency mutation.

## Validation

No `lake update`, `lake build`, dependency clone/fetch, checkout, repair, or network operation was
run. The direct diagnostic is narrower than the required Lake entry point and is not presented as
a substitute for a passing pinned `lake env lean` recipe.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0424` | 0 | Rank 78; lifecycle planned; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0424/check_anchor_audit.py` (first probe) | 1 | The shared mathlib status was transiently nonempty, so the clean-check assertion failed and no pass was credited; this worker made no cache change. |
| `python3 Stage1_Instances/THM-M-0424/check_anchor_audit.py` (clean-state retry) | 0 | Six immutable candidates verified; exact root remains M3. |
| `python3 Stage1_Instances/THM-M-0424/check_obligation_tree.py` | 0 | 18 obligations and 35 typed edges passed; denominator `83afccaebaea7322e89808dde65a4cff0cd758498ff63f70fbf8b00cf1e42a00`; root open M3. |
| `cd Formalizations/Lean && timeout --foreground 60 python3 ../../Stage1_Instances/THM-M-0424/check_statement.py` | 1 | Ordinary-Lake check failed because shared `flt-regular` could not resolve `HEAD`; no checker pass is credited. |
| `cd Formalizations/Lean && timeout --foreground 30 lake env lean --version` | 1 | Lake failed because shared `flt-regular` could not resolve `HEAD`; no ordinary-Lake result is credited. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 128 | Shared checkout has no resolvable `HEAD`; this worker did not change or repair it. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular cat-file -t 56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` | 0 | The manifest-pinned commit object is present despite the invalid checkout state. |
| Direct pinned-Lean trust-zero recipe below | 0 | Exact target refuted at `{1,0}`; all four counterexample declarations reported exactly `propext`, `Classical.choice`, and `Quot.sound`; every `assert_no_sorry` passed. |
| Scoped prohibited-construct scan of all owned Lean files | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, declared `axiom`, `constant`, `opaque`, `unsafe`, `external`, `native_decide`, or `implemented_by`. |
| Search for a `CommGroup (BrauerGroup ...)` instance in the pinned dependency closure | 1 | Expected no-match; the audited definitions file still leaves this construction open. |
| `python3 -m json.tool` on the current blocker packet | 0 | The structured blocker packet parsed as valid JSON. |
| `git diff --check --no-index` for each new blocker artifact | 1 | Expected no-index difference status with no diagnostic output; both files have no whitespace errors. |
| Trailing-whitespace scan of both new blocker artifacts | 1 | Expected no-match. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The successful supporting replay used:

```bash
set -euo pipefail
repo="$PWD"
target="$repo/Stage1_Instances/THM-M-0424"
tmp=$(mktemp -d /tmp/thm-m-0424-head9e1db93a-direct.XXXXXX)
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
`efa2ea0ea05ce852276dd67e3abe1c6f3c705670f8c435bebcf57be1456b4e51`; the counterexample output
SHA-256 was `c309037999d6b2be51e46f3e5a1e3ce8f67255764f213671c71f0df4696e8dcb`. The corresponding
`.olean` SHA-256 values were `3cf07b674053f73ba89b4b05c86e12c87cece6b588f3ee71ff389db747a1c2c2`
and `73972a794d9812a5d5398ecf4b35ab924352e1d526e1a8d77ebca72bdd5177a2`.

Pinned environment: Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lean binary SHA-256
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`; mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; Lake manifest SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

This artifact claims no proof-node state transition, audit completion, validation, release, or
master acceptance.
