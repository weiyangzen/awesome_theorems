# THM-M-0545 proof-phase recheck at base 7505614b

Item: `S56-M-0545-PROOF`

Intent: `prove`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `7505614b75de56cf10bbd196a4aaa0ca2a117064`

Base tree: `730e162a2133e4a077d764043b5e722c1f7feb39`

## Verdict

`blocked`. No positive proof body can inhabit the exact frozen Lean target in
a consistent environment. The placeholder-free declaration

```text
Stage1Instances.THMM0545.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0545.HodgeDecompositionTarget.{0, 0, 0, 0}
```

kernel-checks at trust level zero against a freshly elaborated temporary
`Statement.olean`. A universe-polymorphic proof requested by the frozen target
would specialize to universes `(0, 0, 0, 0)` and contradict this declaration.

The formal target quantifies over every `HodgeAnalyticData`, but
`realizesSmoothComplexForms` and `realizesHodgeOperators` are unconstrained
proposition fields. They impose no laws connecting the supplied form spaces,
exterior derivative, codifferential, or Laplacian to the manifold. The checked
countermodel uses the compact zero-dimensional Euclidean Riemannian manifold,
sets every form space to `Complex`, sets both differentials to zero and the
Laplacian to the identity, and makes all four proposition fields true. At
degree one, the form `1` cannot be the sum of harmonic, exact, and coexact
parts because each such part must be zero.

This refutes only the overbroad abstract encoding, not the mathematical Hodge
decomposition theorem. No positive proof body, proof receipt, composition
certificate, or frozen obligation was added or closed. The item remains
`[ ]`; lifecycle remains `planned`; audit completion, proof completion,
validation, release, theorem completion, and master acceptance remain false.
The prerequisite `S56-M-0545-OBLIGATION_TREE` is still worker-provisional
`[_]`, not master-accepted.

Because the assigned proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY` at
`M0545-S-REALIZATION`. The current registry's remaining root cut set is
`M0545-S-REALIZATION`, `M0545-A-COMPLETION`, `M0545-A-D`,
`M0545-A-ADJOINT`, `M0545-A-LAPLACIAN`, `M0545-A-ELLIPTIC`,
`M0545-A-GREEN`, `M0545-L-CLOSED-RANGES`, and `M0545-S-BOUNDARY`.

Positive proof work can resume only after an authorized statement revision
replaces the opaque realization propositions with concrete pinned definitions
or source-justified, noncircular law-bearing structures that exclude the
countermodel without assuming decomposition. That correction needs a new
accepted expression fingerprint, followed by fresh statement, anchor-audit,
obligation-tree, and proof phases in dependency order.

## Scoped Validation

All commands ran in this worker clone. No `lake update`, `lake build`,
dependency clone/fetch, network operation, or `.lake` mutation ran. The
automation-provided `Formalizations/Lean/.lake` symlink was reused read-only.
Temporary Lean objects and logs were created under `/tmp` and removed by a
shell trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0545` | 0 | Rank 105; lane `frontier_deep_formalization_debt`; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0545/check_anchor_audit.py` | 0 | `ok: target boundary, five candidate rows, 11 Lean probes, and pinned mathlib revision agree` |
| `python3 Stage1_Instances/THM-M-0545/check_obligation_tree.py` | 0 | 17 obligations and 132 typed edges passed; denominator `52a39eb0...9896e`; root remains open at `M4`. |
| Isolated explicit-path `lake env lean --trust=0 -t 0` replay below | 0 | The exact statement and universe-zero refutation elaborated. `#print axioms` reported `[propext, Classical.choice, Quot.sound]`. |
| Independent isolated replay of the same two Lean invocations | 0 | Both invocations exited 0 with identical object/log hashes and axiom output; this corroborates the blocker but is not release-grade independent verification because the pinned artifacts were shared. |
| `rg -n --pcre2 '<prohibited-token-pattern>' Stage1_Instances/THM-M-0545 --glob '*.lean'` | 1 | Expected no-match result: no prohibited proof escape occurs in the owned Lean sources. |
| `python3 -m json.tool Stage1_Instances/THM-M-0545/proof-recheck-2026-07-15-head-7505614b-slot22.json` | 0 | The structured blocker packet is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0545` | 0 | No tracked-diff whitespace diagnostics. |
| `git diff --no-index --check /dev/null <each new artifact>` | 1 each | Expected new-file difference exit; empty output for both files confirms no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The success-only manifest is absent. |

The narrow kernel replay used the existing pinned build objects directly:

```bash
set -uo pipefail
tmp=$(mktemp -d /tmp/thm-m-0545-proof-7505614b-slot22.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0545/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0545/ProofCountermodel-2026-07-14.lean \
  "$tmp/ProofCountermodel.lean"
lean_path=$(
  find -L "$PWD/Formalizations/Lean/.lake/packages" \
    "$PWD/Formalizations/Lean/.lake/build/lib/lean" \
    -path '*/build/lib/lean' -type d -print 2>/dev/null |
    sort -u | paste -sd: -
)
cd "$tmp"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$lean_path" lake env lean --trust=0 -t 0 --root="$tmp" \
  -o Statement.olean Statement.lean > statement.log 2>&1
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$lean_path" lake env lean --trust=0 -t 0 --root="$tmp" \
  ProofCountermodel.lean > proof.log 2>&1
```

The primary replay ran from `2026-07-15T14:09:17+08:00` through
`2026-07-15T14:09:30+08:00`; both Lean invocations exited `0`.
`Statement.olean` was 347208 bytes with SHA-256
`0cb3c19973217747cb7ee91bb25171d50212bdef10d4246cd1d5ccc952cb1bce`.
The statement log was 5758 bytes with SHA-256
`afcc4739ad6536f2f83577f6076cdcd38cbb3c15d867ddadac48cc5e417227a9`.
The proof log was 439 bytes with SHA-256
`ea27796c6b2205a152959ad24901f96ca03213689439e9530ab83b4ddaff6e60`.
Its exact trust result was:

```text
'Stage1Instances.THMM0545.not_hodgeDecompositionTarget' depends on axioms:
[propext, Classical.choice, Quot.sound]
```

Pinned identities: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake
`5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

The paired JSON artifact binds the current source and specification hashes,
commands and results, trust output, invalidation boundary, and proposed
fail-closed diagnosis. It is blocker evidence, not a positive proof receipt.
