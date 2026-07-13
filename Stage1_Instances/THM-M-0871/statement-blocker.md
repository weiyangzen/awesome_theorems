# THM-M-0871 exact-statement gate: blocked

- Item: `S56-M-0871-STATEMENT`
- Base revision: `46a0f2a3ea74765a0467c489264b838ffbb70675`
- Base tree: `7b1b5269d7da840fd086da731d6f92903c209c35`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully frozen from the received source record. The catalog
supplies only `有界树宽图的MSO可判定性` (decidability of MSO on bounded-treewidth graphs), Bruno
Courcelle, 1990, and the untrusted status `已验证`. This identifies a theorem family, not one
binder-complete proposition.

The inspected primary sources expose materially different results. Courcelle's 1990 paper includes
decidable monadic theory for context-free or fixed bounded-expression-width graph classes and
linear evaluation of a fixed formula only when a bounded-width graph expression or grammar
derivation is supplied. Courcelle's 1992 paper connects treewidth to bounded expressions and gives
a quadratic fixed-formula, fixed-width route for bare finite hypergraphs, including a
decomposition or approximation boundary. The sources quantify over vertices, edges, vertex sets,
and edge sets, and the broader 1990 framework admits counting atoms.

These are not interchangeable encodings of one selected target. The repository does not choose:

- finite simple graphs, labeled graphs, hypergraphs, incidence structures, or relational structures;
- MSO1, edge-set MSO2, CMSO, or another language;
- decidability of a class theory, fixed-sentence truth, or uniform model checking;
- fixed or input formula, width, signature, grammar, expression, or decomposition;
- expression width, treewidth, incidence width, or the bridge between them;
- a bare graph, supplied decomposition, graph expression, or grammar derivation as input;
- Boolean, witness, certificate, decomposition, rejection, or class-validity output; or
- mere decidability, polynomial, quadratic, fixed-parameter, or linear time under a cost model.

Selecting a familiar modern finite-simple-graph MSO model-checking theorem would silently replace
the source-backed family. Selecting one of the 1990 or 1992 results without accountable review would
also invent the root-selection decision. First-order graph logic, treewidth alone, Bodlaender's
decomposition algorithm, a single fixed property, or a stored decision procedure is not a valid
substitute.

Boundary decisions are likewise proposition-changing: empty and singleton graphs, edgeless and
disconnected graphs, width-zero and width-one conventions, empty decompositions, loops and repeated
hyperedges, labels, formulas with no free variables, empty assignments, counting moduli, malformed
encodings, missing or incorrect decompositions, out-of-bound widths, zero-length expressions,
totality, halting, hidden formula-dependent constants, and input-size semantics all remain open.

Therefore there is no canonical human statement to encode, no exact Lean expression to hash, and no
meaningful way to claim minimal imports, checked alternate transports, or the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations. No theorem
declaration, axiom, placeholder, broadened interface, weakened special case, or substituted result
was added.

## Source boundary

The repository record at `Docs/researches/math_theorems.md:6383-6388` contains no bibliography,
definitions, binders, premise, conclusion, algorithm, cost model, correction record, reviewer, or
formal artifact. `Docs/Stage0_Blueprint.md:23765-23790` repeats the slogan while explicitly leaving
the exact definitions and premises, formal system, proof route, dependencies, alternate forms,
axioms, machine status, and artifacts open.

The uncredited source leads are:

- Bruno Courcelle, *The Monadic Second-Order Logic of Graphs. I. Recognizable Sets of Finite
  Graphs*, *Information and Computation* 85(1), 12-75 (1990), DOI
  `10.1016/0890-5401(90)90043-H`: Definitions 3.1-3.2, Theorem 4.4, Corollaries 4.8/4.10, and
  Proposition 4.14. The inspected scan has SHA-256
  `e5989841626dc08c5acea6fd6bfb8c2413ff86d9c5b16f80aba5c6cfb7f42acd`.
- Bruno Courcelle, *The Monadic Second-Order Logic of Graphs III: Tree-Decompositions, Minors and
  Complexity Issues*, *RAIRO-Theoretical Informatics and Applications* 26(3), 257-286 (1992), DOI
  `10.1051/ita/1992260302571`: Definition 2.1 and Proposition 3.1. The inspected scan has SHA-256
  `b73c2e11a5311f6f69ced7815d72ccc1b65cb476c24b4e3b4ac0f58acef08774`.

