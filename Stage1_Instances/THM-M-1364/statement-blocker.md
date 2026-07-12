# Exact-statement gate: blocked

Item: `S56-M-1364-STATEMENT`

Theorem: `THM-M-1364`

Base revision: `f608e06dccf2e158f1d2feeadb48f1b64d296cdd` (tree
`c0e4ab057a962cd2020342a692d39952f65d8bec`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only the title `Lorenz系统` (Lorenz system), Edward Lorenz, 1963, and the gloss
`混沌的经典例子` (a classic example of chaos). It supplies no cited truth-valued proposition,
equations, parameters, state or time domain, solution semantics, invariant set, definition of
chaos or attractor, ordered binders, hypotheses, conclusion, proof boundary, or boundary cases.
Stage0 explicitly leaves the formal system, exact definitions and premises, proof process,
dependencies, alternate statements, axioms, machine status, and artifact links open. The catalog
value `已验证` is untrusted metadata under rev-5.6.

The likely historical source, Edward N. Lorenz's 1963 paper *Deterministic Nonperiodic Flow*, has
only been identified bibliographically. The catalog gives no page, equation, proposition, or
numerical-experiment locator, and no complete source transcription, correction and errata review,
or independent source approval has selected a root claim. Even the familiar polynomial equations
and conventional parameters do not select one theorem. Materially different possible targets
include an elementary property of the vector field, dissipativity or an absorbing set, a specified
sensitivity or topological-chaos predicate, a geometric Lorenz-attractor theorem, or a rigorous
computer-assisted strange-attractor result for the original equations. These claims are not
interchangeable.

Choosing one of those targets would add, weaken, broaden, or substitute proposition-changing
mathematics. The model and coordinate convention, parameter values or ranges, solution and flow
carrier, invariant-set and attractor semantics, topology or metric or measure structures,
quantifier scope, exact conclusion, analytic versus certified-computation boundary, and all
degenerate cases remain unresolved. Writing down the Lorenz equations is not itself a theorem that
an unspecified meaning of chaos holds. Likewise, an equilibrium calculation, negative divergence,
phase portrait, sampled trajectory, floating-point Lyapunov exponent, abstract geometric model, or
premise that assumes the desired attractor cannot close this root.

The intake therefore correctly leaves the canonical human statement, Lean module and expression,
minimal imports, and canonical expression and environment fingerprints null at `[H5, M4, R4]`.
Without a canonical target, checked alternate transports and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined rather than passed.
No `Statement.lean`, axiom, placeholder, weakened special case, broadened interface, statement
receipt, or proof claim was introduced.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates against the pinned environment. Its three direct
imports expose ten adjacent generic ODE, flow, fixed-point, invariant-set, derivative, omega-limit,
and compactness interfaces. They do not define the Lorenz equations, select parameters, define a
chaos or attractor predicate, or state a Lorenz-system conclusion. The imports are discovery-only
and cannot be certified minimal for an absent target; the successful check receives no statement,
anchor, or proof credit.

A bounded exact-topic search of pinned mathlib's `Mathlib` tree and the shared
`Formalizations/Lean/AwesomeTheorems` source tree found no Lorenz-system, Lorenz-equations,
Lorenz-attractor, geometric-Lorenz, or deterministic-nonperiodic declaration. This is narrow
feasibility evidence, not the downstream immutable anchor audit or a claim of absence outside the
two searched trees.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1364` | 0 | rank 974, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped catalog, Stage0, manifest, DAG, intake, crosswalk, and scope inspection | 0 | only a system-family title and informal chaos gloss are authoritative; no source-selected proposition exists |
| `sha256sum` over authority, intake, source, probe, toolchain, and pinned mathlib inputs | 0 | current hashes are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake match the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree match; the package worktree is clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1364/IntakeProbe.lean` | 0 | ten adjacent generic APIs elaborated; complete stdout SHA-256 `fcd83261...f61c`; no target theorem was declared |
| bounded exact-topic search in pinned mathlib's `Mathlib` tree and `Formalizations/Lean/AwesomeTheorems` | 1 | expected no-match result; discovery only, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-1364/check_intake.py` | 1 | the historical intake validator stops at its stale blueprint hash; it also freezes its earlier base and intake-only inventory, so this phase does not rewrite it |
| prohibited Lean construct scan over the owned path | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| JSON parse and scoped blocker-invariant check | 0 each | IDs, null target and imports, unchanged vector, four undefined mutations, false completion flags, exact changed paths, and absent self-test agree |
| scoped and per-new-file whitespace checks | 0; 1 per new file | no whitespace diagnostics; no-index exits are only the expected new-file differences |
| `test ! -e .stage1-worker-selftest.json` | 0 | the self-test manifest is absent because the exact-statement completion gate did not pass |

The intake prerequisite has provisional worker state `[_]`, not master-accepted state `[x]`. Its
receipt declares `accepted: false` and supplies no accepted receipt ID. That dependency-acceptance
gap independently prevents statement-node acceptance; the first substantive statement failure is
the missing exact source-statement identity.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then preserve and hash one lawful immutable primary or authoritative source, select and transcribe
one exact truth-valued root and every incorporated definition with pinpoint locators, inspect
corrections and errata, and independently approve why the result represents this target rather than
neighboring chaos, horseshoe, entropy, Lyapunov-exponent, or random-attractor targets. The selection
must fix the equations or model, parameters, spaces, solution and invariant-set semantics, exact
chaos or attractor predicate and quantifiers, conclusion, computation and certificate boundary,
ordered binders, and every degenerate case.

A fresh statement run can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; the root remains `[H5, M4, R4]`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, node receipt, worker
`[_]`, or master acceptance is claimed.
