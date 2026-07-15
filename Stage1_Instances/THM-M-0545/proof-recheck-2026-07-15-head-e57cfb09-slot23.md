# THM-M-0545 proof-phase recheck at base e57cfb09

Item: `S56-M-0545-PROOF`

Intent: `prove`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `e57cfb0904e8a827b17320aba51bd41b96109c7c`

Base tree: `79ab3544eee575a45c51d85923144ed20f607f9e`

## Verdict

`blocked`. No positive proof body can inhabit the exact frozen Lean target.
Two independent, placeholder-free countermodels kernel-check at trust level
zero against a freshly elaborated `Statement.olean`:

```text
Stage1Instances.THMM0545.not_hodgeDecompositionTarget_degreeZero :
  Not Stage1Instances.THMM0545.HodgeDecompositionTarget.{0, 0, 0, 0}

Stage1Instances.THMM0545.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0545.HodgeDecompositionTarget.{0, 0, 0, 0}
```

The first contradiction is at the degree-zero boundary. The frozen `IsExact`
predicate requires a natural `j` with `j + 1 = k`, so it has no inhabitant at
`k = 0`. Nevertheless, `HasUniqueDecomposition` requires an exact summand for
every `k`, and the root quantifies over all natural degrees.

The second contradiction is at the realization boundary. The root quantifies
over every `HodgeAnalyticData`, while `realizesSmoothComplexForms` and
`realizesHodgeOperators` are unconstrained proposition fields. They impose no
laws on the supplied form spaces or operators. A realization with `Complex`
forms, zero exterior derivative and codifferential, and identity Laplacian
satisfies all four proposition hypotheses but cannot decompose the degree-one
form `1`.

A universe-polymorphic proof of the requested positive target would specialize
to universes `(0, 0, 0, 0)` and contradict either checked declaration. These
countermodels refute only the overbroad abstract Lean encoding, not the
mathematical Hodge decomposition theorem.

No positive proof body, proof receipt, composition certificate, or obligation
closure was added. The proof item remains `[ ]`; the recorded root remains
`[H3, M4, R4]`. `[H3, M5, R4]` is only a fail-closed diagnosis proposed for
master reconciliation. The predecessor obligation-tree item remains
worker-provisional `[_]`, so the dependency gate also remains open. Audit
completion, validation, release, theorem completion, and master acceptance are
false. Because the assigned phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY` at
`M0545-S-BOUNDARY`. The independent realization failure is
`M0545-S-REALIZATION`. The actionable reopen set is
`S56-M-0545-STATEMENT`, `M0545-S-BOUNDARY`, `M0545-S-REALIZATION`, and
`M0545-ROOT`.

The frozen graph's remaining root cut set is `M0545-S-REALIZATION`,
`M0545-A-COMPLETION`, `M0545-A-D`, `M0545-A-ADJOINT`,
`M0545-A-LAPLACIAN`, `M0545-A-ELLIPTIC`, `M0545-A-GREEN`,
`M0545-L-CLOSED-RANGES`, and `M0545-S-BOUNDARY`.

Positive proof work can resume only after an authorized statement revision:

1. repair degree-zero exactness so the zero exact summand is representable;
2. replace the opaque realization propositions with concrete pinned
   definitions or source-justified, noncircular law-bearing structures; and
3. accept a new target fingerprint, then rerun statement, anchor-audit,
   obligation-tree, and proof phases in dependency order.

The statement repair invalidates the current graph and requires a refreeze.

## Scoped Validation

All commands ran in this worker clone against the existing pinned Lake
artifacts. The automation-provided untracked `Formalizations/Lean/.lake`
symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network operation, or `.lake` mutation ran. Temporary Lean
objects and logs were confined to a fresh `mktemp` directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0545` | 0 | Rank 105; lane `frontier_deep_formalization_debt`; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0545/check_anchor_audit.py` | 0 | `ok: target boundary, five candidate rows, 11 Lean probes, and pinned mathlib revision agree` |
| `python3 Stage1_Instances/THM-M-0545/check_obligation_tree.py` | 0 | 17 obligations and 132 typed edges passed; denominator `52a39eb0...9896e`; root remains open at `M4`. |
| Isolated trust-zero Lean recipe below | 0 | Statement and both universe-zero refutations elaborated; all three Lean exits were `0`. |
| `rg -n --pcre2 '\\b(?:sorry\|admit\|sorryAx\|native_decide\|implemented_by)\\b\|^[[:space:]]*(?:axiom\|opaque\|constant\|unsafe\|external)\\b' Stage1_Instances/THM-M-0545 --glob '*.lean'` | 1 | Expected no-match result: no prohibited escape occurs in owned Lean sources. |
| Pinned-mathlib Hodge/codifferential/coexact source scan | 1 | Expected no-match result: no exact positive closure was found. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion manifest is absent. |

Exact isolated Lean recipe, run from the repository root:

```bash
set -uo pipefail
tmp=$(mktemp -d /tmp/thm-m-0545-proof-e57cfb09-slot23.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0545/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0545/ProofBoundaryCountermodel-2026-07-15.lean \
  "$tmp/ProofBoundaryCountermodel.lean"
cp Stage1_Instances/THM-M-0545/ProofCountermodel-2026-07-14.lean \
  "$tmp/ProofCountermodel.lean"
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
lean_bin=$(cd Formalizations/Lean && lake env which lean)
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$lean_path" "$lean_bin" --trust=0 -t0 --root="$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean" > "$tmp/statement.log" 2>&1
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$lean_path" "$lean_bin" --trust=0 -t0 --root="$tmp" \
  "$tmp/ProofBoundaryCountermodel.lean" > "$tmp/boundary.log" 2>&1
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$lean_path" "$lean_bin" --trust=0 -t0 --root="$tmp" \
  "$tmp/ProofCountermodel.lean" > "$tmp/realization.log" 2>&1
```

The replay ran from `2026-07-15T20:03:48+08:00` through
`2026-07-15T20:04:17+08:00`. The output hashes were:

```text
Statement.olean  0cb3c19973217747cb7ee91bb25171d50212bdef10d4246cd1d5ccc952cb1bce
statement.log    afcc4739ad6536f2f83577f6076cdcd38cbb3c15d867ddadac48cc5e417227a9
boundary.log     a3e7a99920e583bc2f934ad400af951ae9989b24410e7d7c68d18ae89a0c9f62
realization.log  ea27796c6b2205a152959ad24901f96ca03213689439e9530ab83b4ddaff6e60
```

`#print axioms` reported `[propext, Classical.choice, Quot.sound]` for both
negative declarations. Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake
`5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

The paired JSON artifact binds the item and obligation IDs, base/tree and
input hashes, exact commands and outputs, trust results, proposed debt
diagnosis, invalidation inputs, and change-impact set. It is current-base
nonrelease blocker evidence, not a positive proof receipt.