Neither lead is admitted as H0 or selected as the canonical root. Complete correction and
proof-node review, lawful source admission, and independent source/scope review remain open.
`THM-M-0870` separately owns treewidth/decomposition scope, and `THM-M-0872` separately owns
Bodlaender's treewidth algorithm scope. Any future combined theorem needs an explicit checked
composition boundary.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports `Mathlib.ModelTheory.Graph`,
`Mathlib.Combinatorics.SimpleGraph.Acyclic`, and
`Mathlib.Combinatorics.SimpleGraph.Maps`. It re-elaborates seven adjacent interfaces:

- `FirstOrder.Language.graph`;
- `SimpleGraph.structure` and `FirstOrder.Language.Theory.simpleGraph`;
- `FirstOrder.Language.simpleGraphOfStructure` and its structure transport;
- `SimpleGraph.IsTree`; and
- `SimpleGraph.Iso`.

These are first-order graph, simple-tree, and graph-isomorphism substrate only. The probe states no
MSO or CMSO syntax, tree decomposition, treewidth, model checker, complexity theorem, canonical
target, or proof body. Its three imports are not claimed to be minimal for an unknown target.

The pinned environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The SHA-256 values of `lean-toolchain`,
`lake-manifest.json`, and `IntakeProbe.lean` are, respectively,
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`d5c2489f9dd5505c6284b31963a732d002b8931c342f133c982d43d91ae95a12`.

The automation-provided `Formalizations/Lean/.lake` link to the canonical pinned artifacts was used
read-only. No `lake update`, `lake build`, dependency clone, fetch, or other `.lake` mutation ran.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0871` | 0 | rank 1425, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | pre-edit output showed only the automation-provided untracked `Formalizations/Lean/.lake` link |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `python3 -B Stage1_Instances/THM-M-0871/check_intake.py` | 1 | historical checker expects intake `[ ]` with zero attempts; current authority records provisional `[_]` with one attempt |
| `(cd Formalizations/Lean && lake --version && lean --version)` | 0 | Lake and Lean identities agree with the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree agree |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0871/IntakeProbe.lean)` | 0 | seven adjacent APIs elaborated; exact output SHA-256 `46545b575aee16710a489611c2038586516077463b8c24492139742a7bd0d860`; representative axioms only `propext` and `Quot.sound`; no target statement |
| bounded exact-topic `rg` over repo-local and pinned mathlib Lean, excluding one unrelated prose hit | 1 expected | no Courcelle, treewidth, graph MSO/CMSO, or matching model-checking declaration found; discovery only |
| prohibited-construct `rg` over target Lean sources | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0871/statement-blocker.json` | 0 | finalized structured blocker is valid JSON |
| scoped blocker invariant assertions | 0 | identity, open state, null target/imports, unchanged vector, false completion flags, exact owned scope, and absent self-test agree |
| `git diff --check` plus scoped no-index checks | 0 | no whitespace diagnostics; no-index exit 1 was accepted only as the normal added-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test is absent because statement completion failed |

The historical intake-checker failure is recorded rather than repaired: the current assignment does
not own the intake phase, and changing its frozen expectations would be unrelated to completing this
statement attempt.

## Retry condition and status boundary

The prerequisite intake is only provisional authoritative `[_]`, with one attempt and an unaccepted,
non-content-addressed receipt. It is not master-accepted `[x]`; this independently prevents accepted
statement closure.

After refreshed intake evidence is master-accepted, accountable reviewers must preserve one
immutable exact primary-source proposition and approve every graph/hypergraph, logic, formula,
width, decomposition, uniformity, input, output, encoding, cost, binder, premise, conclusion, proof,
correction, and boundary convention. They must reconcile the neighboring treewidth and Bodlaender
targets. A later statement worker can then encode only that claim, minimize its pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport, and
run all four mutation classes.

The first failed substantive gate is exact source-statement identity. The root remains
`[H1, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt-vector change is
proposed. This is blocked-attempt evidence, not completion of the statement node or any downstream
node. Because the assigned phase did not pass its completion gate, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, accepted state, statement
fingerprint, or proof credit is emitted.
