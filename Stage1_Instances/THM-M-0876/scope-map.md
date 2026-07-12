# Scope map

## Preserved catalog scope

The intake preserves the graph-isomorphism computational-complexity topic and literal phrase
`图同构在NP与P之间的位置`. It does not turn "position" or "between" into a set-membership theorem.
The status `部分解决` and scheduling lane `known_partial_branch_deepening` are metadata, not evidence
that a particular mathematical or machine-checked branch was selected.

## Candidate roots not credited

The catalog wording is compatible with several inequivalent propositions or research questions:

1. The decision language for finite graph isomorphism belongs to NP.
2. The graph-isomorphism decision problem belongs to P, which would be an open root rather than a
   proved theorem target unless an accepted source changes that status.
3. Graph isomorphism is NP-intermediate, necessarily with explicit complexity assumptions and a
   precise meaning of "intermediate."
4. A deterministic algorithm decides graph isomorphism in quasipolynomial time.
5. A bundle separates known upper bounds, conditional hardness results, and the remaining P-status
   question into independently sourced branches.

None is selected at intake. In particular, the literal phrase does not license `GI ∈ NP \ P`.

## Proposition-changing decisions

Before statement elaboration, an approved source decision must freeze:

- a primary or authoritative source edition, exact theorem or problem locator, incorporated
  definitions, correction and errata disposition, proof boundary, and independent review;
- finite simple undirected graphs versus directed, colored, labeled, multigraph, or relational
  structures, including whether the two vertex types are the same;
- a canonical encoding of pairs of finite graphs as bit strings or another fixed alphabet, plus
  malformed-input behavior and the relationship between encoding length and vertex count;
- the decision predicate, likely existence of an adjacency-preserving vertex equivalence, and a
  checked correspondence with `Nonempty (G ≃g H)` for the chosen graph representation;
- deterministic and nondeterministic machine models, cost measure, worst-case quantification, and
  uniformity assumptions;
- exact definitions of polynomial and quasipolynomial time and the complexity class NP;
- reduction type when hardness, completeness, or conditional consequences are in scope;
- whether the conclusion is a known membership/upper-bound theorem, an open classification
  question, a conditional separation, or a source-reviewed branch ledger; and
- binder order, constants, asymptotic thresholds, strict inequalities, empty inputs, small graphs,
  unequal vertex counts, and all other degenerate cases.

Each choice can change the proposition and therefore cannot be inferred from the topic label.

## Neighbor target boundaries

- `THM-M-0873` separately represents the generic graph-isomorphism problem with the catalog's
  quasipolynomial-time status.
- `THM-M-0874` separately represents the Babai quasipolynomial algorithm.
- `THM-M-0875` separately represents the Weisfeiler-Lehman heuristic/refinement topic.
- `THM-M-1567` is a second catalog record for the generic graph-isomorphism problem.

Statements or proof credit from these targets cannot silently replace `THM-M-0876`.

## Explicit exclusions

- `GI ∈ NP`, a quasipolynomial upper bound, or a special graph-class algorithm presented as the
  full target without a checked source crosswalk.
- An unconditional claim that graph isomorphism is outside P or is NP-intermediate.
- An assertion that failure to locate an NP-completeness proof proves non-NP-completeness.
- A predicate or structure field that assumes the desired algorithm or complexity bound.
- Runtime experiments, benchmark data, executable heuristics, or unchecked certificates.
- The catalog label `部分解决`, the scheduling lane, or an API probe used as proof evidence.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean` checks `SimpleGraph.Iso`, formal
languages, and computable many-one and one-one reductions. A bounded pinned/repo-local search found
no graph-isomorphism complexity theorem or standard P, NP, or quasipolynomial-time framework. The
probe establishes adjacent interface feasibility only; it is not a complete anchor audit, an
encoding, an algorithm, a complexity proof, or evidence for the received target.
