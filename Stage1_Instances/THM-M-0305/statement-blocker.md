# Exact-statement gate: blocked

Item: `S56-M-0305-STATEMENT`

Theorem: `THM-M-0305`

Base revision: `f23ca64267b6746e12a641dcc66cc4dbaf1e2191` (tree
`d1872d3251ef6a9c395116467608691849d80496`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete mathematical wording is only the title `庞加莱不等式` (Poincare inequality) and the
gloss `Sobolev函数的L^p估计` ("an `L^p` estimate for Sobolev functions"), with Henri Poincare and
1890 as uncited metadata. It supplies no truth-valued formula, primary-source locator, domain,
measure, function space, exponent range, normalization, weak derivative, norms, constant
dependency, ordered binders, or boundary cases. Stage0 explicitly leaves the precise definitions
and premises open, and rev-5.6 treats the catalog's `已验证` value as untrusted.

Those missing choices distinguish inequivalent propositions. A mean-subtracted inequality on a
bounded connected domain is not the same statement as a zero-trace or compact-support inequality;
neither is a one-dimensional Wirtinger specialization or a Gagliardo-Nirenberg-Sobolev estimate
with dimension-related exponents. The catalog separately assigns the same attribution, year, and
gloss to PDE target `THM-M-1239`, but no reviewer has decided whether the two records are aliases,
distinct formulations, or which target owns a terminal proof body. Selecting a familiar variant,
copying the sibling target, or conjoining variants would invent, broaden, or substitute mathematics.

The intake therefore correctly leaves the canonical human statement, Lean module and expression,
minimal imports, and canonical expression and environment fingerprints null at `[H1, M3, R4]`.
Without one canonical target, checked transports and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined rather than
passed. No `Statement.lean`, axiom, placeholder, assumed inequality, weakened special case, or
broadened theorem was introduced.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated using the pinned environment and its single
direct import, `Mathlib.Analysis.FunctionalSpaces.SobolevInequality`. It checks `eLpNorm`, `fderiv`,
and four derivative-norm inequalities for compactly supported or bounded-support continuously
differentiable functions on finite-dimensional real normed spaces. All six interfaces elaborate,
but mathlib presents the results as Gagliardo-Nirenberg-Sobolev inequalities. They do not select a
domain Sobolev model, mean-zero versus trace/support normalization, or source-faithful Poincare
root. The import therefore cannot be certified minimal for an absent canonical target, and the
successful check receives no statement, transport, anchor, or proof credit.

A bounded exact-topic search in repository-local Lean and pinned mathlib found Poincare-inequality
names only in the distinct probability target `THM-M-0998`; adjacent analysis files expose the
Gagliardo-Nirenberg-Sobolev interfaces above. This is narrow feasibility evidence, not the later
immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The `lean-toolchain`,
`lake-manifest.json`, intake probe, and Sobolev module SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`,
`94f92e3c6e6874be653253240f9e1181ec82e6ad9c4f64686b54d92fc78929e6`, and
`bbd0840b2f0c1145c325577c18bb136053d2712dc1c24ad66c8aba0370a4623b`.

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
| `python3 scripts/stage1_target.py show THM-M-0305` | 0 | rank 1013, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped catalog, Stage0, manifest, DAG, intake, crosswalk, scope, and duplicate inspection | 0 | only the family label and gloss are authoritative; all proposition-changing choices and the `THM-M-1239` identity boundary remain open |
| `sha256sum` over authority, intake, toolchain, lockfile, probe, and pinned mathlib inputs | 0 | hashes agree with `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0305/IntakeProbe.lean` | 0 | six adjacent APIs elaborated; no canonical target, transport, or proof body was declared |
| pinned mathlib revision, tree, and worktree inspection | 0 | revision and tree agree with the fingerprint; the package worktree was clean |
| bounded repo-local and pinned-mathlib Lean search for Poincare-inequality names | 0 | exact-name matches belonged to the distinct probability target; no source-frozen real-analysis root was found under the bounded terms |
| `python3 -B Stage1_Instances/THM-M-0305/check_intake.py` | 1 | the historical intake checker freezes intake authority state `[ ]`, while the current authoritative DAG records provisional `[_]`; this phase does not rewrite historical evidence |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-0305` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0305/statement-blocker.json` | 0 | the finalized structured blocker parsed as JSON |
| scoped statement-blocker invariant assertions | 0 | IDs, open state, null target and imports, four undefined mutations, unchanged debt, false completion flags, exact paths, and absent self-test agree |
| whitespace checks for both added blocker artifacts | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable did not pass |

The intake prerequisite has provisional worker state `[_]`, not master-accepted state `[x]`. Its
receipt explicitly has `accepted: false` and no accepted receipt ID. Rev-5.6 permits this
dependency-ordered attempt, but dependency acceptance independently remains necessary before any
future statement transition can be master-accepted. The first substantive failure here is the
missing exact source-statement variant and duplicate-identity decision.

## Retry condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash one lawful complete primary or authoritative source edition, select and
transcribe one exact result and every incorporated definition with pinpoint locators, audit its
translation, corrections, and errata, and independently approve the mapping. They must resolve the
identity and proof-ownership relationship with `THM-M-1239`, then freeze the scalar field, ambient
dimension, domain and regularity, measure, Sobolev model, exponents, normalization or trace/support
condition, derivative, norms, constant dependencies, ordered binders, and every boundary case.

A later statement worker can then encode that same claim using real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, check every credited
transport, and run all four mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H1, M3, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json`, node receipt, worker `[_]`, or master acceptance is claimed.
