# Exact-statement gate: blocked

Item: `S56-M-1365-STATEMENT`

Theorem: `THM-M-1365`

Base revision: `f608e06dccf2e158f1d2feeadb48f1b64d296cdd` (tree
`c0e4ab057a962cd2020342a692d39952f65d8bec`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only `Smale马蹄` (Smale horseshoe), Stephen Smale, 1967, and the gloss
`混沌的几何模型` ("a geometric model of chaos"). It supplies no cited truth-valued proposition,
definition, ordered binder, hypothesis, conclusion, proof boundary, or boundary case. Stage0
explicitly leaves the formal system, exact definitions and premises, proof route, equivalent
statements, axioms, machine status, and artifacts open. The catalog value `已验证` is untrusted
metadata under rev-5.6.

The wording identifies a construction and theorem family, not one proposition. Smale's 1967
Section 1.5 is a plausible discovery source, but it separates the full-shift periodic-point result,
the two-strip invariant-set conjugacy, perturbation persistence, a global sphere construction, and
the transverse-homoclinic-point theorem. These claims have materially different maps, domains,
regularity and crossing assumptions, invariant sets, iterate conventions, coding strengths, and
conclusions. The catalog neither cites that source nor selects one result or conjunction.

Choosing Proposition (5.3), Proposition (5.4), the global construction, Theorem (5.5), an affine
example, or a generic symbolic-dynamics theorem would invent, narrow, broaden, or substitute
mathematics rather than elaborate the exact received target. The source scan also has a possible
invariant-set-symbol print or OCR ambiguity, and the cited precursor, correction history,
immutable source admission, and independent source review remain open.

The intake therefore correctly leaves the canonical human statement, Lean module and expression,
minimal imports, and canonical expression and environment fingerprints null at `[H5, M4, R4]`.
Without a canonical target, checked alternate transports and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined rather than
passed. No `Statement.lean`, axiom, placeholder, assumed conjugacy, weakened special case, or
broadened theorem was introduced.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its four direct
imports expose eight adjacent stream, semiconjugacy, iteration, periodic-point, and homeomorphism
interfaces, all of which elaborate. The probe defines no horseshoe map, square or strip geometry,
maximal invariant set, coding homeomorphism, hyperbolicity, or source-selected conclusion. Its
imports therefore cannot be certified minimal for an absent canonical target, and the successful
check receives no statement, anchor, or proof credit.

A bounded exact-topic search in repo-local Lean and pinned mathlib found no horseshoe declaration
under the recorded terms. This is narrow discovery evidence, not the downstream immutable anchor
audit or a claim of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The `lean-toolchain`,
`lake-manifest.json`, and probe SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`47b1096f7f47c4dd31508b12c9545fc923d505a17d41757c7c43c30423bdaec2`.

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
| `python3 scripts/stage1_target.py show THM-M-1365` | 0 | rank 975, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped source, Stage0, manifest, DAG, intake, crosswalk, and scope inspection | 0 | only the construction-family label and gloss are authoritative; all proposition-changing choices remain open |
| `sha256sum` over authority, intake, toolchain, and pinned mathlib inputs | 0 | hashes agree with `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| pinned mathlib revision, tree, and worktree inspection | 0 | revision and tree agree with the fingerprint; the package worktree was clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1365/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; no canonical target or proof body was declared; stdout SHA-256 `fee81f942f0db786a0fa927f041ed2ea6b9b62f1404f43f5ff9374b75e665176` |
| bounded repo-local and pinned-mathlib Lean search for horseshoe terms | 1 | expected no-match exit; discovery only, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-1365/check_intake.py` | 1 | the historical intake receipt pins an older blueprint hash; this phase records rather than rewrites historical evidence |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-1365` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1365/statement-blocker.json` | 0 | the finalized structured blocker parsed as JSON |
| scoped statement-blocker invariant assertions | 0 | IDs, open state, null target and imports, four undefined mutations, unchanged debt, false completion flags, exact paths, and absent self-test agree |
| whitespace checks for both added blocker artifacts | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

The intake prerequisite has provisional worker state `[_]`, not master-accepted state `[x]`. Its
receipt explicitly has `accepted: false` and no accepted receipt ID. This attempt can preserve the
substantive statement blocker, but dependency acceptance independently remains necessary before a
future statement transition can be accepted. The first substantive failure here is the missing
exact source-statement identity and result selection.

## Retry condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash one lawful complete primary or authoritative source edition, select and
transcribe one exact result and every incorporated definition with pinpoint locators, audit the
precursor, corrections, errata, and the possible symbol ambiguity, and independently approve the
source crosswalk. They must freeze the ambient space and map class, strip geometry and estimates,
maximal invariant set, alphabet and shift direction, coding strength, iterate and locality,
ordered binders, exact conclusion, and every boundary case.

A later statement worker can then encode that same claim using real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, check every credited
transport, and run all four mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion
gate, no `.stage1-worker-selftest.json`, node receipt, worker `[_]`, or master acceptance is
claimed.
