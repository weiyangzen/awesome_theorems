# Exact-statement gate: blocked

Item: `S56-M-1366-STATEMENT`

Theorem: `THM-M-1366`

Base revision: `a07fc18923e20fd2876d04809a15d5b31e55512f` (tree
`1268491c8f2677e1c8e38754fa93dd190892e69e`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only `结构稳定性` (structural stability), the Andronov/Pontryagin attribution,
the year 1937, and the gloss `系统在扰动下的稳定性` ("stability of systems under perturbations").
It supplies no cited truth-valued proposition, definitions, ordered binders, hypotheses,
conclusion, proof boundary, or boundary cases. Stage0 explicitly leaves the formal system, exact
definitions and premises, proof route, equivalent statements, axioms, machine status, and artifact
links open. The catalog value `已验证` is untrusted metadata under rev-5.6.

Structural stability is relative to a chosen space of dynamical systems, topology on that space,
and equivalence relation. The record chooses none of them. The object could be a vector field,
flow, map, or diffeomorphism; perturbations could use a `C0`, `C1`, `Cr`, compact-open, Whitney, or
other topology; and stability could mean conjugacy, orbit equivalence with a time change, or a
classification. It is also unclear whether the root is a definition, robustness or openness
theorem, necessary or sufficient condition, characterization, classification, density result, or
existence statement. Those choices materially change the domains, quantifier order, hypotheses,
conclusion, and exceptional cases.

The repository separately owns Peixoto's theorem (`THM-M-1367`), Morse-Smale systems
(`THM-M-1368`), Hartman-Grobman (`THM-M-1345`), stable manifolds (`THM-M-1346`), the Smale
horseshoe (`THM-M-1365`), hyperbolic dynamical systems (`THM-M-1411`), and Anosov diffeomorphisms
(`THM-M-1412`). Selecting one of those familiar results would substitute another root. A separate
physics-corpus record, Stage0 `THM-P-0745`, gives the more specific gloss "rough systems of
two-dimensional systems are structurally stable," but it is absent from the frozen Stage1
manifest and still supplies no exact definitions or proposition. It is ambiguity evidence, not
authority to redirect this target.

The intake therefore correctly leaves the canonical human statement, Lean module and expression,
minimal imports, and expression and environment fingerprints null at `[H5, M4, R4]`. Without a
canonical target, alternate transports and the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined rather than passed. No
`Statement.lean`, axiom, placeholder, assumed stability structure, weakened example, broadened
theorem, or neighboring result was introduced.

## Source boundary

The two duplicate six-line catalog records originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`, blob
`5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf`. Duplication is not independent evidence. Crossref DOI
`10.1201/9780367813758-12` points to a 2019 selected-works chapter titled *Rough Systems*, pages
159-164, whose record names R. V. Gamkrelidze. That is a secondary discovery lead, not an accepted
1937 primary theorem. No source currently has an accepted edition, pinpoint proposition, complete
definition and assumption map, proof boundary, correction or errata disposition, and independent
review.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its single direct
import exposes eight adjacent flow, orbit, invariant-set, homeomorphism, semiconjugacy, and factor
interfaces, all of which elaborate. The probe defines neither a perturbation space nor structural
stability and states no theorem. Its import therefore cannot be certified minimal for an unknown
canonical target, and the successful check receives no statement, anchor, or proof credit.

A bounded exact-topic search found no structural-stability, rough-system, Andronov, Peixoto, or
Morse-Smale occurrence in repository-local Lean or pinned mathlib. This is narrow discovery
evidence, not the downstream immutable anchor audit or a global absence claim. A broader initial
`Pontryagin` search returned only unrelated Pontryagin-duality and characteristic-class text.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The `lean-toolchain`,
`lake-manifest.json`, and probe SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`e30b13a2ae0f1af7e3af4b25a417aed0b717cf70c2f23599753c1cdfa98394fe`.

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
| `python3 scripts/stage1_target.py show THM-M-1366` | 0 | rank 976, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped manifest, blueprint, DAG, skill, guideline, source, Stage0, intake, crosswalk, and scope inspection | 0 | the Stage1 catalog gives only a topic and gloss; the cross-corpus variant is outside the manifest and also inexact; all proposition-changing choices remain open |
| `sha256sum` over authority, source, intake, toolchain, and pinned mathlib inputs | 0 | hashes agree with the structured blocker |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1366/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; no canonical target or proof body was declared; stdout SHA-256 `f70405ae8da7777a4097551cdf70b10dea74c6aa6e13c9183967cce5603e68f1` |
| pinned mathlib revision, tree, and worktree inspection | 0 | revision and tree agree with the fingerprint; package worktree clean |
| bounded repo-local and pinned-mathlib Lean search for exact-topic terms | 1 | expected no-match exit; discovery only, not an anchor audit |
| `jq -e 'any(.targets[]; .theorem_id == "THM-P-0745")' Docs/Stage1_Targets_rev-5.6.json` | 1 | expected false result; the cross-corpus record is outside the frozen Stage1 target set |
| `python3 -B Stage1_Instances/THM-M-1366/check_intake.py` | 1 | historical intake checker freezes state `[ ]` and attempts 0, while current authority records provisional `[_]` and attempts 1; this phase does not rewrite intake evidence |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-1366` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1366/statement-blocker.json` | 0 | structured blocker parsed as JSON |
| scoped statement-blocker invariant assertions | 0 | IDs, open state, null target and imports, four undefined mutations, unchanged debt, false completion flags, current hashes, exact paths, and absent self-test agree |
| whitespace checks for both added blocker artifacts | 0 | no whitespace diagnostics; no-index exit 1 is expected for a clean new-file diff |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

The intake prerequisite is only provisional `[_]` and is not master-accepted. That acceptance
boundary independently prevents eventual statement-node acceptance, but the first substantive
failure in this attempt is the missing exact source statement and root selection.

## Retry condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash an immutable primary or authoritative source, select and transcribe one exact
truth-valued proposition and every incorporated definition with pinpoint locators, audit
corrections and errata, reconcile the cross-corpus and neighboring target boundaries, and
independently approve the source crosswalk. They must freeze the system object, phase space, time
convention, regularity, perturbation topology, equivalence relation, local or global scope,
quantifier order, every hypothesis and conclusion, and every boundary case.

A later statement worker can then encode that same claim using real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, check every credited
transport, and run all four mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json`, node receipt, worker `[_]`, or master acceptance is claimed.
