# Exact-statement gate: blocked

Item: `S56-M-0256-STATEMENT`

Theorem: `THM-M-0256`

Base revision: `d4646fb26544dad2bd601137067a00d47064a074`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record gives the title `泰希米勒理论` ("Teichmuller theory"), attributes it to Oswald
Teichmuller in 1939, and supplies only the gloss `黎曼面的模空间` ("moduli space of Riemann
surfaces"). The wording names a theory and an object, not a truth-valued proposition. It specifies
no surface category, marking or equivalence relation, ordered binders, hypotheses, conclusion, or
degenerate cases. Stage0 expressly leaves the exact definitions and premises, formal system,
foundation, proof route, equivalent forms, axioms, and machine artifact open. The source status
`已验证` is untrusted metadata under rev-5.6.

The integrated intake therefore freezes `canonical_statement`, `canonical_claim`, Lean module,
declaration or expression, elaborated-expression hash, and target environment fingerprint as null.
It classifies the received catalog target as `[H5, M4, R4]`, with the statement gate blocked because
the target is not a stable proposition. This statement-phase inspection found no approved target
correction or exact primary-source proposition that changes that boundary.

The execution DAG records the intake dependency as provisional worker state `[_]`; its receipt is
not master-accepted and lists no accepted receipt ID. That is a separate acceptance boundary. It
does not authorize inventing the missing claim, and it does not change the first substantive
failure in this attempt: exact source-statement identity and variant selection.

Several inequivalent theorem families fit the gloss: construction of marked-surface Teichmuller
space, existence and uniqueness of extremal quasiconformal maps, identification of a moduli space
as a mapping-class-group quotient, or a dimension, manifold, topology, contractibility, metric, or
geodesic theorem. Selecting one would invent a conclusion or substitute missing mathematics.
It could also absorb neighboring targets `THM-M-0255` (quasiconformal mapping theory),
`THM-M-0257` (complex structure), or `THM-M-0258` (boundary). A generic quotient or manifold
interface would be only an abstract shadow, not a source-faithful Teichmuller theorem.

Consequently there is no canonical expression from which to establish minimal imports, a
normalized kernel-expression fingerprint, checked alternate transports, or meaningful
removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations. The rev-5.6
statement gate fails at exact source-statement identity and variant selection, before proof or
anchor evidence may be inspected. No theorem declaration, axiom, placeholder, broadened interface,
or substituted special case was added.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports `Mathlib.Geometry.Manifold.Complex` and
`Mathlib.GroupTheory.GroupAction.Defs`. Under the pinned environment it re-elaborates these six
generic interfaces:

- `ChartedSpace`;
- `IsManifold`;
- `MDifferentiable`;
- `MulAction.orbitRel`;
- `MulAction.orbitRel.Quotient`; and
- `Quotient.mk`.

These checks show only that generic complex-manifold, group-action, orbit-relation, and quotient
substrates are available. They neither define Riemann-surface moduli nor state a target theorem.
The two imports are not claimed to be minimal for an unknown canonical target, and successful
elaboration receives no statement, anchor, or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`, the
`lake-manifest.json` SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and the probe SHA-256 is
`200c56c97f87a0627ee1bb8eda17e663a9725349199d1d443a85b8b766b1ff7b`.

The automation-provided untracked `Formalizations/Lean/.lake` symlink points to the canonical
checkout's pinned artifacts. It was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0256` | 0 | rank 942, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` plus `git rev-parse HEAD` and `git rev-parse HEAD^{tree}` | 0 | base revision above, tree `1308114241d7b7c725a558dbe58775d1e3dd5083`; before this phase only the automation-provided `.lake` symlink was untracked |
| `git blame -L 1843,1848 -- Docs/researches/math_theorems.md` and exact-block hashing | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; block SHA-256 `9a4df3af762ddb0ac5e0b89340e286bf0248d6b16a12b0245a6172f00faa5e07` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0256/IntakeProbe.lean)` | 0 | all six generic interfaces elaborated; no target theorem was stated |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 1 | expected no-match result for Teichmuller-space, Riemann-surface-moduli, extremal-quasiconformal, and Teichmuller quadratic-differential terms; not an anchor audit or global absence claim |
| `python3 -B Stage1_Instances/THM-M-0256/check_intake.py` | 1 | known phase-evolution failure: the intake-only checker expects its pre-integration execution-DAG state `[ ]`, while the integrated DAG records intake `[_]`; its historical hashes and closed artifact inventory are also not statement-phase evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-0256/statement-blocker.json` | 0 | structured blocker parsed as valid JSON |
| prohibited-construct `rg` over target Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped tracked and added-file whitespace checks | 0 | no whitespace diagnostics in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test exists because the assigned statement deliverable is blocked |

The historical intake validator is intentionally not claimed as a current statement check: its
receipt is bound to pre-integration revision `a8aba97a7ef2ff387e7814fe517e1b35524a04dc` and older
blueprint/DAG snapshots, while this statement run starts from the integrated revision above.
Rewriting that integrated provisional intake history is outside this phase and is unnecessary to
establish the present source-statement blocker.

## Retry condition and status boundary

An accountable reviewer must preserve and hash an immutable primary or authoritative source,
identify and transcribe one exact proposition with a theorem/page locator and incorporated
definitions, audit corrections and errata, reconcile the catalog's 1939 identity/date with the
selected source, and independently approve the crosswalk. The selection must freeze the surface
type and genus, punctures and boundary, finite-type and stability conditions, marking and
equivalence conventions, automorphism treatment, Teichmuller-space versus coarse/orbifold/stack
moduli semantics, every ordered binder and hypothesis, the exact conclusion, and all boundary
cases. A later statement worker can then encode that same claim, minimize pinned imports, serialize
and hash its elaborated expression and environment, check alternate transports, and run all four
required mutation classes.

This is the first failed gate, not completion of the statement node or any downstream node. The
root remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no
debt-vector change is proposed. The assigned phase is not genuinely self-tested to its completion
gate, so no `.stage1-worker-selftest.json` is emitted and no node-specific completion or
master-acceptance receipt is claimed. Master acceptance of the provisional intake remains an
additional prerequisite for any eventual accepted statement transition.
