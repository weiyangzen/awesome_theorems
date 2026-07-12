# Exact-statement gate: blocked

Item: `S56-M-1434-STATEMENT`

Theorem: `THM-M-1434`

Base revision: `00890977f5ac2d94be2403ddfafae007a79c69f0` (tree
`061723c466c8cd25b6dc1d49dc72524392c756aa`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1434-INTAKE` has provisional worker
state `[_]`, which permits this statement attempt, but it has no master acceptance. The exact Lean
4 target cannot be truthfully elaborated from the authoritative repository record. That record
supplies only the title, Dennis Sullivan, 1985, and the gloss "no wandering domains for rational
functions." Its `verified` label is untrusted metadata under rev-5.6.

The primary-source lead is Sullivan's 1985 Annals article, *Quasiconformal homeomorphisms and
dynamics I. Solution of the Fatou-Julia problem on wandering domains*. The official journal page
confirms the bibliography but says no abstract is available and exposes neither the article text
nor a theorem locator. Fresh OpenAlex and Semantic Scholar checks reported closed access and no
usable full text. No immutable exact theorem passage, definitions, proof boundary, corrections,
errata, translation review, or independent source approval was therefore available for this phase.

The familiar textbook formulation cannot be selected from memory. Doing so would invent all of
the following proposition-changing choices:

- the analytic Riemann-sphere model and topology;
- how a rational function becomes a total self-map at finite poles and infinity;
- the exact degree or nonconstancy hypothesis;
- the normal-family definition of the Fatou set;
- the connected-component representation and induced forward map;
- pointwise image equality versus equality of containing components;
- iteration indexing and witnesses for a genuinely positive period; and
- constant and degree-one maps, empty or whole-sphere Fatou sets, poles, infinity, critical points,
  exceptional orbits, and minimal-period conventions.

These choices yield inequivalent or not-yet-transported encodings. A polynomial-only result, an
algebraic `RatFunc` statement without total analytic sphere dynamics, a Julia-set fact, a periodic
component classification, or generic component/iteration APIs would be a substituted theorem.

Consequently the rev-5.6 exact source-statement identity gate fails before there is a canonical
human proposition to encode. There is no exact Lean expression on which to certify minimal
imports, serialize an expression and environment fingerprint, compile alternate transports, or
run the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations. Those four mutation classes are undefined, not passed. No `Statement.lean`, surrogate
predicate, theorem declaration, axiom, placeholder, or broadened special case was added.

## Pinned Lean boundary

The existing `IntakeProbe.lean` directly imports five pinned mathlib modules and successfully
re-elaborates nine adjacent algebraic-rational, meromorphic, compactification, connected-component,
iterate, and periodic-point interfaces. It states no no-wandering-domain theorem. Its imports are
therefore discovery candidates only and cannot be called minimal for an unidentified target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The `lean-toolchain`, `lake-manifest.json`, and probe
SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`d3f792091bec104b2899bd4880e88d63aabad7f2843183d4f03bd3b8f0865f5e`.

The automation-provided `Formalizations/Lean/.lake` link points to the canonical pinned artifacts
and was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1434` | 0 | rank 932, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all; git rev-parse HEAD; git rev-parse 'HEAD^{tree}'; readlink Formalizations/Lean/.lake` | 0 | before this attempt, only the automation-provided `.lake` link was untracked; the base revision and tree are recorded above |
| source record, Stage0, manifest, blueprint, skill, and intake dossier inspection | 0 | only a one-line source gloss exists; the intake leaves the exact claim and formal target null and enumerates proposition-changing choices |
| official journal page, OpenAlex, and Semantic Scholar discovery | 0 | bibliography confirmed; no abstract, theorem text, open-access URL, or usable full text was exposed |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1434/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; no canonical target was stated |
| pinned mathlib revision, tree, and status inspection | 0 | revision and tree match the fingerprint above; package worktree clean |
| bounded Sullivan/wandering-domain/Fatou/Julia/complex-dynamics source-name search | 1 | expected no-match exit; discovery only, not an anchor audit or global-absence claim |
| `python3 -B Stage1_Instances/THM-M-1434/check_intake.py` before adding blocker artifacts | 1 | the historical intake checker requires the intake worker's absent root self-test manifest; this phase does not recreate or rewrite provisional intake evidence |
| JSON parsing and scoped blocker assertions | 0 | item identity, null target/imports, undefined mutations, unchanged vector, false completion flags, and no-self-test boundary agree |
| prohibited Lean proof-escape scan over `Stage1_Instances/THM-M-1434` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped tracked and added-file whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the statement deliverable is blocked |

## Retry condition and status boundary

Accountable reviewers must preserve and hash an immutable primary or authoritative source; pinpoint
and transcribe the exact theorem and every incorporated definition, hypothesis, conclusion,
exception, correction, and erratum; freeze the sphere, rational-map, Fatou-set, component-action,
equality, iteration, period, and boundary conventions; and independently approve the
source-to-target mapping. A later statement worker can then encode that same claim using real Lean
definitions, minimize its pinned imports, serialize and hash the elaborated expression and
environment, compile every credited transport, and run all four required mutation classes.

Master acceptance of the intake must also occur before an accepted statement transition, though
it was not the substantive reason this worker attempt stopped.

The first failed gate is exact source-statement identity. The root remains `[H1, M4, R3]`, with
`audit_complete: false` and `theorem_complete: false`; no debt-vector change is proposed. This is
blocked-attempt evidence, not completion of the statement node or any downstream node. Because the
assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted and no worker `[_]`, receipt, or master acceptance is
claimed.
