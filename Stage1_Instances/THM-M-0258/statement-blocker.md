# Exact-statement gate: blocked

Item: `S56-M-0258-STATEMENT`

Theorem: `THM-M-0258`

Base revision: `f294137feee7840fd105a4d3f6073d5cf45508ea` (tree
`234b8f273d252c2c42ce6860315ed973049c871a`).

## Decision

The exact Lean 4 target cannot be truthfully frozen or elaborated from the authoritative repository
record. The complete received mathematical metadata is the title `沃尔夫-登乔定理`, the attribution
Hartmut Wolf/Ken'ichi Ohshika, the year 1990, and the gloss `泰希米勒空间的边界` ("boundary of
Teichmuller space"). These fields do not form a truth-valued proposition with ordered binders,
hypotheses, and a conclusion. Stage0 explicitly leaves the formal system, precise definitions and
premises, proof route, equivalent forms, axioms, and formal artifact open. The catalog label
`已验证` is untrusted metadata under rev-5.6.

The title resembles a transposed rendering of the classical Denjoy-Wolff theorem about iterates of
holomorphic self-maps. The attribution and gloss instead point toward unidentified Teichmuller or
Kleinian geometry. The catalog does not identify a primary source, corroborate a joint Wolf/Ohshika
theorem, choose a dynamics domain or a surface type, select a boundary or compactification model,
or state what is to exist, converge, embed, be identified, or be classified. The intake's
bibliographic leads distinguish several nearby theorem families but were not admitted as an exact
source statement.

Selecting the classical Denjoy-Wolff theorem, a Thurston, Bers, Gardiner-Masur, Weil-Petersson, or
horofunction boundary theorem, a Michael Wolf harmonic-map degeneration theorem, or an Ohshika
deformation-space theorem would replace the missing mathematics. Those alternatives have different
domains, hypotheses, conclusions, and boundary cases. No such substitution was made.

The intake therefore deliberately leaves `canonical_statement`, `canonical_claim`, the Lean module
and expression, the elaborated-expression hash, and the target environment fingerprint null. Its
provisional worker state `[_]` permits dependency-ordered preparation, but its receipt is not
accepted and supplies no master acceptance.

Section 5.1 of the rev-5.6 standard fails first at exact source-statement identity. There is no
canonical expression for which imports can be certified minimal. Checked alternate transports and
the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
are undefined, not passed. No surrogate definition, theorem declaration, axiom, placeholder,
broadened interface, or convenient special case was added. The root remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` directly imports four pinned mathlib modules and re-elaborates
eight adjacent unit-disc, Schwarz, manifold, and one-point-compactification interfaces. It defines
neither a Denjoy-Wolff target nor a Teichmuller space or boundary and states no theorem for this
item. Its successful elaboration is a substrate check only; its imports are not claimed to be
minimal for the unknown root and receive no statement or proof credit.

A bounded exact-topic search over repo-local and pinned mathlib Lean files found no Denjoy-Wolff,
Wolf/Ohshika, Teichmuller-space, or named Teichmuller-boundary target. Unrelated occurrences of
Teichmuller-Tukey, Teichmuller lifts, and local class-field-theory Teichmuller names were excluded.
This is narrow feasibility evidence, not the downstream anchor audit or proof of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The `lean-toolchain`, `lake-manifest.json`, and probe
SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`87fb153047e8e8cd9b9027c4944fb31a950428a38cfeb1e05a56e1c73cc4b6ce`.

The automation-provided `Formalizations/Lean/.lake` link points to the canonical pinned artifacts
and was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0258` | 0 | rank 1266, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all; git rev-parse HEAD 'HEAD^{tree}'; readlink Formalizations/Lean/.lake` | 0 | before this attempt, only the automation-provided `.lake` link was untracked; base revision, tree, and link target were recorded |
| catalog, Stage0, manifest, blueprint, execution DAG, skill, and intake-dossier inspection | 0 | the records supply only the internally mismatched metadata tuple and leave the canonical claim and formal target null |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake match the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status inspection | 0 | pinned mathlib revision and tree match; its source worktree is clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0258/IntakeProbe.lean` | 0 | all eight adjacent APIs elaborated; stdout SHA-256 `5ec5d2e656509f2115e3991d380ccc17d8743575569c2c442f2a913af9c2d7e4`; no canonical target was stated |
| bounded exact-topic search over repo-local and pinned mathlib Lean sources | 1 | expected no-match exit after excluding unrelated names; no target declaration found; discovery only |
| `python3 -B Stage1_Instances/THM-M-0258/check_intake.py` before blocker artifacts were added | 1 | known phase-evolution failure: the intake checker freezes authoritative intake state `[ ]`, while the integrated DAG now records provisional `[_]`; this phase did not rewrite historical intake evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-0258/statement-blocker.json` | 0 | structured blocker parsed as valid JSON |
| scoped statement-blocker invariant check | 0 | item identity, open blocked state, null target and imports, four undefined mutations, unchanged `H5/M4/R4`, false completion flags, and absent self-test agree |
| prohibited Lean proof-escape scan over `Stage1_Instances/THM-M-0258` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped tracked and added-file whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the statement deliverable is blocked |

## Retry Condition And Status Boundary

An accountable source reviewer must preserve and hash an immutable primary or approved
authoritative edition, correct and independently approve the catalog identity, and transcribe one
exact truth-valued proposition and every incorporated definition with pinpoint locators. The review
must map all assumptions and the proof boundary, verify attribution, date, translation, corrections,
and errata, and freeze the domain or surface, map or family, ordered binders, hypotheses, conclusion,
convergence or boundary semantics, compactification and topology, equivalence relation, and all
degenerate cases.

A later statement worker can then encode that same claim, minimize pinned imports, serialize and
hash the elaborated expression and environment, compile every credited transport, and run the four
required mutation classes. Master acceptance of the intake is also required before an accepted
statement transition.

The first failed gate is exact source-statement identity. This is blocked-attempt evidence, not
completion of the statement node or any downstream node. `statement_elaborated`, `audit_complete`,
and `theorem_complete` remain false; no debt-vector change or accepted receipt is proposed. Because
the assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted and no worker `[_]` claim is made.
