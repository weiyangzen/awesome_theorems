# Source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:6756-6761` supplies exactly the title `卢卡斯数`, attribution to
Edouard Lucas, year 1878, gloss `斐波那契数列的推广`, importance `中`, and status `已验证`. Git
history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no formula, bibliography,
edition, definition, ordered binders, hypotheses, conclusion, proof locator, correction history,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:25201-25226` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, equivalent forms, axioms,
machine status, and artifact links unresolved. The rev-5.6 manifest records rank 1544, baseline
`L0 / rework_required`, no legacy slot, `lifecycle_mode: planned`, and `theorem_complete: false`.
Its `已验证` field is explicitly untrusted.

## Literal clause crosswalk

| Repository component | Mathematical information fixed | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `卢卡斯数` | a recognizable recurrence-sequence name | a future classical `L` definition or source-selected Lucas-family encoding | object/family name, not a proposition |
| `斐波那契数列的推广` | suggests a second-order recurrence relationship | `LinearRecurrence`, a concrete function, and checked bridges to `Nat.fib` | family, parameters, formula, and claim role absent |
| Edouard Lucas / 1878 | historical attribution metadata | immutable source provenance | no cited work, edition, page, or theorem |
| `已验证` | untrusted inventory value | accepted source and kernel receipts would be required | no H or M completion credit |

There is no source node to map to a canonical statement. Consequently the statement, binders,
hypotheses, conclusion, Lean expression, minimal imports, expression fingerprint, transports, and
mutations remain intentionally unaccepted rather than guessed.

## Mathematical source boundary

No primary mathematical source is cited by the catalog, and this intake admits none. The year and
attribution are bibliographic leads only. Before H status can improve, a source audit must preserve
an edition, identify whether it defines classical Lucas numbers or a general `U/V` family, locate
the exact definition or theorem and proof, map every parameter and premise, audit corrections and
errata, and obtain independent review. General mathematical familiarity with the recurrence
`2, 1, 3, 4, 7, ...` does not select the repository root and is not H0 evidence.

## Pinned formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

| Declaration | Candidate role | Intake boundary |
|---|---|---|
| `LinearRecurrence` | generic order-and-coefficients recurrence structure | no Lucas parameters or initial values selected |
| `LinearRecurrence.IsSolution` | generic recurrence predicate | substrate, not an exact-topic target |
| `LinearRecurrence.mkSol` | constructs a sequence from initial values | no source-selected initialization or proposition |
| `LinearRecurrence.is_sol_mkSol` | proves the constructed sequence solves its recurrence | generic theorem only |
| `LinearRecurrence.eq_mk_of_is_sol_of_eq_init'` | generic uniqueness from initial values | possible future bridge, not the root |
| `LinearRecurrence.sol_eq_of_eq_init` | equality of solutions from their initial segment | possible future bridge, not the root |
| `Nat.fib` and `Nat.fib_add_two` | pinned Fibonacci definition and recurrence | neighboring sequence substrate only |

`IntakeProbe.lean` checks these signatures and candidate axiom reports. A bounded search of all
pinned package Lean sources found no declaration matching `Lucas number` or `Lucas sequence`; the
sole exact-phrase hit is prose saying that certain Lucas-sequence terms are examples of elliptic
divisibility sequences. This is bounded intake discovery, not the later exhaustive anchor audit or
a global absence theorem.

The legacy repo-local declaration
`AwesomeTheorems.Stage1.S1_M_018.lucasSequence (P Q : Int)` has initial values `0` and `1` and
recurrence `U(n+2) = P*U(n+1) - Q*U(n)`. It was built for `THM-M-0405` primitive-divisor work,
explicitly carries legacy/unaccepted status under rev-5.6, and is not the classical `L(0)=2`,
`L(1)=1` sequence. It receives no statement, wrapper, or proof credit here.

The provisional machine level is `M4`: generic substrate and a foreign legacy model exist, but no
usable exact formal artifact for the unidentified catalog root is credited.

## First downstream gate

Before ordinary statement work can pass, accountable reviewers must approve a target correction or
redirection, preserve one immutable mathematical source, select one exact truth-valued proposition,
map every definition, parameter, binder, hypothesis, conclusion, index convention, boundary case,
proof dependency and correction, and independently approve fidelity to `THM-M-0924`. Only then may
the statement phase choose minimal imports, serialize the elaborated expression and environment
fingerprint, compile checked alternate encodings, and run the required mutation classes.

