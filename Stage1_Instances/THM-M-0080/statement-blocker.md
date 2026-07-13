# THM-M-0080 exact-statement gate: blocked

Item: `S56-M-0080-STATEMENT`

Base revision: `48abbb2d2eeb89816c5ffc0ad8faafa4b9d24dd0` (tree
`0f26e2c78fb5fff9277cbbdfef5e145fd4ef06f1`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0080-INTAKE` has only provisional
worker state `[_]`; its unsigned receipt has `accepted: false` and no accepted receipt IDs. More
importantly, the intake deliberately leaves the binder-complete canonical proposition, Lean
declaration, minimal imports, elaborated-expression fingerprint, and canonical-target environment
fingerprint unresolved.

The inspected 1934 source does identify the intended theorem family. Kurosch's Section 2 headline
on printed page 651 says that, when `G` is the free product of component subgroups `H_alpha`, every
subgroup `F` of `G` can be decomposed as a free product `F = * F_beta`, with every `F_beta` either
infinite cyclic or conjugate in `G` to a subgroup of one component. Footnote 5 permits a product
with one factor. The headline does not add modern double-coset indexing, a packaged free factor,
uniqueness, rank, or canonicality.

That working translation is not yet sufficient to choose an exact Lean proposition. The source's
incorporated free-product definitions and the theorem passage have not received independent German
transcription and translation review, a complete definition/assumption/proof-node and boundary
crosswalk, an expanded correction and erratum audit, or accountable source approval. Those open
reviews control proposition-changing choices:

- the index and carrier universes and whether the ambient object is the external
  `Monoid.CoprodI G` or an internal free product with explicit component embeddings;
- the existential factor index and whether factors are subgroups of the ambient product or of the
  subgroup carrier;
- the exact infinite-cyclic predicate, including the trivial-group convention;
- equality, `MulEquiv`, or transported equality for ambient conjugacy and its left/right convention;
- the exact meaning of "can be decomposed", which must assert that the free product of the factors
  is the whole subgroup rather than only generating it; and
- empty and singleton component families, trivial components, an empty factor family, bottom and
  top subgroups, trivial conjugate intersections, and universe-lifted carriers.

These are not cosmetic encodings. Selecting a familiar modern formulation would either strengthen
the root with double-coset representatives or a named free factor, or silently choose conventions
the admitted evidence has not fixed. Replacing the claim with Nielsen-Schreier, a free-product
normal form, injectivity of component maps, or the fact that a free product of free groups is free
would substitute a different theorem.

Sections 5 and 5.1 of the rev-5.6 standard make unresolved statement identity and a missing
expression fingerprint hard blockers. No `Statement.lean`, canonical declaration, import-minimality
claim, expression/environment fingerprint, alternate-form credit, or mutation fixture was created.
The removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations are undefined,
not passed. No proof evidence was inspected or credited, and no axiom, placeholder, broadened
statement, or convenient substitute was introduced.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned toolchain. Its sole import is
`Mathlib.GroupTheory.CoprodI`, and it checks twelve free-product, reduced-word, free-group, and
subgroup interfaces. The complete output is 18 lines and 1796 bytes with SHA-256
`3e17d30f52671e0bc1e325a2d7cd109ab6e0f91cba4704929041f93ca240d50d`.

This is discovery evidence only. The probe declares no canonical Kurosh target, source transport,
or proof body, so its import cannot be certified minimal for an absent target. A bounded search of
the worker-local Lean sources and pinned mathlib found no Kurosh subgroup-decomposition declaration;
an unrelated ring-theory comment about the Kurosh problem and free-product infrastructure were the
only other topic matches. This is not a global absence claim or the downstream anchor audit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or other
dependency mutation was run.

## Validation evidence

Commands ran on 2026-07-13 (`Asia/Shanghai`) from the repository root unless another working
directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0080` | 0 | rank 1529, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `.lake` link; base revision and tree are recorded above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions agree with the environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision/tree agree and the package worktree is clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0080/IntakeProbe.lean` | 0 | twelve adjacent interfaces elaborated; output fingerprint recorded above; no target or proof declared |
| bounded repository and pinned-mathlib topic search | 0 | no Kurosh subgroup-decomposition declaration found; discovery result only |
| `python3 -B Stage1_Instances/THM-M-0080/check_intake.py` | 1 | historical intake checker expects authority state `[ ]`, while integration now records provisional `[_]`; it is not current statement evidence and was not modified |
| prohibited declaration scan over the owned Lean file | expected no-match | no `sorry`, `admit`, `sorryAx`, axiom, bodyless constant, opaque declaration, or unsafe declaration |
| JSON parse and scoped blocker-invariant query | 0 | identity, null target/imports, unchanged vector, undefined mutations, false completion flags, and no-self-test boundary agree |
| new-file whitespace checks for both blocker artifacts | expected difference, no diagnostics | neither owned blocker file has a whitespace error |

## Retry condition

The integration lane must first accept fresh intake evidence. Accountable source and group-theory
reviewers must independently approve the transcription, translation, incorporated definitions,
complete theorem/proof crosswalk, correction disposition, and all boundary conventions above. A
formal reviewer must then freeze one source-identical external or internally transported
free-product encoding, its exact decomposition and conjugacy predicates, and any modern alternate
only through checked transports.

A fresh statement run can then encode exactly that approved claim, minimize pinned imports,
serialize the elaborated expression and environment, compile every credited transport, and run all
four mutation classes.

This is a blocked statement attempt, not completion of this or any downstream node. Lifecycle
remains `planned`; the root remains `[H1, M3, R4]`; `audit_complete` and `theorem_complete` remain
false. Because the assigned deliverable is not genuinely self-tested, no root
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.
