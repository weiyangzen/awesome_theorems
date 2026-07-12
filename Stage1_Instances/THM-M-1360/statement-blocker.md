# Exact-statement gate: blocked

Item: `S56-M-1360-STATEMENT`

Theorem: `THM-M-1360`

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The record supplies only `Hopf` bifurcation, Eberhard Hopf, 1942, and the gloss `周期解产生的分岔`
("bifurcation in which periodic solutions arise"). It supplies no cited proposition, differential
system, ordered binders, hypotheses, conclusion, incorporated definitions, proof boundary, or
boundary cases. Stage0 explicitly leaves the exact definitions and premises, proof route,
equivalent statements, axioms, machine status, and artifacts open. The catalog value `已验证` is
untrusted metadata under rev-5.6.

The inspected sources expose materially inequivalent Hopf theorems rather than resolving that
ambiguity. Hopf's historical paper is a plausible lead for an analytic finite-dimensional
existence and isolation theorem, but the repository does not cite it, select an exact clause, or
provide a complete transcription, translation, assumption map, correction audit, immutable source
packet, and independent review. A modern smooth theorem may additionally require a nonzero first
Lyapunov coefficient and conclude a supercritical or subcritical stability classification. A
Banach-space theorem instead uses closed-operator, nonresonance, resolvent, and periodic-function-
space hypotheses and can conclude local branch exhaustiveness modulo phase. The catalog selects
none of these contracts.

Choosing the familiar planar normal form, an n-dimensional center-manifold theorem, Hopf's analytic
result, a Banach/PDE/delay theorem, a degenerate result, or a conjunction would invent, strengthen,
broaden, or substitute mathematics rather than elaborate the exact received target. The state
space, vector-field regularity, equilibrium branch, critical spectrum and multiplicity, crossing
orientation, harmonic and nonlinear nondegeneracy, parameter side, periodicity and phase
conventions, uniqueness, normal form, stability, and all degenerate cases remain unresolved.

The intake therefore correctly leaves the canonical human statement, Lean module and expression,
minimal imports, and canonical expression and environment fingerprints null at `[H1, M4, R4]`.
Without a canonical target, checked alternate transports and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined rather than passed.
No `Statement.lean`, axiom, placeholder, assumed periodic branch, weakened example, or broadened
theorem was introduced.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its five direct
imports expose nine adjacent periodicity, integral-curve, flow, smoothness, derivative, eigenvalue,
and spectrum interfaces, all of which elaborate. The probe defines no equilibrium continuation,
critical-pair crossing, Lyapunov coefficient, periodic branch, phase quotient, normal form, or Hopf
conclusion. Its imports therefore cannot be certified minimal for an absent canonical target, and
the successful check receives no statement, anchor, or proof credit.

A bounded case-insensitive exact-topic search in repo-local Lean and pinned mathlib found no
Andronov-Hopf or Hopf-bifurcation declaration. This is narrow discovery evidence, not the
downstream immutable anchor audit or a claim of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The `lean-toolchain`,
`lake-manifest.json`, and probe SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`a7a9ef7e91c4a19660dfadf91bab89c9b6325fb1ea1d41e42a8a26723e2776ec`.

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
| `python3 scripts/stage1_target.py show THM-M-1360` | 0 | rank 970, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped source, Stage0, manifest, DAG, intake, crosswalk, and scope inspection | 0 | only the theorem-family label and gloss are authoritative; all proposition-changing choices remain open |
| `sha256sum` over authority, intake, toolchain, and pinned mathlib inputs | 0 | hashes agree with `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1360/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; no canonical target or proof body was declared |
| pinned mathlib revision, tree, and worktree inspection | 0 | revision and tree agree with the fingerprint; the package worktree was clean |
| bounded repo-local and pinned-mathlib Lean search for Andronov/Hopf bifurcation terms | 1 | expected no-match exit; discovery only, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-1360/check_intake.py` | 1 | the historical intake checker freezes intake authority state `[ ]`, while current authority records provisional `[_]`; this phase does not rewrite historical evidence |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-1360` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1360/statement-blocker.json` | 0 | the finalized structured blocker parsed as JSON |
| scoped statement-blocker invariant assertions | 0 | IDs, open state, null target and imports, four undefined mutations, unchanged debt, false completion flags, exact paths, and absent self-test agree |
| whitespace checks for both added blocker artifacts | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

The intake prerequisite has provisional worker state `[_]`, not master-accepted state `[x]`. Its
receipt explicitly has `accepted: false` and no accepted receipt ID. Rev-5.6 permits this
dependency-ordered attempt, but dependency acceptance independently remains necessary before any
future statement transition can be master-accepted. The first substantive failure here is the
missing exact source-statement identity and variant selection.

## Retry condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash one lawful complete primary or authoritative source edition, select and transcribe
one exact result and every incorporated definition with pinpoint locators, reconcile the 1942/1943
provenance, audit translations, corrections, and errata, and independently approve the source
crosswalk. They must freeze the system and state space, regularity, equilibrium branch, critical
spectrum, crossing and nonlinear nondegeneracy, periodic-solution and phase conventions, parameter
side, uniqueness, normal-form and stability conclusions, ordered binders, and every boundary case.

A later statement worker can then encode that same claim using real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, check every credited
transport, and run all four mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H1, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json`, node receipt, worker `[_]`, or master acceptance is claimed.
