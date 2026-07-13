# Scope map

## Preserved theorem family

The intake preserves the computability-theoretic parameter theorem. Informally, program indices
can be effectively specialized by fixing some inputs, producing an index for the residual partial
computable function. The repository fixes the title `s-m-n定理`, Stephen Kleene, 1943, and the
gloss `参数定理`; it does not supply the indexing model, arities, formula, source locator, or proof.

The Spring 2024 Stanford Encyclopedia of Philosophy archive gives a precise standard candidate
family in Section 3.1, Theorem 3.1: for all natural `n,m`, there is a primitive-recursive
`s_n^m(i,x_0,...,x_(m-1))` such that

```text
phi^n_(s_n^m(i,x_0,...,x_(m-1)))(y_0,...,y_(n-1))
  ~= phi^(n+m)_i(x_0,...,x_(m-1),y_0,...,y_(n-1)).
```

This inspected secondary statement narrows the family but is not an accepted primary source or an
adopted canonical claim.

## Decisions required at statement freeze

An approved source review must freeze all of the following before any formal candidate can become
the canonical statement:

1. The primary source edition, theorem/page locator, incorporated definitions, proof boundary,
   corrections or errata, and independent review. The catalog's 1943 attribution is untrusted.
2. The acceptable numbering or program formalism: natural indices, inductive codes, or another
   effective enumeration, including universality and decoding behavior.
3. Whether `n,m` are arbitrary arities, positive arities, or encoded into a unary presentation, and
   how zero-arity cases and tuples are represented.
4. The exact order and dependency of the index, fixed-parameter, and residual-input binders.
5. Whether the index transformer must be primitive recursive, total computable, or another precise
   effectiveness class. This distinction is visible between the standard statement and the
   proposition exposed by the pinned mathlib candidate.
6. Whether semantic agreement is equality of partial values, extensional equality of partial
   functions, graph equality, or another checked relation.
7. The natural-index/`Code`, tuple/pairing, arity, evaluator, and effectiveness transports required
   to connect any packed unary Lean encoding to the adopted human statement.
8. The exact foundation profile, hypotheses, conclusion, malformed-code policy, and every excluded
   degenerate case.

## Neighbor and duplicate boundaries

- `THM-M-0742` and `THM-M-0743` separately own recursion and fixed-point theorem families. The
  s-m-n theorem may be their dependency, but their root statements and evidence are not this root.
- `THM-M-0741` separately owns the halting problem; an undecidability application cannot replace
  parameterization.
- `THM-C-0005` repeats the s-m-n title and gives the fuller index-plus-parameter gloss, but it is
  outside the closed Stage1 target set. It is duplicate/ownership evidence only, not a second slot
  or a source of shared proof credit.

## Explicit exclusions

The target is not merely the existence of a universal evaluator, a pairing function, a particular
specialized program, or a non-effective transformation. It is not syntactic equality of program
indices, the recursion theorem, a fixed-point theorem, or the halting theorem. The catalog's
untrusted `已验证` label, an unchecked human equivalence, or the discovery probe cannot provide
proof credit.

## Formal boundary

`IntakeProbe.lean` checks the exact type and axiom report of the pinned `Nat.Partrec.Code.smn`
candidate and its primitive-recursive witness fact. It declares no target theorem or wrapper. The
candidate fixes `Code`, one natural parameter, one residual natural input, `Nat.pair`, and
pointwise equality of partial evaluations. Its theorem conclusion exposes `Computable₂` rather
than the primitive-recursive transformer required by the inspected standard formulation. No exact
statement identity, alternate encoding, transport, mutation test, or proof-body credit is claimed.

## Phase boundary

This intake freezes a planned dossier and all-open task DAG only. Primary-source acceptance,
canonical statement elaboration, candidate audit, obligation and graph freezes, proof,
composition, trust closure, readable reconstruction, hermetic replay, independent verification,
and master acceptance remain downstream.
