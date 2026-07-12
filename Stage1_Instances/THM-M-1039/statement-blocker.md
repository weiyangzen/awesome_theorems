# Exact-statement gate: blocked

Item: `S56-M-1039-STATEMENT`  
Theorem: `THM-M-1039`  
Base revision: `4633bb122ff00838c72bebefcbb3490430c9e2f3`

## Decision

The exact Lean 4 target cannot yet be truthfully elaborated. The only source
record says "SDE solutions have the Markov property" and attributes the family
to Itô (1951). It gives no work, theorem, page, formula, or assumptions. The
intake accordingly leaves the coefficient class, uniqueness notion, solution
concept, filtration convention, state/noise dimensions, and exact Markov
identity open. Its Oksendal and Karatzas-Shreve references are discovery
candidates without an edition-specific theorem/page crosswalk.

Those choices distinguish materially different propositions. In particular,
pathwise uniqueness and uniqueness in law support different restart arguments;
weak solutions need not make every arbitrary selection Markov; a
time-inhomogeneous SDE needs a two-parameter transition family or time adjoined
to the state; and a deterministic-time conditional-expectation identity is not
silently interchangeable with the strong Markov property at stopping times.
Selecting one textbook variant would therefore substitute a nearby theorem for
the unidentified source claim, contrary to the rev-5.6 exact-statement gate.

## Pinned Lean boundary

The environment is Lean `4.29.0` with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. `StatementProbe.lean` uses two
imports to elaborate the concrete substrate currently available for a future
statement: filtrations, Markov kernels, regular conditional distributions, and
conditional expectations. A scoped source search found no declaration for an
SDE, Brownian motion, stochastic integral, or SDE Markov theorem in this pinned
mathlib tree.

The historical discovery module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_232.lean` also elaborates, but
it is not an exact target. Its `SDEMarkovData` stores the SDE integral equation,
coefficient assumptions, strong existence/uniqueness, independent noise
increments, and transition-semigroup identification as unconstrained `Prop`
fields. Thus it does not define an SDE or Brownian driver and delegates the
essential source premises to callers. Moreover, its conclusion simultaneously
requires a conditional law given `X_s`, a filtration-relative indicator
identity, and a bounded-test identity, although the source metadata selects
none of these or their conjunction. Reusing that shape would broaden and
substitute the source claim.

## Validation record

Commands ran in this worker clone using the existing pinned Lake artifacts. No
dependency update, clone, fetch, or build was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1039` | 0 | rank 232; planned; L0/rework-required; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1039/StatementProbe.lean` | 0 | the five substrate declarations elaborated with the two pinned imports |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_232.lean` | 0 | historical abstract boundary elaborated; this does not prove or identify an exact target |
| `rg -n -i '\\b(SDE|Brownian|stochastic integral|Ito|Itô|Markov property|strong Markov)\\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching declaration or source occurrence in pinned mathlib |
| `git diff --check -- Stage1_Instances/THM-M-1039` | 0 | no whitespace errors |

## Gate result and retry condition

First failed gate: exact source-statement identity. Without it, there is no
canonical expression to hash and no meaningful removed-hypothesis, changed-
domain, binder-scope, or boundary mutation suite. Machine debt remains `M4`.

Retry only after an authoritative stable source supplies an exact theorem and
all definitions needed to freeze the equation, coefficient regularity and
growth, solution and uniqueness notions, filtration, quantifier order, and
one precise Markov conclusion. The statement phase can then encode concrete
objects, minimize imports, serialize the elaborated expression/environment,
and run all four mutation classes.

This artifact does not complete the statement node, accept a receipt, or claim
theorem completion. No `.stage1-worker-selftest.json` is emitted because the
assigned deliverable is not genuinely self-tested.
