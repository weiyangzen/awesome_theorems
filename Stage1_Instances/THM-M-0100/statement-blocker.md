# Exact-statement gate: blocked

Item: `S56-M-0100-STATEMENT`

Theorem: `THM-M-0100`

Base revision: `ee8c1843ef3ce74178a990f4e64554c1558c51fa` (tree
`3a34df1cc2089854dc563ab4909cc0586713ad20`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only the title Kazhdan's Property (T), David Kazhdan, the year 1967, and the
gloss "a rigidity property concerning group representations." It contains no truth-valued
proposition, source citation, incorporated definition chain, ordered binders, hypotheses, or
conclusion. Its `verified` label is untrusted metadata under rev-5.6.

The intake identifies an authoritative modern source lead, B. Bekka, P. de la Harpe, and A.
Valette, *Kazhdan's Property (T)*, draft dated February 23, 2007. That source makes the ambiguity
concrete rather than resolving it. Definition 1.1.3 defines Property (T) through existence of a
compact Kazhdan set, while Proposition 1.2.1 states a distinct weak-containment characterization.
The same source gives Fell-topology characterizations, compact-generation consequences, examples,
lattice results, and a Property (FH) equivalence under additional hypotheses. The original 1967
paper has only been identified bibliographically; its proposition text has not been admitted or
crosswalked.

Selecting the compact-Kazhdan-set definition, the almost-invariant-vector characterization, one
consequence, one example, or an equivalence would therefore add or substitute mathematics absent
from the catalog. Even the source definition leaves proposition-affecting encoding work: the
topological-group and Hilbert-space models, strong continuity and unitarity, the supremum used for
`(Q, epsilon)`-invariance, compactness and separation conventions, positivity and strictness,
quantifier order, zero-dimensional spaces, empty sets, and all universes must be frozen against an
accepted source passage. No accountable selection, complete premise crosswalk, corrections audit,
immutable source admission, or independent review authorizes those choices.

Section 5.1 of the rev-5.6 standard requires one source-faithful target, minimal pinned imports, an
elaborated-expression serialization and environment fingerprint, checked alternate transports,
and mutations for a removed hypothesis, changed domain, changed binder scope, and boundary case.
Without a canonical proposition, none of those objects exists. The statement node remains `[ ]` at
`[H5, M4, R4]`; no statement, audit, theorem completion, receipt, or master acceptance is claimed.

## Pinned Lean boundary

The existing `IntakeProbe.lean` directly imports `Mathlib.RepresentationTheory.Invariants` and was
re-elaborated with the existing pinned Lake artifacts. It checks the algebraic `Representation`
type and three invariant-submodule declarations. Those APIs provide neither continuous unitary
representations, almost invariant vectors, compact Kazhdan sets, nor Property (T). Its import is an
adjacent discovery surface, not a minimal import for an unknown canonical target, and the probe
declares no theorem or proof body.

A bounded exact-name search located no `PropertyT`, `KazhdanSet`, `KazhdanPair`, or corresponding
Property (T) declaration in repo-local Lean or pinned mathlib. Broader Kazhdan hits concerned the
unrelated Kazhdan-Lusztig targets. This is feasibility evidence only, not the downstream anchor
audit or proof of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link was used read-only. No update, build, clone, fetch, or dependency
mutation was performed.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0100` | 0 | rank 1116, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all; git rev-parse HEAD 'HEAD^{tree}'; readlink Formalizations/Lean/.lake` | 0 | only the automation-provided `.lake` link was untracked; the recorded base and tree were otherwise clean |
| source record, Stage0, manifest, standard, execution skill, and intake dossier inspection | 0 | the catalog supplies a property-family label; the intake leaves the canonical mathematical and formal targets null and records inequivalent source surfaces |
| `git blame -L 733,738 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | the pinned revision and tree above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0100/IntakeProbe.lean` | 0 | four adjacent APIs elaborated; stdout SHA-256 `e8037fa1d003ad1b144494b54f4f931cc7131a5aeb8fa5801c84a94c6a962306`; no target or proof body |
| bounded exact Property (T)/Kazhdan API search in repo-local and pinned-mathlib Lean | 1 | expected no-match result; broader hits were unrelated Kazhdan-Lusztig material |
| `python3 -B Stage1_Instances/THM-M-0100/check_intake.py` | 1 | known historical replay failure: the intake checker freezes the earlier authoritative intake state `[ ]`, while integration now records provisional `[_]`; this statement run does not rewrite historical evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-0100/statement-blocker.json` plus scoped blocker assertions | 0 | structured blocker parsed and its identity, null statement gate, unchanged debt, four undefined mutations, change scope, and no-self-test boundary agreed |
| prohibited Lean declaration scan over `Stage1_Instances/THM-M-0100` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry condition

The intake dependency still requires master acceptance before an eventual accepted statement
transition. Accountable reviewers must lawfully preserve and hash a complete source edition,
select and transcribe one exact proposition with every incorporated definition, binder, hypothesis,
conclusion and proof boundary, audit corrections and translation, resolve every group,
representation, topology, Hilbert-space, compact-set, epsilon, vector and boundary convention, and
independently approve the mapping. A fresh statement run can then encode that same claim, minimize
its pinned imports, serialize and hash the elaborated expression and environment, check every
credited transport, and execute all four required mutation classes.

The first failed gate is exact source-statement identity. This is blocked-attempt evidence, not
completion of the statement node or any downstream node. Because the assigned phase is not
genuinely self-tested to its completion gate, no `.stage1-worker-selftest.json` is emitted.
