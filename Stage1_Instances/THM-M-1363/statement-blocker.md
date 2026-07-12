# Exact-statement gate: blocked

Item: `S56-M-1363-STATEMENT`

Theorem: `THM-M-1363`

Base revision: `a07fc18923e20fd2876d04809a15d5b31e55512f` (tree
`1268491c8f2677e1c8e38754fa93dd190892e69e`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record gives only the name `混沌理论` (chaos theory), a collective twentieth-century
attribution, and the gloss `确定性系统的混沌行为` (chaotic behavior of deterministic systems). It
supplies no citation, truth-valued proposition, definition, ordered binders, hypotheses, conclusion,
or boundary cases. Stage0 explicitly leaves the formal system, exact definitions and premises,
proof path, dependencies, alternate statements, axioms, machine status, and artifacts open. The
catalog value `已验证` is untrusted metadata under rev-5.6.

Chaos theory is a field, not one theorem. The gloss could mean Devaney chaos, sensitive dependence,
positive topological or measure entropy, Li-Yorke scrambled sets, mixing, a symbolic factor or
horseshoe result, or a theorem that a named system is chaotic. Those choices use inequivalent
definitions, systems, phase and time spaces, structures, regularity assumptions, quantifiers, and
conclusions. A universal reading is false for identity and constant dynamics; an existential
reading still needs a selected system and chaos notion. The ODE catalog category does not authorize
silently restricting the target to a smooth real flow.

The intake's Teschl discovery source confirms that authors use competing definitions and presents a
particular continuous discrete-map Devaney definition plus a chaos-to-sensitivity lemma. The
catalog does not cite or select that source, definition, or lemma, so none is the canonical root or
receives H0 credit. Neighboring targets separately own the Lorenz system, Smale horseshoe,
topological entropy, and measure entropy. Selecting one would substitute a different target.

The intake therefore correctly leaves the canonical human statement, Lean module and expression,
minimal imports, binders, hypotheses, alternate transports, and expression and environment
fingerprints null at `[H5, M4, R4]`. Without a canonical target, the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined rather than passed.
No `Statement.lean`, axiom, placeholder, assumed interface, weakened special case, broadened theorem,
or neighboring result was introduced.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its four direct
imports expose eight adjacent flow, invariance, periodic-point, action-transitivity, and
topological-entropy interfaces, all of which elaborate. The probe defines no chaos predicate and
states no theorem. Its imports therefore cannot be certified minimal for an unknown canonical
target, and the successful check receives no statement, anchor, or proof credit.

A bounded source-name search for chaos, chaotic, Devaney, sensitive dependence, Li-Yorke, scrambled
sets, and `isChaotic` in pinned `Mathlib/Dynamics` found no match. A repo-local search found only
unrelated Wiener-chaos prose. This is narrow discovery evidence, not the downstream immutable anchor
audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The `lean-toolchain`, `lake-manifest.json`, and probe
SHA-256 values are respectively `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`ec8dedf9d7a097a0b694f067e230e71aea8edaa539e08a8533f05e021871ae40`.

The automation-provided `Formalizations/Lean/.lake` link points to canonical pinned artifacts and
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1363` | 0 | rank 973, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD HEAD^{tree}` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| `rg -n -C 12 'THM-M-1363\|混沌理论\|确定性系统的混沌行为' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Blueprint_rev-5.6.md Stage1_Instances/THM-M-1363` | 0 | only the field label and phenomenon gloss are authoritative; every proposition-changing choice remains open |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1363/IntakeProbe.lean` | 0 | eight adjacent pinned APIs elaborated; no canonical target was stated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` and `git -C ... status --short`; `sha256sum` on the four imported mathlib sources | 0 | revision, tree, cleanliness, and source hashes agree with the structured blocker |
| `rg -n -i --glob '*.lean' '\b(chaos\|chaotic\|Devaney)\b\|sensitive[ -]dependence\|Li[- ]Yorke\|scrambled set\|isChaotic' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Dynamics` | 1 | expected no-match exit; discovery only, not an anchor audit |
| the corresponding bounded `rg` over `Formalizations/Lean/AwesomeTheorems` | 0 | only unrelated Wiener-chaos prose matched; no target-specific declaration or statement |
| `python3 -B Stage1_Instances/THM-M-1363/check_intake.py` | 1 | historical intake receipt pins an older authoritative-blueprint hash; this phase does not rewrite intake evidence to manufacture freshness |
| `rg -n -i '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|opaque\|constant)[[:space:]]\|\bunsafe\b' Stage1_Instances/THM-M-1363 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1363/statement-blocker.json` and a recorded Python assertion script over its IDs, null target, mutations, debt, flags, paths, base revision/tree, and absent self-test | 0 | JSON and scoped invariants agree |
| `git diff --check -- Stage1_Instances/THM-M-1363` | 0 | no tracked-diff whitespace diagnostics; the blocker artifacts are untracked and checked separately |
| `git diff --no-index --check /dev/null <added blocker file>` for each added file | 1 each (expected difference) | neither added artifact produced a whitespace diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

The intake prerequisite is only provisional `[_]` and is not master-accepted. That acceptance
boundary independently prevents statement-node acceptance, but the first substantive failure in
this attempt is the missing exact source statement.

## Retry Condition And Status Boundary

The integration lane must accept refreshed intake evidence. Accountable reviewers must preserve and
hash an immutable primary or authoritative source, select and transcribe one exact truth-valued
theorem and all incorporated definitions with pinpoint locators, audit corrections and errata,
reconcile the neighboring targets, and independently approve the source crosswalk. They must freeze
the dynamics and time model, phase and invariant spaces, topology or metric or measure structures,
regularity, exact chaos notion, ordered binders, hypotheses, conclusion, alternate transports, and
every boundary case.

A later statement worker can then encode that same claim using real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile each credited
transport, and run all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json`, node receipt, worker `[_]`, or master acceptance is claimed.
