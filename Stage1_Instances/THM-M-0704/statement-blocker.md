# Statement gate blocker

Item: `S56-M-0704-STATEMENT`

Base revision: `f4c286c4ebc4a8b1a5d0a746afd6fba9849e4c7c`.

## Decision

The rev-5.6 statement phase is blocked and is not self-tested as complete. The repository source
identifies the topic "lambda calculus" and gives only the gloss "functional computation model".
That text is not a proposition and supplies no ordered binders, hypotheses, conclusion, calculus,
syntax representation, equality convention, or reduction semantics. Consequently there is no exact
human claim that can be mapped to a canonical Lean `Prop`, and no truthful elaborated-expression
hash or statement mutation suite can be produced.

The adjacent `THM-M-0705` separately names the Church-Rosser theorem and states confluence. The
Stage0 catalogue also separately names lambda-calculus/Turing-machine equivalence as `THM-C-0021`.
Using either result here would substitute a different repository target. Encoding a term datatype
or checking Lean kernel expression constructors would supply a definition/API probe rather than the
required theorem. None of those broadenings or substitutions is made.

This is the first failed gate in section 5.1 of the rev-5.6 blueprint: an exact mathematical claim
must exist before Lean elaboration, canonical serialization, checked transports, and semantic
mutation tests are meaningful. The existing `IntakeProbe.lean` remains intake-only evidence and is
not credited as statement elaboration.

## Retry condition

An authorized source-selection decision must provide one immutable, pinpointed proposition and
freeze at least:

- typed or untyped lambda calculus;
- raw named syntax, de Bruijn syntax, or an alpha-quotiented representation;
- the exact substitution and reduction/conversion conventions;
- all quantified objects, hypotheses, conclusion, and boundary cases;
- a source edition, theorem/page or exact passage, and premise-to-binder crosswalk.

Only then can this node add a minimal-import Lean target, preserve its elaborated expression and
environment fingerprint, and run the required removed-hypothesis, changed-domain, binder-scope,
and boundary-case mutations. Source selection must not silently choose confluence or computational
model equivalence, because those are distinct catalogue items.

## Scoped validation on 2026-07-12

No `.lake` update, build, fetch, or clone was run. The canonical pinned artifacts were used
read-only.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0704` | exit 0; rank 745, lifecycle planned, theorem_complete false |
| `rg -n -C 10 'THM-M-0704|lambda calculus' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | exit 0; the target has only a topic gloss, while confluence and Turing-machine equivalence are separately catalogued |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0704/IntakeProbe.lean)` | exit 0; only `Lean.Expr.bvar`, `Lean.Expr.lam`, and `Lean.Expr.app` API checks elaborated |

The truthful phase result is `blocked`, with root vector unchanged at `[H3, M4, R4]`. There is no
canonical statement, no claimed statement receipt, no audit completion, and no theorem completion.
Because the assigned phase did not pass, no `.stage1-worker-selftest.json` is emitted.
