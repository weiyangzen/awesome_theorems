# Exact-statement gate: blocked

Item: `S56-M-0910-STATEMENT`

Theorem: `THM-M-0910`

Base revision: `fcabbf1e0ad9507eebe91663bccabfa87d22813e` (tree
`873e589c594454b7f263c7ed2342089a4d15e842`).

## Decision

The statement item remains `[ ]`. Its intake dependency has provisional state `[_]`, but the
receipt is unsigned, non-content-addressed, `accepted: false`, and not master-accepted. Its replay
checker is also stale after integration changed the authoritative intake row from `[ ]`, attempt 0,
to `[_]`, attempt 1. Those dependency defects already prevent an accepted transition.

Independently, the exact-statement gate cannot pass. The catalog records only the name
"Caucal theorem", Didier Caucal, 1996, and the gloss "graph decidability". It does not identify a
truth-valued proposition. The matching source family contains several inequivalent results:
preservation of monadic-theory decidability under rational graph transformations, decidability for
`REC_Rat`, a recognizable word-graph presentation theorem, and narrower pushdown/regular-graph
consequences. They have different graph classes, premises, binders, and conclusions. Selecting any
one merely because it is familiar would invent or substitute missing mathematics.

Therefore no canonical mathematical statement, Lean expression, minimal import set, expression
fingerprint, environment-expression fingerprint, credited transport, or statement mutation is
emitted. No `Statement.lean`, node receipt, or root `.stage1-worker-selftest.json` was created.

## Missing proposition data

An accepted source decision must freeze all of the following before a fresh statement attempt:

1. One immutable admitted edition and exact numbered result, with the 1996 proceedings, expanded
   manuscript, and 2003 journal relationship, corrections, and errata reconciled.
2. Directed labelled graph, root, accessibility, vertex and label carriers, equality or
   isomorphism convention, and the exact graph class and effective presentation.
3. The monadic second-order syntax and semantics, sentence encoding, set-variable interpretation,
   and the meaning of `MTh(G)`.
4. Per-graph versus uniform decidability, the inputs consumed by the decider, and whether the
   conclusion is a reduction to `S2S`, preservation, decidability, or an effective construction.
5. Rational languages, restrictions, substitutions, inverse edges, closure operations, every
   effectiveness hypothesis, ordered binder, universe, and typeclass assumption.
6. Empty graphs, absent roots, empty alphabets or rational languages, unreachable vertices,
   identity transformations, finite graphs, isomorphic presentations, closed sentences, malformed
   encodings, and other boundary cases.

Until those decisions receive independent source review, the four required mutation classes are
not meaningful: there is no approved hypothesis to remove, domain to change, binder scope to
alter, or boundary contract to test.

## Lean boundary

The existing `IntakeProbe.lean` re-elaborates with the pinned toolchain. Its imports expose only
adjacent first-order graph/model-theory, DFA/regular-language, and computability interfaces. They
do not encode monadic second-order vertex-set quantification, Caucal's transition-graph classes,
rational graph transformations, `S2S`, or the source reduction. Consequently those imports cannot
be certified as minimal imports for an absent canonical target.

The replay used Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). It printed the eleven adjacent interfaces and exited
0; complete output SHA-256 was
`843c8da1809c702af6c73a67aa4bf2362fbde7bb434e37ce2fddcc98f170a927`. A bounded exact-topic
search returned no match. This is feasibility evidence only, not a formal anchor audit or absence
claim.

## Validation results

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0910` | 0 | rank 1452; planned; L0/rework_required; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (pre-edit) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `python3 -B Stage1_Instances/THM-M-0910/check_intake.py` | 1 | historical checker stops at its exact intake-row assertion because it expects state `[ ]`, attempt 0, while current authority records `[_]`, attempt 1; intake artifacts were not rewritten |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 and Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree above; clean source worktree |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0910/IntakeProbe.lean)` | 0 | eleven adjacent declarations elaborated; 889 output bytes; SHA-256 `843c8da1...927`; no target or proof declaration |
| bounded `rg` for Caucal, `REC_Rat`, prefix-recognizable graphs, and decidable monadic theory | 1 (expected) | no match in pinned mathlib or repo-local Lean; discovery only |

The finalized structured artifact was then JSON-parsed and checked for identity, blocked state,
null target/import/fingerprints, unchanged `[H5, M4, R4]` vector, four undefined mutations, empty
receipt/fingerprint lists, false completion flags, exact changed paths, and absent worker self-test.
A prohibited-construct scan and new-file/scoped whitespace checks also passed.

No `lake update`, `lake build`, dependency clone/fetch, or other `.lake` mutation was run.

## Retry condition

The integration lane must revalidate and master-accept refreshed intake evidence. Accountable
reviewers must preserve and independently approve one exact source result with every incorporated
definition, premise, binder, conclusion, proof boundary, correction, erratum, presentation choice,
effectivity requirement, and boundary case. A fresh statement run may then encode precisely that
claim, minimize pinned imports, serialize the elaborated expression and environment, compile every
credited transport, and execute all four required mutation classes.

This blocker does not claim a statement, proof, receipt, audit completion, theorem completion, or
master acceptance.
