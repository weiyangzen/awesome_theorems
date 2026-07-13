# Exact-statement gate: blocked

Item: `S56-M-0893-STATEMENT`

Theorem: `THM-M-0893`

Base revision: `46a0f2a3ea74765a0467c489264b838ffbb70675` (tree
`7b1b5269d7da840fd086da731d6f92903c209c35`).

## Decision

The exact Lean 4 target cannot yet be truthfully frozen from the admitted repository record. The
catalog gives the family name "Bannai-Ito conjecture," attributes it to Eiichi Bannai and Tatsuro
Ito in 1984, and supplies only the gloss "a bound on the diameter of distance-regular graphs." It
cites no theorem and fixes no diameter inequality, valency quantifier, definition of
distance-regularity, graph model, finiteness or isomorphism convention, proof boundary, correction,
or erratum. Its `proved` label is untrusted metadata under rev-5.6.

The identified proof source is S. Bang, A. Dubickas, J. H. Koolen, and V. Moulton, *There are only
finitely many distance-regular graphs of fixed valency greater than two*, *Advances in Mathematics*
**269** (2015), 1-55, DOI `10.1016/j.aim.2014.09.025`. The inspected immutable preprint,
arXiv `0909.5253v1`, states as Theorem 1.1:

> There are only finitely many distance-regular graphs of fixed valency greater than two.

That standard root is materially more precise than the catalog gloss. Section 2.3 defines a
distance-regular graph as a finite connected graph whose nearer- and farther-layer neighbor counts
depend only on the distance between the selected vertices; regularity and valency follow. Section
2.3.2 explains that a diameter bound depending only on fixed valency would imply finiteness, while
also quoting the different Ivanov bound `D <= F(k) h`, which still depends on the graph through its
head `h`. These facts explain the gloss but do not make an unspecified diameter theorem,
Theorem 1.1, and Ivanov's intermediate inequality interchangeable.

The original conjecture locator reported by the proof paper is Bannai and Ito, *Algebraic
Combinatorics I: Association Schemes* (1984), p. 237. That page and its incorporated definitions,
edition history, corrections, and errata have not been preserved or independently accepted. The
published-versus-preprint proof delta, full assumption and proof-boundary map, exact relationship
to the catalog gloss, and independent source review also remain open.

Formal representation is separately unresolved. Mathlib has no identified distance-regular
predicate. A source-faithful target needs the complete intersection-layer definition, the outer
quantifier `k > 2`, and finiteness of finite connected simple graphs of valency `k` up to graph
isomorphism. Raw graphs over arbitrary carrier universes do not form the small collection asserted
by the theorem. Choosing a quotient of `Sigma n, SimpleGraph (Fin n)`, a finite representative set,
a bounded `Fin n` normal form, or another encoding changes foundation and transport obligations.
Distance-regularity and valency must be proved invariant under the chosen graph isomorphism.

The boundary cases are proposition-bearing. Valencies zero, one, and two are excluded; cycles make
the valency-two extension invalid. Empty, singleton, disconnected, diameter-zero, and diameter-one
graphs must be handled explicitly rather than hidden by mathlib's natural-valued diameter
convention. A bound on diameter, bounded vertex order, finitely many intersection arrays, and
finitely many labeled graphs are useful bridges but are not definitionally the same as finiteness
of graph isomorphism classes.

Selecting a familiar formal candidate before those source and representation decisions would
invent or substitute mathematics. Sections 5 and 5.1 of the rev-5.6 blueprint make statement
ambiguity and a missing elaborated expression fingerprint hard blockers. The intake correctly
leaves the canonical Lean module, expression, minimal imports, checked transports, and expression
and environment fingerprints open at `[H1, M4, R4]`. Without a canonical target, the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined,
not passed. No `Statement.lean`, axiom, placeholder, assumed classification, weakened theorem, or
broadened theorem was introduced.

The prerequisite `S56-M-0893-INTAKE` is only provisional worker state `[_]`, not master-accepted
state `[x]`. Its receipt is unsigned and non-content-addressed, declares `accepted: false`, and has
no accepted receipt ID. That does not prevent truthful blocker work, but master acceptance remains
independently required before a future statement transition can be accepted.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with the pinned environment and imports:

```lean
import Mathlib.Combinatorics.SimpleGraph.Diam
import Mathlib.Combinatorics.SimpleGraph.Finite
import Mathlib.Combinatorics.SimpleGraph.Maps
```

All eight adjacent graph, connectedness, regularity, metric, diameter, and isomorphism interfaces
elaborate. This is real environment evidence, but the probe defines no distance-regular predicate,
finite isomorphism-class carrier, Bannai-Ito target, source transport, or proof body. Its imports
therefore cannot be certified minimal for an absent target. For a noncanonical fixed-valency
candidate, `Metric` plus `Finite` appears to provide distance, finite neighborhoods, regularity, and
graph isomorphism; `Diam` would be necessary only if reviewers select a diameter surface. This is
an import feasibility observation, not a frozen target or minimal-import claim.

A bounded exact-topic search of repository-local and pinned-mathlib Lean sources found no
Bannai-Ito or distance-regular declaration. This is discovery-only feasibility evidence, not the
downstream immutable anchor audit and not a claim of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The `lean-toolchain`,
`lake-manifest.json`, and probe-output SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`9140602012137030e9c4172bc7a93e9e933520015fcb2c02cded02e3105f2f71`.

The automation-provided `Formalizations/Lean/.lake` link points to the canonical pinned artifacts
and was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai), from the repository root
unless a different working directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0893` | 0 | rank 1442, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped manifest, blueprint, skill, catalog, Stage0, intake, scope, and crosswalk inspection | 0 | the standard fixed-valency root is strongly identified, but its exact relationship to the catalog gloss and all source and formal representation choices remain open |
| `sha256sum` over authority, intake, probe, toolchain, Lake, and relevant pinned mathlib inputs | 0 | hashes agree with `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0893/check_intake.py` | 1 | historical intake replay stops at line 133 because it freezes intake authority state `[ ]` while current authority records provisional `[_]`; this statement worker records rather than rewrites historical evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree agree with the fingerprint; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0893/IntakeProbe.lean` | 0 | eight adjacent graph APIs elaborated; complete stdout SHA-256 is `91406020...2f71`; no canonical target was stated |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 1 | expected no-match exit; discovery only, not an anchor audit |
| prohibited Lean construct scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| JSON parse and scoped invariant check for `statement-blocker.json` | 0 each | IDs, blocked open state, null target and imports, unchanged vector, four undefined mutations, false completion flags, exact paths, final newlines, and absent self-test agree |
| whitespace checks for both new blocker artifacts | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then preserve and independently approve the original 1984 page and an authoritative proof edition;
select the exact finiteness root, diameter root, or explicit conjunction; and state a checked
relationship to the catalog gloss. They must freeze every incorporated definition, ordered binder,
hypothesis, conclusion, proof boundary, correction, erratum, graph model, distance-regular
convention, small isomorphism-class finiteness representation, foundation profile, and boundary
case.

A fresh statement worker can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
