# Exact-statement gate: blocked

Item: `S56-M-0654-STATEMENT`  
Theorem: `THM-M-0654`  
Base revision: `8a4de324e430348fba945ccc31633dc565330377`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record gives only the title "Robinson consistency theorem", the year 1956, and the gloss
"compatibility of theories". The accepted intake identifies Abraham Robinson's *A Result on
Consistency and its Application to the Theory of Definition* as a leading discovery candidate, but
explicitly records that its exact result, definitions, assumptions, and errata have not been
inspected. It also leaves unresolved whether the adjacent `THM-M-0655` joint-consistency record is
an alias, a different formulation, or a distinct theorem.

The provisional family does not determine one proposition. An exact statement must decide literal
language intersection or explicit embeddings, a union-language construction, syntactic
consistency or semantic satisfiability, the role of completeness, and the precise common-sentence
consequence condition. It must also fix polarity and direction, binder order, equality, and the
behavior of empty or inconsistent component theories, an empty common language, and identical
languages. These choices alter the domains, hypotheses, and conclusion. Selecting a familiar
joint-consistency biconditional would therefore invent or substitute mathematics, contrary to the
rev-5.6 exact-statement gate.

Consequently there is no canonical human claim from which to derive minimal imports, an elaborated
expression hash, checked transports, or meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary mutations. Machine state remains `M4`; statement and theorem completion
are false. No theorem, axiom, placeholder, weakened special case, or abstract interface containing
the desired result was introduced.

## Pinned Lean boundary

`StatementProbe.lean` imports only `Mathlib.ModelTheory.Satisfiability` and checks the concrete
first-order substrate available in the pinned environment: languages, language homomorphisms,
transport of theories, theories as sets of sentences, semantic satisfiability, preservation under
injective language maps, and the consequence/non-satisfiability bridge. These ingredients show
that a later source-frozen encoding has a plausible formal surface. They neither select the
historical theorem nor determine its exact target and receive no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The canonical `.lake` artifacts were used read only;
no update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0654` | 0 | rank 699, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| repository search for the theorem ID, Chinese/English names, and source title | 0 | only underspecified metadata, intake material, and the adjacent target; no exact proposition |
| pinned-mathlib search for Robinson/joint consistency | 1 | no theorem-specific declaration (`rg` exit 1 means no match) |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0654/StatementProbe.lean` | 0 | elaborated all seven substrate checks; no theorem target was claimed |
| `python3 -m json.tool Stage1_Instances/THM-M-0654/statement-blocker.json` | 0 | blocker JSON is syntactically valid |
| `git diff --check -- Stage1_Instances/THM-M-0654` | 0 | no whitespace errors |

## Retry condition

An accountable source reviewer must preserve and hash an immutable primary-source edition, select
and transcribe the exact result with all incorporated definitions and assumptions, audit errata,
resolve its relation to `THM-M-0655`, and independently approve the row-by-row mapping. A later
statement worker can then encode that same claim, minimize pinned imports, serialize and hash the
elaborated expression, check alternate transports, and run all four required mutation classes.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
