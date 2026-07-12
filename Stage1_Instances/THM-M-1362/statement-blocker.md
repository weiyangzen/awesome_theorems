# Exact-statement gate: blocked

Item: `S56-M-1362-STATEMENT`

Theorem: `THM-M-1362`

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only the label `叉形分岔` (pitchfork bifurcation), attribution to many
twentieth-century mathematicians, and the gloss `对称性破缺的分岔` (a bifurcation of symmetry
breaking). It supplies no cited truth-valued proposition, model, definitions, ordered binders,
hypotheses, conclusion, proof boundary, or boundary cases. Stage0 explicitly leaves the formal
system, precise definitions and premises, proof route, alternate forms, axioms, machine status, and
artifact links open. The catalog value `已验证` is untrusted metadata under rev-5.6.

"Pitchfork bifurcation" names a family of inequivalent statements. The target could be a scalar
equilibrium calculation, a stability classification for an autonomous ODE, a local theorem for an
odd smooth family, an equivariant branching lemma, or a center-manifold and normal-form result. It
could be supercritical or subcritical and could assert existence, uniqueness, regularity,
stability, conjugacy, or some conjunction. Those choices change the parameter and phase spaces,
symmetry action, regularity, locality, critical spectrum, transversality and nondegeneracy
hypotheses, branch side and parameterization, ordered binders, conclusion, and exceptional cases.

The inspected Teschl discovery source does not resolve this ambiguity. Section 6.5, printed page
200, presents the scalar family `x' = mu*x - x^3` as a prototypical supercritical example and
describes its fixed points and stability; Problem 6.17 asks the reader to prove the claims. The
catalog does not cite Teschl or select this example. An equilibrium root-count result also does not
by itself prove the source's dynamical stability claims. Choosing the example, its subcritical sign
variant, or a general symmetry-breaking theorem would therefore invent or substitute mathematics.

The intake correctly leaves the canonical human statement, Lean module and expression, minimal
imports, and expression and environment fingerprints null at `[H5, M4, R4]`. Without a canonical
target, alternate transports and the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined rather than passed. No
`Statement.lean`, axiom, placeholder, assumed branch interface, weakened example, broadened theorem,
or neighboring result was introduced.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its five direct
imports expose adjacent derivative, smoothness, integral-curve, flow, and fixed-point interfaces.
All five checks elaborate, but the probe defines no symmetry, pitchfork, branch, stability, or
normal-form predicate and states no target theorem. Its imports therefore cannot be certified
minimal for an unknown canonical target, and the successful check receives no statement, anchor,
or proof credit. In particular, `Function.IsFixedPt f x` means `f x = x`, whereas an equilibrium
of a vector field satisfies `f x = 0`; using that generic predicate directly for the cubic vector
field would encode the wrong proposition.

A bounded exact-topic source search found no `pitchfork` or `bifurcat` occurrence in repository-local
Lean or pinned mathlib. This is narrow discovery evidence, not the downstream immutable anchor audit
or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The `lean-toolchain`,
`lake-manifest.json`, and probe SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`2cd2060d4c0f7c14786d013c49a066bb6aee7d2eb5048d82bf154cbeabeed500`.

The automation-provided `Formalizations/Lean/.lake` link points to the canonical pinned artifacts
and was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1362` | 0 | rank 972, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped repository source, Stage0, manifest, DAG, intake, crosswalk, and scope inspection | 0 | only the phenomenon label and gloss are authoritative; all proposition-changing choices remain open |
| `sha256sum` over authority, intake, toolchain, and pinned mathlib inputs | 0 | hashes agree with the structured blocker |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1362/IntakeProbe.lean` | 0 | five adjacent APIs elaborated; no canonical target was stated |
| pinned mathlib revision, tree, and worktree inspection | 0 | revision and tree agree with the fingerprint; package worktree clean |
| bounded repo-local and pinned-mathlib Lean search for `pitchfork` or `bifurcat` | 1 | expected no-match exit; discovery only, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-1362/check_intake.py` | 1 | historical intake receipt pins older blueprint and execution-DAG hashes; this phase does not rewrite intake evidence to manufacture freshness |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-1362` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1362/statement-blocker.json` | 0 | structured blocker parsed as JSON |
| scoped statement-blocker invariant assertions | 0 | IDs, open state, null target and imports, four undefined mutations, unchanged debt, false completion flags, exact paths, and absent self-test agree |
| whitespace checks for both added blocker artifacts | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

The intake prerequisite is provisional `[_]`, not master-accepted. That acceptance boundary
independently prevents eventual statement-node acceptance, but the first substantive failure in
this attempt is the missing exact source statement.

## Retry condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash an immutable primary or authoritative source, select and transcribe one exact
truth-valued theorem and all incorporated definitions with pinpoint locators, audit corrections and
errata, reconcile the neighboring bifurcation targets, and independently approve the source
crosswalk. They must freeze the system model, parameter and phase spaces, symmetry action,
regularity, locality, critical spectrum, transversality and nondegeneracy assumptions, supercritical
or subcritical sign, branch parameterization, stability notion, ordered binders, conclusion, and
every boundary case.

A later statement worker can then encode that same claim using real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, check every credited
transport, and run all four mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json`, node receipt, worker `[_]`, or master acceptance is claimed.
