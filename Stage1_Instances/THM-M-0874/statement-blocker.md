# Exact-statement gate: blocked

Item: `S56-M-0874-STATEMENT`

Theorem: `THM-M-0874`

Base revision: `db4b8793e70ce8af74c9c9490acfa50aa3684d5e` (tree
`6434a20532ae7c523ad293e67a6228ab384bfb8a`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete catalog claim is the title `Babai算法`, the attribution Laszlo Babai, the year 2015,
and the gloss `图同构的准多项式算法` ("a quasipolynomial algorithm for graph isomorphism"). It
does not identify a source, proposition, incorporated definitions, ordered binders, hypotheses,
conclusion, proof boundary, correction history, reviewer, or formal artifact. Stage0 repeats the
gloss while explicitly leaving the formal system, definitions, premises, proof route, dependencies,
alternate forms, axioms, machine status, and artifacts open. The catalog's `已验证` label is
untrusted inventory metadata under rev-5.6.

The intake identifies the stable human result family but deliberately freezes no exact proposition.
Babai's arXiv `1512.03547v2`, Theorem 1.1.1, states String Isomorphism in quasipolynomial time and
Corollary 1.1.2 derives Graph Isomorphism. Its timing analysis was later invalidated. The author
update and UPCC note repair one recursive case while recording a separate Design Lemma correction;
Helfgott, Bajpai, and Dona's post-fix exposition states the repaired Graph Isomorphism result as
Corollary 1.2. These are strong source leads, but no lawfully preserved, independently accepted
bundle maps every incorporated definition, correction, assumption, and proof node. They support
the provisional `H1` boundary, not an approved source root.

The source-level shorthand also leaves proposition-changing choices unresolved:

- finite simple graph representation and canonical graph-pair serialization;
- valid, duplicate, padded, malformed, truncated, and unequal-order inputs;
- Boolean decision versus isomorphism witness, coset, or generating-set output;
- deterministic machine, totality and halting semantics, primitive step, and worst-case cost model;
- vertex count versus encoded length and the graph-to-string polynomial-overhead bridge;
- constants, exponent, logarithm base, threshold, rounding, and small-input convention in a bound
  such as `exp(C * (log n)^c)`; and
- ordered quantifiers, universes, typeclass context, boundary cases, and checked alternate
  encodings.

Selecting familiar definitions for these fields would invent formal scope. Plain decidability,
brute-force enumeration, membership in NP, a special graph class, String Isomorphism alone, a
generic computability statement, or an assumed solver would weaken or substitute the catalog
claim. None is admissible.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. The intake correctly leaves the canonical human statement, Lean module
and expression, minimal imports, and expression/environment fingerprints null while proposing the
provisional classification `[H1, M4, R4]`.
Without a canonical target, checked transports and the required removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations are undefined, not passed. No
`Statement.lean`, axiom, placeholder, invented computation interface, weakened target, or
broadened theorem was introduced.

The prerequisite `S56-M-0874-INTAKE` has provisional worker state `[_]`, not master-accepted state
`[x]`. Its receipt is unsigned, non-content-addressed, declares `accepted: false`, and contains no
accepted receipt ID. Its historical checker also freezes pre-integration blueprint bytes and now
fails closed. Section 10.2 permits this provisional statement attempt; intake master acceptance
remains independently required only before any future statement master closure.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates in the pinned environment. Its four direct imports
authenticate ten adjacent graph-isomorphism, language, computable-reduction, and Turing-machine
time APIs. They define neither a finite graph serialization nor the Graph Isomorphism language,
Babai procedure, quasipolynomial resource predicate, correctness theorem, graph-to-string resource
transport, or proof body. `ManyOneReducible` is not resource bounded, while
`TM2ComputableInPolyTime` is polynomial-specific. The imports are substrate evidence only and
cannot be certified minimal for an absent canonical target.

A bounded exact-topic search over repository-local and pinned-mathlib Lean sources found no Babai,
String Isomorphism, Coset Intersection, or quasipolynomial-time implementation. This is narrow
discovery evidence, not the downstream immutable anchor audit or a claim of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` link to canonical pinned artifacts was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository root unless
a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0874` | 0 | rank 1428; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| scoped manifest, blueprint, skill, guidelines, catalog, Stage0, and complete intake inspection | 0 | the received record does not freeze a binder-complete computation theorem; the intake deliberately leaves the canonical claim and formal target null |
| authority, source, intake, toolchain, lockfile, probe, and pinned-mathlib `sha256sum` checks | 0 | exact current fingerprints are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0874/check_intake.py` | 1 | the historical intake checker stops at stale receipt input `Docs/Stage1_Blueprint_rev-5.6.md`; historical evidence was preserved rather than rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions agree with the recorded environment |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree agree; the dependency worktree is clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0874/IntakeProbe.lean` | 0 | all ten adjacent APIs elaborated; complete stdout SHA-256 `c94680a938d92119c98702932b0d292219a326ffea96af8452fba086ee7bf61d`; no canonical target or proof body |
| bounded exact-topic Lean search excluding owned intake prose | 1, expected no match | no matching implementation was located; discovery only |
| prohibited Lean construct scan over the owned path | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse, scoped blocker assertions, and whitespace checks | 0 | identity, null target/imports, unchanged vector, undefined mutations, false completion flags, exact two-file scope, and clean whitespace agree |
| `test ! -e .stage1-worker-selftest.json` | 0 | the self-test manifest is intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition

Accountable source, algorithms, and formal reviewers must lawfully preserve and hash a complete
corrected source bundle, select one exact Graph Isomorphism proposition, and approve every
graph/input/output representation, machine and cost semantic, size measure, bound, reduction,
binder, hypothesis, conclusion, correction, erratum, and boundary choice. The integration lane must
also master-accept refreshed intake evidence before it can master-close a later statement result.

A fresh statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a truthful blocked-attempt record, not completion of the statement node or any downstream
node. Lifecycle remains `planned`; the item remains `[ ]`; the accepted baseline remains
`unclassified_L0`, while the unaccepted intake proposal remains `[H1, M4, R4]`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, proof credit, or master acceptance is claimed.
