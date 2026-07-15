# THM-M-0545 proof-phase recheck at base 3a40b196

Item: `S56-M-0545-PROOF`

Intent: `prove`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `3a40b1969f841e07036db5c4d7f03e97c7c57949`

Base tree: `404cccc598c2d4c8831d55138df788f0438ddce8`

## Verdict

`blocked`. No positive proof body can inhabit the exact frozen Lean target.
The existing placeholder-free declaration

```text
Stage1Instances.THMM0545.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0545.HodgeDecompositionTarget.{0, 0, 0, 0}
```

kernel-checks at trust level zero against a freshly elaborated temporary
`Statement.olean`. A universe-polymorphic proof of the requested target would
specialize to universes `(0, 0, 0, 0)` and contradict this declaration.

The failure is in the frozen encoding. `HodgeDecompositionTarget` quantifies
over every `HodgeAnalyticData`, while `realizesSmoothComplexForms` and
`realizesHodgeOperators` are unconstrained proposition fields. They impose no
laws connecting the form spaces, exterior derivative, codifferential, or
Laplacian to the manifold.

The checked countermodel specializes to the compact zero-dimensional
Euclidean Riemannian manifold. It takes `Complex` as every form space, sets the
exterior derivative and codifferential to zero and the Laplacian to the
identity, and makes all four explicit proposition fields true. At degree one,
harmonicity forces the harmonic summand to zero, while the two zero images
force the exact and coexact summands to zero. Thus the form `1` cannot equal
their sum.

This refutes only the overbroad abstract encoding, not the mathematical Hodge
decomposition theorem. No positive proof body, receipt, composition
certificate, or frozen obligation was added or closed. The proof item remains
`[ ]`; the recorded root vector remains `[H3, M4, R4]`, with
`[H3, M5, R4]` only a fail-closed diagnosis proposed for master
reconciliation. Audit completion, validation, release, theorem completion,
and master acceptance remain false. The predecessor obligation-tree item is
worker-provisional (`[_]`) rather than master-accepted.

