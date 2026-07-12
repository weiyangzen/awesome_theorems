# Exact-statement gate: blocked

Item: `S56-M-1361-STATEMENT`

Theorem: `THM-M-1361`

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only `跨临界分岔` (transcritical bifurcation), an attribution to many
twentieth-century mathematicians, and the gloss `平衡点交换稳定性的分岔` (a bifurcation in which
equilibria exchange stability). It supplies no cited truth-valued proposition, definitions,
ordered binders, hypotheses, conclusion, or boundary cases. Stage0 explicitly leaves the formal
system, exact definitions and premises, proof route, equivalent statements, axioms, machine status,
and artifact links open. The catalog value `已验证` is untrusted metadata under rev-5.6.

The wording identifies a phenomenon and theorem family, not one proposition. It does not select a
definition, the scalar example `x' = mu*x - x^2`, a general local bifurcation theorem, or a smooth
normal-form classification. Those alternatives require materially different choices of continuous-
or discrete-time dynamics, state and parameter spaces, equilibrium branches, regularity, stability
predicate, locality, genericity and nondegeneracy conditions, coordinate and parameter conventions,
and conclusion. Selecting any one from memory would invent, narrow, broaden, or substitute
mathematics rather than transcribe the received target.

The inspected Teschl discovery source does not resolve the choice. Section 6.5 presents the scalar
example and says its fixed points collide and exchange stability, but the catalog does not cite or
select that example and Problem 6.17 delegates its proof. The passage also says both noncritical
fixed points are stable, which conflicts with the adjacent derivative criterion: the state
derivatives at `x = 0` and `x = mu` are `mu` and `-mu`. No matching official erratum was found.
Correcting or promoting this passage without accountable source review would exceed this worker's
authority.

The intake therefore correctly leaves the canonical human statement, Lean module and expression,
minimal imports, and expression and environment fingerprints null at `[H5, M4, R4]`. Without a
canonical target, alternate transports and the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined rather than passed. No
`Statement.lean`, axiom, placeholder, weakened special case, broadened interface, or assumed
transcritical predicate was introduced.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its five direct
imports expose six adjacent implicit-function, integral-curve, flow, fixed-point, derivative, and
smoothness interfaces, all of which elaborate. The probe defines no equilibrium stability,
stability exchange, or transcritical bifurcation and states no theorem. Its imports therefore
cannot be certified minimal for an unknown canonical target, and the successful check receives no
statement, anchor, or proof credit.

A bounded source search for `transcritical` or `bifurcat` in repo-local Lean and pinned mathlib
returned no match. This is narrow discovery evidence, not the downstream immutable anchor audit or
a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The `lean-toolchain`,
`lake-manifest.json`, and probe SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`ae025fbb5f82839713b12865647573105e318e7b24fddfcdf5d6293709d7c270`.

The automation-provided `Formalizations/Lean/.lake` link points to canonical pinned artifacts and
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1361` | 0 | rank 971, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped repository source, Stage0, manifest, DAG, intake, crosswalk, and scope inspection | 0 | only the phenomenon label and gloss are authoritative; all proposition-changing choices remain open |
| `sha256sum` over authority, intake, toolchain, probe, and pinned mathlib inputs | 0 | hashes agree with the structured blocker |
| `python3 -B Stage1_Instances/THM-M-1361/check_intake.py` | 1 | historical intake receipt pins an older blueprint hash; this phase does not rewrite intake evidence to manufacture freshness |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | revision and tree agree with the fingerprint; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1361/IntakeProbe.lean` | 0 | six adjacent APIs elaborated; no canonical target was stated |
| bounded repo-local and pinned-mathlib Lean search for `transcritical` or `bifurcat` | 1 | expected no-match exit; discovery only, not an anchor audit |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-1361` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1361/statement-blocker.json` | 0 | structured blocker parsed as JSON |
| scoped statement-blocker invariant assertions | 0 | IDs, open state, null target and imports, four undefined mutations, unchanged debt, false completion flags, exact paths, and absent self-test agree |
| whitespace checks for both added blocker artifacts | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

The intake prerequisite is only provisional `[_]` and is not master-accepted. That acceptance
boundary independently prevents statement-node acceptance, but the first substantive failure in
this attempt is the missing exact source statement.

## Retry condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash an immutable primary or authoritative source, select and transcribe one exact
truth-valued theorem and all incorporated definitions with pinpoint locators, resolve or formally
delimit the Teschl wording issue, audit corrections and errata, reconcile neighboring targets, and
independently approve the source crosswalk. They must freeze the dynamics model, parameter and state
spaces, equilibrium branches, regularity, stability notion, locality, genericity and nondegeneracy
hypotheses, coordinate conventions, ordered binders, conclusion, and every boundary case.

A later statement worker can then encode that same claim using real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json`, node receipt, worker `[_]`, or master acceptance is claimed.
