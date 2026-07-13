# Exact-statement gate: blocked

Item: `S56-M-0766-STATEMENT`

Theorem: `THM-M-0766`

Base revision: `db4b8793e70ce8af74c9c9490acfa50aa3684d5e` (tree
`6434a20532ae7c523ad293e67a6228ab384bfb8a`).

Attempt date: 2026-07-13 (`Asia/Shanghai`).

## Decision

The assigned statement node remains `[ ]`. The repository source record supplies only the object
name "linear-bounded automaton," the gloss "context-sensitive languages," a Seymour
Ginsburg/Sheila Greibach attribution, and the year 1963. It gives no
truth-valued proposition, bibliography, source passage, definition chain, ordered binders,
hypotheses, conclusion, or proof boundary. Stage0 repeats the gloss while explicitly leaving the
precise definitions and premises open. The catalog's source-status label is untrusted metadata
under rev-5.6.

The integrated intake therefore correctly freezes a concept family at `[H5, M4, R4]`, not a
theorem statement. At least three materially different roots remain compatible with the record:

1. a definition and operational semantics for a linear-bounded automaton;
2. Landweber's 1963 one-way result from deterministic LBA acceptance to type-1 generation;
3. Kuroda's 1964 equivalence between nondeterministic LBA acceptance and context-sensitive
   generation.

The repository separately assigns the explicit CSL/LBA equivalence to `THM-C-0152` and Kuroda
1964. Treating that neighboring target as this item's statement would be an unapproved target and
ownership correction. The bounded source audit also did not locate a matching joint
Ginsburg/Greibach 1963 theorem; their relevant joint mapping paper is from 1966 and concerns a
different result family. Selecting any familiar formulation would therefore invent or substitute
proposition-changing mathematics.

Even after selecting a root, the statement must fix deterministic versus nondeterministic
transitions; existential versus unique runs; one-tape versus multitape storage; exact-input-cell,
endmarker, or constant-factor tape bounds; alphabet, blank, head-motion, initial-configuration,
halting, and acceptance conventions; grammar syntax and derivation; the noncontracting versus
context-sensitive production convention; the special start-to-empty rule; and empty alphabet,
empty language, empty word, and zero-length-input behavior. It must then freeze language equality
or implication direction, ordered binders, finiteness and decidable-equality assumptions, and all
representation transports. These choices are not mere notation.

The prerequisite intake has only provisional worker state `[_]`, not master-accepted state `[x]`.
Its receipt is unaccepted, non-content-addressed, and contains no accepted receipt ID. Independently
of that dependency boundary, its canonical human statement, Lean module and expression,
elaborated-expression hash, and canonical-target environment fingerprint are null. The historical
intake checker now stops because it froze the intake cursor at `[ ]` while current authority records
`[_]`; this statement attempt records that freshness boundary rather than rewriting intake evidence.

Consequently there is no canonical expression to elaborate, no direct import set that can
truthfully be certified minimal, no expression or environment fingerprint, and no credited
alternate encoding. The required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations are undefined, not passed. No `Statement.lean`, theorem declaration,
proof body, axiom, placeholder, weakened special case, or broadened theorem was added.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with its two direct imports,
`Mathlib.Computability.Language` and
`Mathlib.Computability.TuringMachine.Computable`. All twelve checks of `Language`, tapes,
deterministic `TM0` machines and configurations, stepping, reachability, initialization,
evaluation, finite support, and finite bundled `TM2` machines elaborated. Probe stdout has SHA-256
`e87dc22e0f0f4423a8d51bb494b1b2ce6d303303ef7ba0fbc4a5e1249e8eb82b`; stderr was empty.

These are adjacent generic interfaces only. The probe defines neither an LBA nor a
context-sensitive grammar and declares no canonical target, checked transport, or proof body. Its
imports therefore cannot be called minimal for an absent target and receive no statement or proof
credit.

A bounded case-insensitive search of repo-local Lean and pinned mathlib found only unrelated
Ginsburg citations about Presburger-semilinear languages and a multilinear bounded import. It
identified no LBA, context-sensitive-language, Kuroda, or matching Ginsburg/Greibach declaration.
This is narrow statement-feasibility evidence, not the downstream exhaustive anchor audit or a
global absence claim.

The pinned environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran inside this isolated worker clone on 2026-07-13, from the repository root unless a
different working directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0766` | 0 | rank 1352; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink existed; base revision and tree are recorded above |
| catalog, Stage0, separate CSL/LBA row, intake, git-blame, and source-lead inspection | 0 | the record is not one proposition; the deterministic one-way and nondeterministic equivalence roots differ, and target correction remains unapproved |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake identities recorded above |
| mathlib `git status --short`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | package worktree clean; pinned revision and tree recorded above |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0766/IntakeProbe.lean` | 0 | twelve adjacent APIs elaborated; stdout hash shown above; empty stderr; no canonical target or proof body |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 0 | six unrelated source-comment/import matches; no matching LBA/CSL declaration; discovery only |
| `python3 -B Stage1_Instances/THM-M-0766/check_intake.py` | 1 | historical intake replay fails at its frozen intake-state assertion because current authority records `[_]`; it was not modified or credited |
| prohibited Lean declaration scan over the owned path | 1, expected no match | no `sorry`, `admit`, `sorryAx`, axiom, bodyless constant, opaque, or unsafe declaration |
| JSON parse and scoped invariant checks | 0 | blocker identity, open state, provisional dependency, null target fields, unchanged vector, four undefined mutations, false completion flags, two-file scope, and absent self-test agree |
| newline/trailing-whitespace checks, scoped `git diff --check`, and per-new-file no-index checks | 0 for diagnostics; 1 expected per new file | both blocker files end in LF and have no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because exact-target elaboration did not pass |

## Retry Condition And Status Boundary

The integration lane must first revalidate and master-accept the intake dependency. Accountable
reviewers must then lawfully preserve and hash one immutable primary or approved authoritative
source, select and independently approve one exact proposition and proof boundary, and map every
incorporated definition, ordered binder, hypothesis, conclusion, translation, correction, erratum,
and boundary case. They must explicitly reconcile ownership with `THM-C-0152` and correct the
unsupported catalog attribution.

The accepted statement decision must freeze the deterministic or nondeterministic machine model,
tape-bound and endmarker convention, grammar and production model, derivation and acceptance
semantics, language representation, equality or implication direction, epsilon policy, universe
and finiteness assumptions, and all degenerate cases. A later statement run can then encode only
that reviewed claim, minimize its pinned imports, serialize and hash its elaborated expression and
environment, compile every credited transport, and run all four required semantic mutation
classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; the root remains `[H5, M4, R4]`;
`audit_complete: false` and `theorem_complete: false`. No debt-vector change, statement receipt,
worker `[_]`, statement fingerprint, proof credit, accepted state, or master acceptance is claimed.
Because the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json` is emitted.
