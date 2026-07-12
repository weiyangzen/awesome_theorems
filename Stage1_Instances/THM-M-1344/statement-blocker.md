# Exact-statement gate: blocked

Item: `S56-M-1344-STATEMENT`

Theorem: `THM-M-1344`

Base revision: `b72c38f3df59ba12e643e0a20be2dd36c063eafc` (tree
`4b2126951b48faf4dd3d85dc1e81962ea29a7004`)

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only `李雅普诺夫间接法` (Lyapunov's indirect method), Aleksandr Lyapunov,
1892, and the gloss `线性化稳定性` (stability by linearization). It gives no equation, phase
space, equilibrium, solution model, regularity, source theorem or page, ordered binders,
hypotheses, conclusion, or boundary cases. Stage0 explicitly leaves the formal system, exact
definitions and premises, proof route, equivalent statements, axioms, machine status, and artifact
links open. The catalog value `已验证` is untrusted metadata under rev-5.6.

The intake correctly preserves several inequivalent candidate claims without selecting one. In a
finite-dimensional autonomous ODE, a negative spectral condition may imply local exponential
stability, while a positive spectral value may imply instability. A target could contain one
direction or both. Other formulations use Banach-space semigroups or conclude only asymptotic or
Lyapunov stability. Each choice changes hypotheses, quantifiers, and conclusion; a critical
linearization with spectrum on the imaginary axis generally gives no conclusion without additional
higher-order hypotheses.

The inspected secondary discovery source, Al Jamal, Chow, and Morris, arXiv:1509.05792v1,
Theorem 3.1, makes this ambiguity explicit by stating separate finite-dimensional stable and
unstable branches and contrasting them with Banach-space variants. The catalog does not cite that
paper or choose either branch. Its immutable PDF hash and source assessment are already recorded by
the intake, but it is discovery evidence rather than an approved primary or authoritative
source-to-target mapping.

Selecting a familiar stable branch, unstable branch, their conjunction, or a semigroup theorem
would therefore substitute mathematics. So would weakening exponential stability, importing scope
from a neighboring theorem, or defining an abstract structure that assumes the desired conclusion.
Without a source-selected proposition, there is no meaningful minimal target import, elaborated
expression fingerprint, alternate-form transport, or removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutation suite. No `Statement.lean`, axiom, placeholder,
weakened special case, or broadened interface was added.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated against the pinned environment. It imports ODE,
Frechet-derivative, and eigenspace modules and checks `IsIntegralCurve`, `IsPicardLindelof`,
`ODE_solution_unique_univ`, `HasFDerivAt`, `fderiv`, `spectrum`, and the finite-dimensional
eigenvalue-spectrum bridge. These are adjacent APIs only. The probe states no target theorem, its
imports are not asserted to be minimal for an unknown canonical target, and its successful
elaboration receives no statement, anchor, or proof credit.

A bounded repo-local and pinned-Mathlib name search found only unrelated Lyapunov central-limit and
exponent material, not a target-specific indirect-method theorem or nonlinear ODE stability
predicate. This is a local feasibility boundary, not the later immutable anchor audit or a global
absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned Mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the
`lake-manifest.json` SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`; and the probe SHA-256 is
`f2ae778468ea688e6c0f566becdfa9926786b4b9bbb919aebbb1de129eaded85`.

The automation-provided `Formalizations/Lean/.lake` link to canonical pinned artifacts was used
read-only. No update, build, dependency clone, fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Commands ran from the repository
root unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1344` | 0 | rank 955, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake match the pinned environment fingerprint above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision and tree match the fingerprint above; the package status is clean |
| `sha256sum Stage1_Instances/THM-M-1344/IntakeProbe.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | all three hashes match the structured blocker |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1344/IntakeProbe.lean)` | 0 | nine adjacent ODE, derivative, and spectral interfaces elaborated; no target theorem was checked |
| `rg -n -i --glob '*.lean' 'lyapunov\|liapunov\|exponential stability\|exponentially stable\|asymptotic.*stabl\|linearization.*stabl\|stability.*lineariz\|unstable.*eigen\|eigenvalue.*real part' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 0 | only unrelated Lyapunov CLT/exponent material occurred; no target-specific declaration was located in this bounded search |
| `rg -n -C 3 '李雅普诺夫间接法\|线性化稳定性' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Targets_rev-5.6.json` | 0 | found only the underspecified catalog record, Stage0 open fields, and manifest metadata |
| `python3 -B Stage1_Instances/THM-M-1344/check_intake.py` | 1 | existing intake replay is stale against the current blueprint hash; this is a prerequisite freshness failure, not a reason to rewrite intake authority during the statement phase |
| `python3 -m json.tool Stage1_Instances/THM-M-1344/statement-blocker.json` | 0 | the structured blocker is valid JSON |
| scoped Python statement-blocker invariant assertions | 0 | IDs, blocked verdict, null target and fingerprints, unchanged `[H1, M4, R4]`, false completion flags, exact changed paths, and absent worker packet agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1344` | 1 | expected no-match result; the API-only probe contains no prohibited proof escape or bodyless/unsafe declaration |
| per-file `git diff --no-index --check /dev/null` for the two new blocker artifacts | 1 per file | expected added-file diff status with no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | the worker packet is absent because the statement completion gate did not pass |

## Retry condition

An accountable reviewer must preserve and hash an immutable primary or authoritative source,
select and transcribe one exact theorem and every incorporated definition with pinpoint locators,
audit proof ancestry and errata or translation, and independently approve the mapping. The source
must fix the system, phase space, equilibrium, regularity, well-posedness, solution model,
linearization, spectral direction or directions, stability strength, quantifier order,
critical-spectrum policy, and all degenerate cases. The prerequisite intake evidence must also be
refreshed and master-accepted against the current authorities.

A later statement worker can then encode that same claim using real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, check every credited
transport, and execute all four required mutation classes.

This is the first failed gate, not completion of the statement node or a downstream node. The root
remains `[H1, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted and no statement-node or master-acceptance receipt is
claimed.
