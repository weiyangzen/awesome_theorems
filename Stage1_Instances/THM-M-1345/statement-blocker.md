# Exact-statement gate: blocked

Item: `S56-M-1345-STATEMENT`

Theorem: `THM-M-1345`

Base revision: `122f443c54e4e81d1bf325b07e18ba095823da6d` (tree
`2629bb0cacebd896715a9abad7c52ad60e7bccd0`)

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only `Hartman-Grobman定理`, the attribution Philip Hartman/David Grobman,
1960, and the gloss `双曲平衡点的局部线性化` (local linearization of a hyperbolic equilibrium).
It gives no citation, equation, phase space, vector-field domain or regularity, local-flow and
time-domain convention, hyperbolicity definition, neighborhoods, conjugacy orientation or
parametrization, ordered binders, hypotheses, conclusion, or boundary cases. Stage0 explicitly
leaves the formal system, exact definitions and premises, proof route, equivalent statements,
axioms, machine status, and artifact links open. The catalogue value `已验证` is untrusted metadata
under rev-5.6.

The intake correctly keeps two source candidates unaccepted. Hartman's 1960 Theorem (II), page
615, concerns `x' = T x + F(x)` near zero, with `F = o(|x|)`, `F` of class `C2`, and all
eigenvalues of `T` off the imaginary axis. It obtains a continuous one-to-one neighborhood
coordinate map conjugating the nonlinear solution transformations to `exp(tT)` while preserving
parametrization. Teschl's modern Theorem 9.9 instead presents a differentiable vector field with a
hyperbolic fixed point and a local homeomorphism conjugating the linear and nonlinear flows, under
inherited local-flow conventions and proof-relevant official errata. The catalogue cites neither
source and does not decide between their regularity or presentation conventions.

The title also names a distinct discrete local-diffeomorphism formulation. A full parametrized
flow conjugacy, a time-one-map conjugacy, and orbit equivalence with time reparametrization are not
interchangeable statements. Nor are a finite-dimensional Euclidean theorem, a coordinate-free
finite-dimensional theorem, and a Banach-space theorem. Selecting Hartman's historical version,
Teschl's modern version, the discrete-map version, or a synthesis would therefore add
proposition-changing mathematics.

Without a source-selected proposition, there is no meaningful minimal target import, elaborated
expression fingerprint, alternate-form transport, or removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutation suite. No `Statement.lean`, axiom, placeholder,
weakened special case, broadened interface, or assumed-conjugacy package was added.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated against the pinned environment. It imports ODE,
flow, derivative, fixed-point, and homeomorphism modules and checks `IsIntegralCurveOn`, `Flow`,
`Flow.toHomeomorph`, `Flow.IsSemiconjugacy`, `Function.IsFixedPt`, `HasFDerivAt`, `fderiv`,
`IsLocalHomeomorphOn`, `Homeomorph`, `OpenPartialHomeomorph`, and `Function.Semiconj`. These are
adjacent APIs only. The probe states no target theorem, its imports are not asserted to be minimal
for an unknown canonical target, and its successful elaboration receives no statement, anchor, or
proof credit.

A bounded exact-topic search of the repo-local Lean tree and pinned Mathlib found no
Hartman-Grobman declaration or hyperbolic-equilibrium local topological-conjugacy result. This is a
local feasibility boundary, not the later immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned Mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the
`lake-manifest.json` SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`; and the probe SHA-256 is
`5b413b783867c0bcf0793af7d8e1a3a26f5daaa465f959e3cbe2a7203fa0ffcd`.

The automation-provided `Formalizations/Lean/.lake` link to canonical pinned artifacts was used
read-only. No update, build, dependency clone, fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Commands ran from the repository
root unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1345` | 0 | rank 956, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | preflight contained only the automation-provided untracked `.lake` link; after this work, only that link and the two owned blocker artifacts are untracked |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake match the pinned environment fingerprint above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision and tree match the fingerprint above; the package status is clean |
| `sha256sum Stage1_Instances/THM-M-1345/IntakeProbe.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | all three hashes match the structured blocker |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1345/IntakeProbe.lean)` | 0 | thirteen adjacent ODE, flow, fixed-point, derivative, local-homeomorphism, and conjugacy interfaces elaborated; no target theorem was checked |
| `rg -n -i --glob '*.lean' 'hartman\|grobman\|topological conjug\|local conjug\|hyperbolic (fixed\|equilibrium)\|hyperbolic.*flow\|flow.*lineariz' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 | no exact-topic result found in this bounded repo-local and pinned-Mathlib search |
| `rg -n -C 5 'Hartman-Grobman定理\|双曲平衡点的局部线性化' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Targets_rev-5.6.json` | 0 | found only the underspecified catalogue record, Stage0 open fields, and manifest metadata |
| `python3 -B Stage1_Instances/THM-M-1345/check_intake.py` | 1 | existing intake replay is stale against the current blueprint hash; this is a prerequisite freshness failure, not a reason to rewrite intake authority during the statement phase |
| `python3 -m json.tool Stage1_Instances/THM-M-1345/statement-blocker.json` | 0 | the structured blocker is valid JSON |
| scoped Python statement-blocker invariant assertions | 0 | IDs, blocked verdict, null target and fingerprints, unchanged `[H1, M4, R4]`, false completion flags, exact changed paths, and absent worker packet agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1345` | 1 | expected no-match result; the API-only probe contains no prohibited proof escape or bodyless/unsafe declaration |
| per-file `git diff --no-index --check /dev/null` for the two new blocker artifacts | 1 per file | expected added-file diff status with no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | the worker packet is absent because the statement completion gate did not pass |

The prerequisite intake receipt is only provisional and not master-accepted. Its public replay also
fails because it records blueprint SHA-256 `88539bc...72e03`, while the current blueprint is
`80514f61...e1a`. This independently prevents statement-node acceptance; this phase does not
rewrite or refresh the separately owned intake evidence.

## Retry condition

An accountable reviewer must preserve and hash an immutable primary or authoritative source,
select and transcribe one exact theorem and every incorporated definition with pinpoint locators,
audit proof ancestry, errata, and Hartman/Grobman genealogy, and independently approve the mapping.
The source must fix the continuous-flow or discrete-map boundary, phase space, vector-field domain
and regularity, equilibrium, well-posedness and local-flow model, hyperbolicity encoding,
neighborhoods, time quantifiers, conjugacy orientation and parametrization, and every degenerate
case. The prerequisite intake evidence must also be refreshed and master-accepted against the
current authorities.

A later statement worker can then encode that same claim using real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, check every credited
transport, and execute all four required mutation classes.

This is the first failed gate, not completion of the statement node or a downstream node. The root
remains `[H1, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted and no statement-node or master-acceptance receipt is
claimed.
