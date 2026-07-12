# Exact-statement gate: blocked

Item: `S56-M-1353-STATEMENT`

Theorem: `THM-M-1353`

Base revision: `0d26adeae663d55eb536120f7d93ede975fe8f49` (tree
`6b5ab44050900e9a4a181b4fc56b1e965183f2c9`)

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1353-INTAKE` has provisional worker
state `[_]` in the authoritative execution DAG, not master-accepted state `[x]`. The intake receipt
also declares `accepted: false`, has no accepted receipt ID, and leaves the canonical mathematical
statement and Lean target null. This is the earliest workflow blocker.

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only `Floquet定理`, the attribution Gaston Floquet, 1883, and the gloss
`周期系统的基本解矩阵` (fundamental matrix of a periodic system). It gives no equation,
source citation, scalar field, dimension, coefficient regularity, positive-period convention,
solution or fundamental-matrix definition, normalization, multiplication orientation, ordered
binders, hypotheses, conclusion, or boundary cases. Stage0 explicitly leaves precise definitions
and premises, equivalent forms, axioms, formal system, proof route, machine state, and artifact links
open. The catalogue value `已验证` is untrusted metadata under rev-5.6.

The intake identifies Floquet's 1883 paper only bibliographically. No exact theorem passage,
incorporated definitions, proof boundary, translation, errata disposition, immutable source copy,
or independent review has been accepted. Its inspected secondary source separates several
inequivalent results: a fundamental-matrix factorization, reduction to a constant-coefficient
system, and spectral consequences. It also distinguishes generally complex period-`T` factors
from a real formulation that may require period `2T`.

Consequently, the source does not choose among a normalized monodromy identity, a factorization
`X(t) = P(t) exp(tB)` for every fundamental matrix, a constant-coefficient reduction, or a
source-defined conjunction. It does not decide a scalar higher-order equation versus a first-order
matrix system, real versus complex factors, period `T` versus `2T`, or the existence and branch
conditions for a logarithm of monodromy. These choices change the proposition. Selecting a familiar
Floquet formulation would therefore invent or substitute mathematics rather than elaborate the
exact received target.

Without a source-selected proposition there is no meaningful minimal target import, elaborated
expression fingerprint, credited alternate transport, or removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutation suite. No `Statement.lean`, axiom, placeholder,
special case, broadened theorem, or interface assuming the requested conclusion was added.

## Pinned Lean boundary

The existing `IntakeProbe.lean` re-elaborates against the pinned environment. It checks
`Function.Periodic`, `IsIntegralCurve`, `IsIntegralCurveAt`, `NormedSpace.exp`,
`Matrix.isUnit_exp`, and `Matrix.GeneralLinearGroup`. These are adjacent substrate APIs only. The
probe defines neither a matrix ODE nor a fundamental matrix and states no Floquet target. Its four
imports cannot be certified minimal for an unknown canonical target, and its successful elaboration
receives no statement, anchor, or proof credit.

A bounded exact-topic search of pinned Mathlib and the repository-local Lean tree found no Floquet
or periodic-linear-ODE fundamental-matrix declaration. This is local feasibility evidence, not the
downstream immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned Mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the
`lake-manifest.json` SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`; and the probe SHA-256 is
`2d19e1c31281fcc41d3ad6082e1ecf1d5c2eb1d4e618b6db6434685d1a6faf37`.

The automation-provided `Formalizations/Lean/.lake` link to canonical pinned artifacts was used
read-only. No update, build, dependency clone, fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Commands ran from the repository
root unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1353` | 0 | rank 963, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree match the values above |
| `git status --short --untracked-files=all` | 0 | preflight contained only the automation-provided untracked `.lake` link; it was preserved read-only |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean matches the pinned environment fingerprint above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake matches the pinned environment fingerprint above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision and tree match the fingerprint above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; the pinned Mathlib package worktree is clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1353/IntakeProbe.lean)` | 0 | six adjacent periodicity, ODE, exponential, and general-linear-group APIs elaborated; no target theorem was checked |
| bounded `rg` for Floquet and periodic-linear-ODE fundamental-matrix patterns in pinned Mathlib and repo-local Lean | 1 | expected no-match result; no target-specific declaration was located under the recorded terms |
| `python3 -B Stage1_Instances/THM-M-1353/check_intake.py` | 1 | the historical intake checker expects its intake DAG item to remain `[ ]`, while the integrated authority now projects provisional `[_]`; this statement phase does not rewrite intake evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-1353/statement-blocker.json` | 0 | the finalized structured blocker parsed as valid JSON |
| scoped statement-blocker invariant assertions | 0 | IDs, blocked state, null target and imports, unchanged `[H1, M4, R4]`, false completion flags, exact changed paths, and absent worker packet agree |
| prohibited Lean-construct scan over `Stage1_Instances/THM-M-1353` | 1 | expected no-match result; the API-only probe contains no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| per-file `git diff --no-index --check /dev/null` for both new blocker artifacts | 1 per file | expected new-file difference status with no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | the worker packet is absent because the statement completion gate did not pass |

The statement phase does not modify generated state or rewrite the separately owned intake
history.

## Retry condition

The integration lane must first master-accept current intake evidence. Accountable reviewers must
then preserve and hash an immutable primary or approved authoritative source, select and transcribe
one exact theorem and every incorporated definition with pinpoint locators, audit translation,
proof boundary, corrections, and errata, and independently approve the source crosswalk. The source
must fix the equation model, field, dimension, coefficient regularity, period, solution and
fundamental-matrix predicates, normalization and multiplication conventions, monodromy or
factorization/reduction conclusion, real/complex and `T`/`2T` boundary, logarithm premises, binder
order, and all degenerate cases.

A later statement worker can then encode that same claim using real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, check every credited
transport, and execute all four required mutation classes.

This is evidence for the first failed gate, not completion of the statement node or a downstream
node. The root remains `[H1, M4, R4]`, with `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. The assigned phase is not genuinely
self-tested to its completion gate, so no `.stage1-worker-selftest.json` or node receipt is emitted
and no master acceptance is claimed.
