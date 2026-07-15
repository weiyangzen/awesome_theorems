# THM-M-0545 proof phase blocked at `33a5b0d6` (`slot11`)

Item: `S56-M-0545-PROOF`

Intent: `prove`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `33a5b0d654c92a894e155f5385edaae684091bb0`

Base tree: `74ed89524afb3c118e31a7fce9b5763fee26b180`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen Lean
target. The existing placeholder-free declaration

```text
Stage1Instances.THMM0545.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0545.HodgeDecompositionTarget.{0, 0, 0, 0}
```

was re-elaborated at trust level zero against a fresh `Statement.olean`. A
universe-polymorphic proof of the requested positive target would specialize
to universes `(0, 0, 0, 0)` and contradict this declaration.

The defect is in the frozen encoding. `HodgeDecompositionTarget` quantifies
over every `HodgeAnalyticData`, but `realizesSmoothComplexForms` and
`realizesHodgeOperators` are unconstrained proposition fields. They impose no
laws connecting the independently supplied form spaces, exterior derivative,
codifferential, or Laplacian to the manifold.

The checked countermodel uses the compact zero-dimensional Euclidean
Riemannian manifold, interprets every form space as `Complex`, sets the
exterior derivative and codifferential to zero and the Laplacian to the
identity, and makes all four explicit propositions true. At degree one,
harmonicity forces the harmonic summand to zero, while membership in the two
zero images forces the exact and coexact summands to zero. Hence the form `1`
cannot equal their sum.

This refutes only the overbroad abstract Lean encoding, not the mathematical
Hodge decomposition theorem. Repairing, strengthening, or narrowing the
target inside this proof item would be a forbidden theorem substitution. No
positive proof body, receipt, composition certificate, or obligation closure
was added. The item remains `[ ]`; the recorded vector remains
`[H3, M4, R4]`, with `[H3, M5, R4]` only a fail-closed diagnosis proposed for
master reconciliation. Audit completion, validation, release, theorem
completion, and master acceptance remain false. The prerequisite obligation
tree is still worker-provisional (`[_]`).

Because the assigned positive proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first semantic gate is `S56-5.1-EXACT-TARGET-CONSISTENCY` at
`M0545-S-REALIZATION`. The frozen graph separately records the open analytic
cut `M0545-S-REALIZATION`, `M0545-A-COMPLETION`, `M0545-A-D`,
`M0545-A-ADJOINT`, `M0545-A-LAPLACIAN`, `M0545-A-ELLIPTIC`,
`M0545-A-GREEN`, `M0545-L-CLOSED-RANGES`, and `M0545-S-BOUNDARY`, but the
earlier statement defect blocks entry to that proof architecture.

Positive proof work can resume only after an authorized statement revision
replaces the opaque realization propositions with concrete pinned definitions
or source-justified, noncircular law-bearing structures that rule out this
countermodel without assuming the decomposition. The corrected target must
receive a new accepted expression fingerprint, followed by fresh statement,
anchor-audit, obligation-tree, and proof phases in dependency order. Repeating
proof search against the unchanged target cannot repair the contradiction.

## Validation

All checks ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was treated as read-only. No `lake update`,
`lake build`, dependency clone/fetch, checkout, repair, or network command was
run. Lean outputs existed only in fresh `/tmp` directories and were removed.

The required project entry point is currently unavailable: `lake env printenv
LEAN_PATH` cannot resolve the already-pinned `flt-regular` package because its
checkout has no resolvable `HEAD` (the manifest-pinned commit object is already
present). No fetch or repair was attempted. The
narrow fallback still used `lake env lean`, the pinned Lean 4.29.0 toolchain,
and an explicit read-only `LEAN_PATH` assembled solely from existing compiled
package directories. It validates the countermodel but is nonrelease blocker
evidence and does not make the missing pinned checkout a passing gate.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0545` | 0 | Rank 105; baseline `L0/rework_required`; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0545/check_anchor_audit.py` | 0 | Target boundary, five candidate rows, 11 Lean probes, and pinned mathlib revision agree. |
| `python3 Stage1_Instances/THM-M-0545/check_obligation_tree.py` | 0 | `PASS`: 17 obligations and 132 typed edges; denominator `52a39eb0...9896e`; root remains open at `M4`. |
| `cd Formalizations/Lean && timeout --signal=TERM --kill-after=2 8s lake env printenv LEAN_PATH` | 124 | Timed out with no output while Lake tried to resolve the incomplete `flt-regular` checkout; a separate `git rev-parse --verify HEAD` returned 128 because that checkout has no resolvable `HEAD`. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | Both modules elaborated; statement log SHA-256 `afcc4739...227a9`, proof log SHA-256 `ea27796c...6e60`, and `Statement.olean` SHA-256 `0cb3c199...b1bce`. Lean reported `[propext, Classical.choice, Quot.sound]`. |
| Independent fresh-`/tmp` replay by a separate worker | 0 | Same source, output, object hashes, byte counts, exact type, and axiom report. This is corroborating diagnostic evidence, not release independence. |
| Scoped prohibited-construct scan over owned `*.lean` | 1 (expected) | No `sorry`, `admit`, `sorryAx`, `native_decide`, `implemented_by`, bodyless declaration, unsafe declaration, or external declaration matched. |
| `python3 -m json.tool Stage1_Instances/THM-M-0545/proof-recheck-2026-07-15-head-33a5b0d6-slot11.json` | 0 | The paired blocker record parses as JSON. |
| Scoped tracked/new-file whitespace checks | 0 | No whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

The successful narrow replay, run from the repository root, was:

```bash
set -uo pipefail
tmp=$(mktemp -d /tmp/thm-m-0545-proof-33a5b0d6-slot11.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0545/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0545/ProofCountermodel-2026-07-14.lean \
  "$tmp/ProofCountermodel.lean"
root=$PWD
base="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean:$root/Formalizations/Lean/.lake/build/lib/lean"
for d in "$root"/Formalizations/Lean/.lake/packages/*/.lake/build/lib/lean; do
  if [ -d "$d" ]; then base="$base:$d"; fi
done
cd "$tmp"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$base" timeout --foreground 600 lake env lean --trust=0 -t0 \
  --root="$tmp" -o Statement.olean Statement.lean >statement.log 2>&1
statement_exit=$?
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$base" timeout --foreground 600 lake env lean --trust=0 \
  -t0 --root="$tmp" ProofCountermodel.lean >proof.log 2>&1
proof_exit=$?
sha256sum statement.log proof.log Statement.olean
wc -c statement.log proof.log Statement.olean
exit $(( statement_exit != 0 || proof_exit != 0 ))
```

The replay ran from `2026-07-15T12:35:05+08:00` through
`2026-07-15T12:35:13+08:00`; both invocations exited `0`. The statement log
was 5758 bytes, the proof log 439 bytes, and `Statement.olean` 347208 bytes.
The exact trust result was:

```text
'Stage1Instances.THMM0545.not_hodgeDecompositionTarget' depends on axioms:
[propext, Classical.choice, Quot.sound]
```

Pinned environment: Linux `7.0.0-27-generic` `x86_64`; Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake
`5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

This artifact is fresh negative nonrelease evidence. It is not a positive
proof receipt, does not satisfy `S56-M-0545-PROOF`, proposes no provisional or
accepted task state, and supports neither audit nor theorem completion.
