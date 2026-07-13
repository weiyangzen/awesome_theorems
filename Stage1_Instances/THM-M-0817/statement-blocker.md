# Exact-statement gate: blocked

Item: `S56-M-0817-STATEMENT`

Theorem: `THM-M-0817`

Base revision: `748243faadc15828fb087059337fd05b7be9fdeb` (tree
`e46d642646f80980838b6f016f5d69b817bd464d`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The record supplies the name "Ramsey's theorem," Frank Ramsey attribution, the year 1930, and only
the gloss "arbitrarily large graphs contain large complete subgraphs or independent sets." It gives
no parameter binders, graph or coloring model, finite/infinite choice, threshold convention,
cardinality semantics, hypotheses, or boundary cases. Stage0 repeats that gloss while explicitly
leaving exact definitions and premises, proof structure, equivalent forms, axioms, and machine
artifacts open. The catalog's `verified` label is untrusted metadata under rev-5.6.

The predecessor `S56-M-0817-INTAKE` has provisional worker state `[_]`, not master-accepted state
`[x]`. Its receipt is unaccepted and non-content-addressed, and its canonical human statement, Lean
module/expression, elaborated-expression hash, and canonical-target environment fingerprint are
null. The historical intake checker now stops because it froze the intake cursor at `[ ]` while
the integrated authority records `[_]`; this statement attempt records that freshness boundary
rather than rewriting intake evidence.

Several proposition-changing variants fit the gloss. It may mean the finite symmetric graph
theorem, the asymmetric two-color theorem, the general finite edge-coloring theorem, an infinite
pair-coloring theorem, a higher-arity theorem, or existence or leastness of a Ramsey threshold. A
finite formulation must still choose `Fin N`, arbitrary finite carriers, or finite subsets; exact
or at-least cardinality; requested clique and independent-set sizes; and quantifier order. These
choices materially affect zero/one requested sizes, empty and singleton carriers, thresholds below
the requested size, and zero/one-color cases. The false literal reading that one fixed finite graph
contains homogeneous sets of every size must also be excluded by a source-approved quantifier
freeze.

The intake identifies F. P. Ramsey's 1930 paper bibliographically, but no primary result passage,
incorporated-definition chain, proof boundary, correction audit, or independent statement review is
available. The inspected Bergerova 2022 secondary article states both a general finite
edge-coloring theorem and a separate asymmetric least-Ramsey-number formulation; it confirms the
family but does not select the catalog target. Choosing either would therefore narrow, broaden, or
substitute mathematics rather than elaborate an exact frozen claim.

Consequently there is no honest canonical expression whose direct imports can be certified
minimal, no expression fingerprint, no credited alternate encoding, and no meaningful
removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation. No
`Statement.lean`, theorem declaration, axiom, placeholder, or assumed Ramsey interface was added.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its single direct import,
`Mathlib.Combinatorics.SimpleGraph.Clique`. It checks clique, independent-set,
exact-cardinality, and complement APIs. All eight checks elaborate, but these are graph-language
ingredients only. They neither select nor state a Ramsey theorem, and the import cannot be claimed
minimal for an absent canonical target.

A bounded case-insensitive search of repo-local Lean and pinned mathlib found only contributor
names and prose describing Hales-Jewett or Hindman's theorem as Ramsey theory. No combinatorial
Ramsey terminal declaration was identified. This is narrow statement-feasibility evidence, not the
downstream exhaustive anchor audit or a global absence claim.

The pinned environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository
root unless another working directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0817` | 0 | rank 1376; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` before editing | 0 | only the automation-provided untracked `.lake` symlink existed; base revision and tree are recorded above |
| catalog, Stage0, manifest, blueprint, execution DAG, skill, and intake-dossier inspection and hashing | 0 | the source gloss does not select one proposition; intake canonical-target fields remain null |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake identities recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned mathlib revision/tree recorded above; package source worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0817/IntakeProbe.lean` | 0 | eight adjacent graph APIs elaborated; stdout SHA-256 `4074040d350cd3bb41abb8ad2fb65d34c41c400f486cdc1adba082716c86bc44`; empty stderr |
| bounded `Ramsey` search in repo-local Lean and pinned mathlib | 0 | nine unrelated name/prose matches; no combinatorial terminal declaration; discovery only |
| `python3 -B Stage1_Instances/THM-M-0817/check_intake.py` | 1 | historical intake replay stops at line 130 because it freezes intake `[ ]` while current authority records `[_]`; it was not rewritten or credited |
| prohibited Lean declaration scan over the owned path | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless `constant`, `opaque`, or `unsafe` declaration |
| structured JSON and scoped invariant checks | 0 | blocker identity, null target/imports, unchanged vector, four undefined mutations, false completion flags, two-file scope, authority fingerprints, and absent self-test agree |
| newline/trailing-whitespace checks, `git diff --check`, and per-new-file no-index checks | 0 for diagnostics; 1 expected per new-file comparison | both blocker files end in LF and have no whitespace diagnostics; no-index status 1 records each intentional new file |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because exact target elaboration did not pass |

## Retry Condition And Status Boundary

The integration lane must first revalidate and master-accept the intake. Accountable reviewers must
then lawfully preserve and hash one immutable primary or approved authoritative source, select and
independently approve one exact result and proof boundary, and map every incorporated definition,
parameter, hypothesis, conclusion, translation, correction, erratum, and boundary case. They must
freeze finite/infinite scope, graph/coloring model, symmetric/asymmetric parameters, number of
colors, carrier and finiteness representation, threshold existence or leastness, cardinality and
witness semantics, ordered quantifiers, foundation profile, and all degenerate cases.

A later statement run can encode only that accepted source claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four required semantic mutation classes.

This is evidence for a truthful first-gate blocker, not completion of the assigned deliverable.
Lifecycle remains `planned`; the root remains `[H1, M4, R4]`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change, statement receipt, worker `[_]`, proof credit, or
master acceptance is claimed. Because the phase is not genuinely self-tested to its completion
gate, no `.stage1-worker-selftest.json` is emitted.
