# Exact-statement gate: blocked

Item: `S56-M-0836-STATEMENT`

Theorem: `THM-M-0836`

Base revision: `0c019b7194c9c43fa5f683fa82d637a0b275410d` (tree
`43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record gives the title `computer proof of the four-color theorem`, Appel/Haken, 1976, and the
gloss `reducible configurations and the discharging method for the four-color theorem`. The gloss
names a proof architecture, not one binder-complete truth-valued proposition. It supplies no
formula, domains, definition chain, fixed configuration inventory, computation artifact, proof
boundary, correction, erratum, or reviewer. Stage0 explicitly leaves the formal system, precise
definitions and premises, proof route, dependencies, alternate forms, axioms, machine state, and
artifacts open. The catalog's `verified` value is untrusted under rev-5.6.

The inspected Appel-Haken 1976 announcement states the ordinary theorem that every planar map can
be colored with at most four colors. It sketches an unavoidable set of reducible configurations,
discharging, and computer programs that checked the configurations. That source-family discovery
does not decide whether this separate catalog target owns:

1. the ordinary Four Color conclusion with Appel-Haken provenance;
2. an unavoidable-set theorem;
3. a fixed conjunction of configuration-reducibility results;
4. correctness of a specified historical program or certificate corpus; or
5. the complete Appel-Haken source suite with checked composition to the Four Color conclusion.

Those roots are not interchangeable. They have different domains, binders, conclusions,
computation contracts, and trust boundaries. The ordinary Four Color Theorem is separately
scheduled as `THM-M-0833`; silently selecting `every finite planar graph is four-colorable` here
would collapse target identity rather than elaborate this proof-method target. The 1977 Part I
*Discharging*, Part II *Reducibility*, and microfiche supplements remain discovery leads: their
primary texts, complete configuration inventory, programs, tables, certificates, correction map,
and independent review were not admitted by intake.

The map or graph model, planarity and embedding conventions, configurations and their occurrence,
ring and symmetry treatment, reducibility, unavoidability, charge and transfer rules, minimal-
counterexample reduction, finite inventory, program or certificate semantics, coverage,
completeness, termination, ordered binders, hypotheses, conclusion, and degenerate cases all
remain unapproved. Selecting any candidate now would invent, broaden, narrow, or substitute
proposition-changing mathematics.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression fingerprint
hard blockers. The intake therefore correctly leaves the canonical mathematical statement, Lean
module, exact expression, imports, and expression/environment fingerprints null at
`[H5, M4, R4]`. Without a canonical target, imports cannot be certified minimal, alternate
transports cannot be credited, and the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined, not passed. No `Statement.lean`,
axiom, placeholder, generic Four Color substitute, assumed planarity interface, or weakened theorem
was added.

The prerequisite `S56-M-0836-INTAKE` is only provisional worker state `[_]`, not master-accepted
`[x]`. Its receipt is unsigned, non-content-addressed, declares `accepted: false`, and has no
accepted receipt ID. Rev-5.6 section 10.2 permits provisional later-node preparation while
concurrency is enabled, but master acceptance remains independently required before a future
statement transition.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with these direct imports:

- `Mathlib.Combinatorics.SimpleGraph.Coloring`
- `Mathlib.Combinatorics.SimpleGraph.DegreeSum`

It authenticates generic `SimpleGraph.Coloring`, `SimpleGraph.Colorable`, chromatic-number,
finite-degree, and degree-sum interfaces plus one tiny bottom-graph coloring. The probe has no
planarity or embedding predicate, configuration calculus, reducibility theorem, discharging rules,
computation checker, source transport, canonical target, or proof body. The imports are therefore
candidate-interface evidence only and cannot be certified minimal for an absent target.

A bounded exact-topic search over repository-local and pinned-mathlib Lean sources returned no
Appel-Haken, Four Color, unavoidable-set, reducible-configuration, or discharging-method occurrence
under the recorded patterns. The coloring module separately lists planar graphs as future work.
This is narrow feasibility evidence, not the downstream immutable anchor audit or a claim of global
absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. Exact source and output SHA-256 values are recorded in
`statement-blocker.json`.

The automation-provided `Formalizations/Lean/.lake` link points to canonical pinned artifacts and
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`), from the repository root unless
a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0836` | 0 | rank 1393; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| scoped manifest, blueprint, skill, guidelines, catalog, Stage0, and complete intake inspection | 0 | the record names a proof method but does not select one stable truth-valued root; intake intentionally leaves the target null |
| authority, source, intake, toolchain, lockfile, probe, and mathlib `sha256sum` checks | 0 | exact current fingerprints are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0836/check_intake.py` | 1 | historical intake replay stops because integration advanced intake from `[ ]` to provisional `[_]`; historical evidence was preserved rather than weakened |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree agree; dependency worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0836/IntakeProbe.lean` | 0 | eight graph-coloring and degree APIs plus one tiny example elaborated; 924-byte stdout SHA-256 `c7e10628...a4e8`; no canonical target or proof body |
| bounded exact-topic search over repository-local and pinned-mathlib Lean | 1, expected no match | no match under the recorded patterns; empty stdout SHA-256 `e3b0c442...b855`; discovery only |
| prohibited Lean construct scan over the owned path | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse and scoped blocker assertions | 0 | identity, open blocked state, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact scope, and absent self-test agree |
| per-new-file `git diff --no-index --check /dev/null <artifact>` | 1 each, expected new-file difference | empty diagnostic output; no whitespace error |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test packet exists because the exact-statement deliverable failed |

The historical intake checker freezes intake-time workflow state. Master integration advanced the
intake item from `[ ]` to provisional `[_]`. Its failure is recorded rather than rewriting the
intake validator to manufacture a passing statement attempt.

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable independent
reviewers must then preserve and hash the complete authoritative source and computation suite;
select one exact truth-valued root or explicit conjunction without collapsing `THM-M-0833`; and
approve every incorporated map or graph, planarity, configuration, reducibility, discharging,
inventory, computation, foundation, trust, binder, hypothesis, conclusion, exception, and
degenerate-case choice.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash its elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a truthful blocked-attempt record, not completion of the statement node or any downstream
node. Lifecycle remains `planned`; the item remains `[ ]`; the root remains `[H5, M4, R4]`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, proof credit, or master acceptance is claimed.
