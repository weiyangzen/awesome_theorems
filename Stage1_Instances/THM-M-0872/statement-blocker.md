# THM-M-0872 exact-statement gate: blocked

- Item: `S56-M-0872-STATEMENT`
- Base revision: `db4b8793e70ce8af74c9c9490acfa50aa3684d5e`
- Base tree: `6434a20532ae7c523ad293e67a6228ab384bfb8a`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the admitted repository record. The
complete catalog claim is `树宽的线性时间近似` (a linear-time approximation of treewidth), under
the label `Bodlaender算法`, attribution Hans Bodlaender, and year 1996. It does not state an
approximation factor, whether a number or decomposition is returned, the graph/decomposition and
width conventions, parameter policy, algorithm, correctness clauses, cost model, ordered binders,
hypotheses, conclusion, or boundary cases. Therefore it is not one stable truth-valued proposition.

The year-matched source lead cannot silently repair the record. Hans L. Bodlaender's 1996 article
*A Linear-Time Algorithm for Finding Tree-Decompositions of Small Treewidth*, DOI
`10.1137/S0097539793251219`, is summarized as an exact fixed-parameter result: for constant `k`,
decide in linear time whether a graph has treewidth at most `k` and, in the positive case, return a
tree decomposition of width at most `k`. That is not the catalog's approximation wording. Intake
admitted bibliographic metadata and a source-family summary only; the publisher body returned HTTP
403, and no immutable theorem passage, incorporated definitions, proof, correction audit, or
independent source review was admitted. Choosing the exact fixed-`k` theorem or a later
approximation theorem here would substitute proposition-changing mathematics.

The prerequisite `S56-M-0872-INTAKE` is also only provisional `[_]`: its receipt is unsigned,
non-content-addressed, `accepted: false`, and has no accepted receipt ID. Rev-5.6 section 10.2
permits preparing this later-node blocker, but master closure remains dependency ordered. Its
historical checker now stops on the blueprint hash changed by integration; this statement attempt
records that freshness boundary rather than rewriting intake evidence or generated authority.

The decisive statement failure is independent of that dependency. Rev-5.6 sections 5 and 5.1 make
statement ambiguity and a missing elaborated-expression fingerprint hard blockers. The intake
deliberately leaves the canonical human statement, Lean module/expression, ordered binders,
hypotheses, conclusion, alternate encodings, expression hash, and canonical-target environment
fingerprint null or empty. Consequently minimal imports, checked transports, and the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined,
not passed. No `Statement.lean`, proxy predicate, theorem declaration, proof body, broadened
interface, or special case was added. The vector remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates under the pinned environment with two
direct imports:

- `Mathlib.Combinatorics.SimpleGraph.Acyclic`
- `Mathlib.Computability.TuringMachine.Computable`

Its nine checks expose finite-simple-graph, graph-tree, Turing-machine, and step-bound interfaces.
The one axiom report contains `propext`, `Classical.choice`, and `Quot.sound`. These imports provide
no bag family, tree decomposition, width, treewidth, Bodlaender algorithm, approximation guarantee,
fixed-parameter correctness theorem, or linear-time theorem. They cannot be certified minimal for
an absent target and receive no statement or proof credit.

A bounded case-insensitive search over pinned mathlib, repo-local Lean, and this owned path matched
only the probe disclaimer and an unrelated phrase about theorem-tree decomposition. It located no
treewidth, tree-decomposition, or Bodlaender declaration. This is narrow statement-feasibility
evidence, not the downstream anchor audit and not a global formal-absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No `lake update`, `lake build`, dependency clone/fetch, or other `.lake` mutation ran.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Lean commands ran from
`Formalizations/Lean`; all others ran from the repository root. Exact argument, result, input hash,
and output hash records are preserved in `statement-blocker.json`. That JSON is a repository-local
worker blocker report, not a statement receipt or accepted-state artifact.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0872` | 0 | rank 1426; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| authority, source, complete-intake, toolchain, lockfile, and direct-mathlib-source `sha256sum` checks | 0 | current digests are preserved in the structured blocker |
| pinned Lean, Lake, and mathlib revision/tree/status checks | 0 | expected versions and clean pinned mathlib worktree |
| `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0872/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; stdout SHA-256 `dc19fff3...927`; no target declaration |
| bounded exact-topic search | 0 | only two non-target prose matches; output SHA-256 `dcfc2de6...cb7` |
| `python3 -B Stage1_Instances/THM-M-0872/check_intake.py` | 1 | historical intake replay stopped at stale `Docs/Stage1_Blueprint_rev-5.6.md`; output SHA-256 `a9e69cd5...25b1` |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, blocker-invariant, whitespace, scoped-change, and absent-self-test checks are also
recorded in the structured report.

## Retry Condition And Status Boundary

The integration lane must master-accept a fresh intake receipt bound to current authority.
Accountable source, graph-algorithm/complexity, and Lean reviewers must preserve one immutable
primary or approved authoritative source and independently approve one exact proposition. They
must resolve approximation versus exact fixed-`k` recognition and construction; crosswalk every
incorporated definition, premise, conclusion, proof boundary, correction, and erratum; and freeze
the graph, decomposition, width, parameter, algorithm/output, encoding, correctness, cost,
quantifier, hypothesis, and degenerate-case semantics without borrowing scope from `THM-M-0870` or
`THM-M-0871`.

A fresh statement worker may then encode precisely that reviewed claim, minimize its pinned direct
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt change is proposed. Because the exact-statement deliverable did
not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master
acceptance is claimed.
