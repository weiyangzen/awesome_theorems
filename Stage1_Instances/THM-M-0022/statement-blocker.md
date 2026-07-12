# Exact-statement gate: blocked

Item: `S56-M-0022-STATEMENT`

Theorem: `THM-M-0022`

Base revision: `5ae439adae290d44dcf08cc6439c5fb64154fe47` (tree
`51717feef6efc7076e60ee31e7a1ca0a246fec42`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0022-INTAKE` is provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this ordered statement
attempt while concurrency is enabled, but master closure remains dependency ordered. The intake
receipt is unsigned, non-content-addressed, declares `accepted: false`, and has no accepted receipt
ID. Its replay also stops at a stale hash for the generated blueprint because later integration
batches changed shared authority bytes. This phase records rather than rewrites that historical
intake evidence.

Independently and decisively, the received repository record does not identify one proposition.
It gives only the title "Hecke character theorem," attributes it to Erich Hecke in 1917, and says
"about a functional equation for L-functions." Stage0 explicitly leaves precise definitions and
premises, the proof route, equivalent statements, axioms, machine status, and artifact links open.
The `已验证` label is untrusted metadata under rev-5.6.

The intake's historical lead is Hecke's 1918 paper *Eine neue Art von Zetafunktionen und ihre
Beziehungen zur Verteilung der Primzahlen*. The inspected passage in section 4, journal pages
368-370, around displayed equation (21), identifies the intended theorem family, but it is not an
accepted exact crosswalk. Exact symbols and all incorporated definitions, the character and
properness hypotheses, conductor/discriminant and gamma normalization, translation, proof
boundary, corrections, and independent review remain open. The paper's Basel and received dates
are February 1918, conflicting with the catalog's 1917 attribution; a 1920 continuation and a
conflicting legacy DOI also remain to be reconciled.

The missing choices change the theorem rather than merely its notation:

- the number field and ideal/ray-class or idele-class definition of a Hecke character;
- finite-order, unitary, algebraic, or general quasicharacters, plus primitivity, conductor,
  infinity type, and ramification data;
- the Euler product or series, analytic-continuation claim, archimedean gamma factors, conductor
  power, and completed L-function normalization;
- the dual or conjugate character, reflection center, epsilon/root number, equality domain, and
  treatment of imprimitive and trivial/polar cases; and
- every ordered binder, universe, typeclass context, hypothesis, conclusion, and boundary case.

There is also an unresolved identity collision. `THM-M-0426` separately records "the functional
equation for Hecke characters" with the gloss "the functional equation of Hecke L-functions," the
same author, year, importance, and untrusted status. No accepted distinction, alias/deduplication
relation, or canonical-root ownership decision exists. Reusing its legacy
`AwesomeTheorems.Stage1.S1_M_080` module would silently substitute foreign scope. That module
supplies the character type, completed function, conductor factor, root number, center, dual, and
primitivity predicate as abstract fields and then asks those inputs to satisfy an equation. It is
an interface boundary, not a construction of Hecke characters or a terminal theorem.

Choosing that abstract interface, a generic `WeakFEPair` equation, or the primitive Dirichlet
character equation over the rational field would therefore invent, broaden, or specialize the
received claim. No source-faithful target can yet be elaborated. Consequently there is no honest
minimal-import claim, serialized elaborated expression, target-environment fingerprint, credited
transport, or removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutation
suite. Those mutations are undefined, not passed. The vector remains `[H1, M4, R3]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned toolchain. Its four direct imports
expose generic weak/strong functional-equation machinery, the primitive Dirichlet-character
special case, and number-field adele/product-formula infrastructure. All nine checks pass. The
probe defines no Hecke character, completed Hecke L-function, source-normalized equation, canonical
target, checked transport, or proof body. Its imports therefore cannot be called minimal for an
absent target and receive no statement or proof credit.

The foreign `S1_M_080.lean` module also elaborates, confirming only that its documented abstract
boundary is syntactically valid. A bounded exact-topic search of pinned mathlib found no concrete
`HeckeCharacter`, arbitrary-number-field Hecke L-function, or idele-class-character declaration
under the recorded terms. These are discovery observations, not the later exhaustive anchor audit
or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or other
dependency mutation was run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0022` | 0 | rank 1069; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base identifiers appear above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree and package-status checks | 0 | revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0022/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; stdout was 1,514 bytes with SHA-256 `2f44f648c4bf45d59e2b1612aa03da64e31f25cdf15acf645d7eee3dfb8a47d2`; no canonical target declared |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_080.lean` | 0 | the foreign abstract interface module elaborated; no target identity or statement credit |
| exact-topic search in pinned mathlib | 1 | expected no-match result under the recorded Hecke-character, Hecke-L-function, idele-class, and Grossencharacter terms |
| `python3 -B Stage1_Instances/THM-M-0022/check_intake.py` | 1 | historical intake replay stops at stale receipt input hash `Docs/Stage1_Blueprint_rev-5.6.md`; it also freezes an intake-only artifact inventory |
| JSON parse and scoped invariants for `statement-blocker.json` | 0 | identity, open state, null target/imports, unchanged vector, four undefined mutations, false completion flags, and absent self-test agree |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped whitespace checks for both blocker artifacts | 0 diagnostics | no whitespace errors; each no-index check exits 1 only because the file is new |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must revalidate and master-accept the intake before accepting a future
statement transition. Accountable reviewers must lawfully preserve and hash a complete primary or
authoritative source edition, select and independently approve one exact proposition, transcribe
all incorporated definitions, ordered binders, hypotheses, completion and normalization choices,
conclusion, proof boundary, translation, date, correction and errata status, and issue an explicit
`THM-M-0022` versus `THM-M-0426` identity and canonical-root ownership decision.

A later statement worker can then encode precisely that approved claim with concrete Lean objects,
minimize pinned imports, serialize and hash the elaborated expression and environment, compile
every credited transport, and run all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt change
is proposed. Because the assigned deliverable did not pass, no `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, or master acceptance is claimed.