Because the assigned proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY` at
`M0545-S-REALIZATION`. Dependency acceptance is also pending because
`S56-M-0545-OBLIGATION_TREE` remains `[_]`; concurrency permits this
provisional diagnostic work, but not proof closure.

The frozen graph's remaining root cut set is `M0545-S-REALIZATION`,
`M0545-A-COMPLETION`, `M0545-A-D`, `M0545-A-ADJOINT`,
`M0545-A-LAPLACIAN`, `M0545-A-ELLIPTIC`, `M0545-A-GREEN`,
`M0545-L-CLOSED-RANGES`, and `M0545-S-BOUNDARY`. Repairing the statement
invalidates that graph and requires it to be refrozen.

Positive proof work can resume only after an authorized statement revision
replaces the opaque realization propositions with concrete pinned definitions
or source-justified, noncircular law-bearing structures that rule out this
record without assuming the desired decomposition. The corrected target must
receive a new accepted expression fingerprint, followed by fresh statement,
anchor-audit, obligation-tree, and proof phases in dependency order. Repeating
proof search against the current fingerprint is not an actionable retry.

## Scoped Validation

The two exact Lean checks ran in a fresh temporary directory with no Lake
workspace file. They used `lake env lean`, the fixed pinned toolchain, and an
explicit `LEAN_PATH` assembled solely from already-present canonical
`build/lib/lean` directories. The worker issued no `lake update`, `lake build`,
clone, fetch, or write command against `.lake`; temporary objects and logs
were removed by a trap.

The shared canonical Lake workspace was not stable enough for release
evidence. Its `flt-regular` checkout had `HEAD -> refs/heads/.invalid`, and a
project-root `lake env lean --version` failed before Lean. Concurrent shared
package activity changed `FETCH_HEAD` and objects during the run, so whole-run
network/mutation state is unknown. `flt-regular` is not imported by the two
checked files and was unnecessary for their explicit isolated `LEAN_PATH`, so
this incident does not erase the narrow kernel refutation; it does prohibit a
full workspace, dependency-closure, or release claim.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0545` | 0 | Rank 105; lane `frontier_deep_formalization_debt`; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0545/check_anchor_audit.py` | 0 | `ok: target boundary, five candidate rows, 11 Lean probes, and pinned mathlib revision agree` |
| `python3 Stage1_Instances/THM-M-0545/check_obligation_tree.py` | 0 | 17 obligations and 132 typed edges passed; denominator `52a39eb0...9896e`; root remains open at `M4`. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | The exact statement and universe-zero refutation elaborated; `#print axioms` reported `[propext, Classical.choice, Quot.sound]`. |
| `(cd Formalizations/Lean && timeout --foreground 120 lake env lean --version)` | 1 | Shared `flt-regular` package could not resolve `HEAD`; full workspace validation unavailable. |
| `rg -n --pcre2 '<forbidden-pattern>' Stage1_Instances/THM-M-0545 --glob '*.lean'` | 1 | Expected no-match result: zero prohibited proof escapes. |
| `python3 -m json.tool Stage1_Instances/THM-M-0545/proof-recheck-2026-07-15-head-3a40b196.json` | 0 | The structured blocker record is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0545` | 0 | No diff whitespace diagnostics. |
| `git diff --no-index --check /dev/null <each new artifact>` | 1 each | Expected new-file difference exits with empty output, so both new files have no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion manifest is absent because the proof phase is blocked. |

Exact isolated Lean recipe, run from the repository root:

```bash
set -uo pipefail
tmp=$(mktemp -d /tmp/thm-m-0545-proof-3a40b196-final.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0545/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0545/ProofCountermodel-2026-07-14.lean \
  "$tmp/ProofCountermodel.lean"
root=$PWD
base="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean:$root/Formalizations/Lean/.lake/build/lib/lean"
for d in "$root"/Formalizations/Lean/.lake/packages/*/.lake/build/lib/lean; do
  base="$base:$d"
done
cd "$tmp"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$base" timeout --foreground 600 lake env lean --trust=0 -t0 \
  --root="$tmp" -o Statement.olean Statement.lean > statement.log 2>&1
statement_exit=$?
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$base" timeout --foreground 600 lake env lean --trust=0 \
  -t0 --root="$tmp" ProofCountermodel.lean > proof.log 2>&1
proof_exit=$?
sha256sum statement.log proof.log Statement.olean
wc -c statement.log proof.log Statement.olean
exit $(( statement_exit != 0 || proof_exit != 0 ))
```

The primary replay ran from `2026-07-15T12:18:44+08:00` through
`2026-07-15T12:18:57+08:00`; both Lean invocations exited `0`. The statement
log was 5758 bytes with SHA-256
`afcc4739ad6536f2f83577f6076cdcd38cbb3c15d867ddadac48cc5e417227a9`.
The proof log was 439 bytes with SHA-256
`ea27796c6b2205a152959ad24901f96ca03213689439e9530ab83b4ddaff6e60`.
The temporary `Statement.olean` was 347208 bytes with SHA-256
`0cb3c19973217747cb7ee91bb25171d50212bdef10d4246cd1d5ccc952cb1bce`.
The exact trust result was:

```text
'Stage1Instances.THMM0545.not_hodgeDecompositionTarget' depends on axioms:
[propext, Classical.choice, Quot.sound]
```

A separate read-only worker independently audited the proof and repeated both
commands in another fresh temporary directory. It obtained the same exits,
byte counts, hashes, and axiom report. This is corroborating nonrelease
evidence, not the independent clean-runner evidence required for release.

Pinned environment: Linux `7.0.0-27-generic` `x86_64`; Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake
`5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

The paired JSON artifact binds the task and obligation IDs, current immutable
base, source hashes, environment, commands, output hashes, trust result,
failure boundary, secondary environment incident, and retry condition. This
is fresh negative nonrelease evidence, not a positive proof receipt.
