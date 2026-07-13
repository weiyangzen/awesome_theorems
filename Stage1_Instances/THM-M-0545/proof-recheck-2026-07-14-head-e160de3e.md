# THM-M-0545 proof-phase recheck at base e160de3e

Item: `S56-M-0545-PROOF`

Intent: `prove`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `e160de3efab9257518f9bda57545182c2c72e155`

Base tree: `762bcfd6b010e582efebfcac2285095967248cb2`

## Verdict

`blocked`. No consistent positive proof body exists for the exact frozen Lean
target. The existing placeholder-free declaration

```text
Stage1Instances.THMM0545.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0545.HodgeDecompositionTarget.{0, 0, 0, 0}
```

kernel-checks at trust level zero against a fresh temporary `Statement.olean`.
A universe-polymorphic proof of the positive target would specialize to
universes `(0, 0, 0, 0)` and contradict this declaration.

The countermodel specializes the manifold to the zero-dimensional Euclidean
space, uses `Complex` as the form space in every degree, sets the exterior
derivative and codifferential to zero and the Laplacian to the identity, and
makes every explicit proposition field true. At degree one, harmonicity forces
the harmonic summand to zero and the zero images force the exact and coexact
summands to zero. The form `1` therefore cannot equal their sum. Lean reports
exactly `propext`, `Classical.choice`, and `Quot.sound` for the refutation.

This refutes the frozen abstract encoding, not the mathematical Hodge
decomposition theorem. `realizesSmoothComplexForms` and
`realizesHodgeOperators` are unconstrained propositions; they do not tie the
supplied form spaces and operators to the manifold. Adding the missing laws in
this proof phase would change the frozen target.

No positive proof body, proof receipt, or frozen-obligation closure was added.
The item remains `[ ]`; the predecessor vector remains `[H3, M4, R4]`, with
`M5` only the proposed diagnosis for this refutable encoding. Audit completion,
validation, release, theorem completion, and master acceptance remain open.
Because the assigned phase is not complete, `.stage1-worker-selftest.json` is
deliberately absent.

## Failed Gate And Retry

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY` at
`M0545-S-REALIZATION`. The immediate remaining root cut set is
`S56-M-0545-STATEMENT`, `M0545-S-REALIZATION`, and `M0545-ROOT`.

Positive proof work can resume only after reopening the statement phase,
replacing the opaque realization propositions with concrete pinned definitions
or source-justified, noncircular law-bearing structures that rule out the
countermodel without assuming decomposition, accepting a corrected statement
fingerprint, and rerunning the statement, anchor audit, obligation-tree, and
proof phases in dependency order.

## Validation

All checks ran in this worker clone against the existing pinned Lake closure.
The automation-provided untracked `Formalizations/Lean/.lake` symlink was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
network operation, or `.lake` mutation was performed. Temporary Lean outputs
and logs were written under `/tmp` and removed by shell traps.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0545` | 0 | Rank 105; lane `frontier_deep_formalization_debt`; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0545/check_anchor_audit.py` | 0 | Target boundary, five candidate rows, 11 Lean probes, and pinned mathlib revision agree. |
| `python3 Stage1_Instances/THM-M-0545/check_obligation_tree.py` | 0 | 17 obligations and 132 typed edges passed; denominator `52a39eb0...9896e`; the predecessor graph records the root open at `M4`. |
| Isolated `lake env lean --trust=0 -t 0` recipe below | 0 | The exact statement and universe-zero countermodel elaborated; the refutation reports `[propext, Classical.choice, Quot.sound]`. Statement-log SHA-256: `afcc4739...227a9`; proof-log SHA-256: `ea27796c...6e60`. |
| `rg -n --pcre2 '\b(?:sorry|admit|sorryAx|native_decide)\b|^[[:space:]]*(?:axiom|unsafe|external)\b|implemented_by' Stage1_Instances/THM-M-0545 --glob '*.lean'` | 1 | Expected no-match result: no prohibited construct occurs in the owned Lean sources. |
| `cd Formalizations/Lean && lake env lean --version; lake --version; git -C .lake/packages/mathlib rev-parse HEAD HEAD^{tree}; sha256sum lean-toolchain lake-manifest.json` | 0 | Lean `4.29.0`, commit `98dc76e3...6740`; Lake `5.0.0-src+98dc76e`; mathlib revision `8a178386...ea95`, tree `bdc39a31...c2b`; dependency hashes match the structured record. |
| `test -z "$(git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain)"` | 0 | The reused pinned mathlib worktree is clean. |
| `git diff --check -- Stage1_Instances/THM-M-0545` | 0 | No tracked-diff whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The success manifest is absent, as required for this blocker. |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0545-proof-e160de3e.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0545/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0545/ProofCountermodel-2026-07-14.lean \
  "$tmp/ProofCountermodel.lean"
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd "$tmp"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$lean_path" lake env lean --trust=0 -t 0 --root="$tmp" \
  -o Statement.olean Statement.lean > statement.log 2>&1
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$lean_path" lake env lean --trust=0 -t 0 --root="$tmp" \
  ProofCountermodel.lean > proof.log 2>&1
sha256sum statement.log proof.log
```

The exact hashes, environment, negative declaration, failed gate, and retry
condition are bound in `proof-recheck-2026-07-14-head-e160de3e.json`. This is
durable blocker evidence, not a positive proof receipt.
