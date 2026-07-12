# Exact-statement gate: blocked

Item: `S56-M-1358-STATEMENT`

Theorem: `THM-M-1358`

Base revision: `8c50139eafcb1c2e29e7ca69379648590820bf53` (tree
`84cd63b08ff977c1b895e0299927df8b6d6bc8ae`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only `分岔理论` (bifurcation theory), an attribution to many twentieth-century
mathematicians, and the gloss `参数变化导致的定性变化` (qualitative changes caused by varying a
parameter). It supplies no cited truth-valued proposition, definitions, ordered binders,
hypotheses, conclusion, or boundary cases. Stage0 explicitly leaves the exact definitions and
premises, proof route, equivalent statements, axioms, machine status, and artifact links open. The
catalog value `已验证` is untrusted metadata under rev-5.6.

Bifurcation theory is a field rather than one theorem. The gloss may refer to bifurcations of
equilibria, periodic orbits, invariant sets, maps, or flows; a definition, persistence theorem,
necessary degeneracy condition, local normal-form result, global result, or genericity theorem;
and different notions of qualitative equivalence. The inspected Teschl discovery source confirms
this ambiguity: Section 6.5 introduces the field, separates pitchfork, transcritical, and
saddle-node examples, records an implicit-function necessary condition, and expressly does not
develop an omnibus theory.

The neighboring repository targets separately own saddle-node (`THM-M-1359`), Hopf
(`THM-M-1360`), transcritical (`THM-M-1361`), and pitchfork (`THM-M-1362`) bifurcations. Selecting
one of them, a structural-stability result, or a convenient implicit-function theorem would
substitute a different target. A universal reading of the gloss fails for constant families; an
existential reading requires a selected system; and a definitional reading only names a
bifurcation. None is an exact transcription of the received record.

The intake therefore correctly leaves the canonical human statement, Lean module and expression,
minimal imports, and expression and environment fingerprints null at `[H5, M4, R4]`. Without a
canonical target, alternate transports and the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined rather than passed. No
`Statement.lean`, axiom, placeholder, assumed interface, weakened special case, broadened theorem,
or neighboring result was introduced.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its five direct
imports expose six adjacent implicit-function, integral-curve, flow, fixed-point, derivative, and
smoothness interfaces, all of which elaborate. The probe defines neither qualitative equivalence
nor bifurcation and states no theorem. Its imports therefore cannot be certified minimal for an
unknown canonical target, and the successful check receives no statement, anchor, or proof credit.

A bounded source search for bifurcation and qualitative-change terms in repo-local Lean and pinned
mathlib found no match. This is narrow discovery evidence, not the downstream immutable anchor
audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The `lean-toolchain`,
`lake-manifest.json`, and probe SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`708e78bb51c52723c5880330a03285e053b5053ce550ec82b0bb71c7de261d88`.

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
| `python3 scripts/stage1_target.py show THM-M-1358` | 0 | rank 968, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped repository source, Stage0, manifest, DAG, intake, crosswalk, and scope inspection | 0 | only the field label and gloss are authoritative; all proposition-changing choices remain open |
| `sha256sum` over authority, intake, toolchain, and pinned mathlib inputs | 0 | hashes agree with the structured blocker |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1358/IntakeProbe.lean` | 0 | six adjacent APIs elaborated; no canonical target was stated |
| pinned mathlib revision, tree, and worktree inspection | 0 | revision and tree agree with the fingerprint; package worktree clean |
| bounded repo-local and pinned-mathlib Lean search for bifurcation and qualitative-change terms | 1 | expected no-match exit; discovery only, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-1358/check_intake.py` | 1 | historical intake receipt pins an older blueprint hash; this phase does not rewrite intake evidence to manufacture freshness |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-1358` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1358/statement-blocker.json` | 0 | structured blocker parsed as JSON |
| scoped statement-blocker invariant assertions | 0 | IDs, open state, null target and imports, four undefined mutations, unchanged debt, false completion flags, exact paths, and absent self-test agree |
| whitespace checks for both added blocker artifacts | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

The intake prerequisite is only provisional `[_]` and is not master-accepted. That acceptance
boundary independently prevents eventual statement-node acceptance, but the first substantive
failure in this attempt is the missing exact source statement.

## Retry condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash an immutable primary or authoritative source, select and transcribe one exact
truth-valued theorem and all incorporated definitions with pinpoint locators, audit corrections and
errata, reconcile the neighboring targets, and independently approve the source crosswalk. They
must freeze the parameter and phase spaces, dynamics class, regularity, invariant object,
qualitative-equivalence notion, local or global scope, genericity and nondegeneracy hypotheses,
ordered binders, conclusion, and every boundary case.

A later statement worker can then encode that same claim using real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, check every credited
transport, and run all four mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json`, node receipt, worker `[_]`, or master acceptance is claimed.
