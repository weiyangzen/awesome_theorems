# Scope map

## Included claim

- A fixed finite alphabet with at least two symbols and languages represented as sets of finite
  words (or an explicitly checked equivalent encoding).
- A concrete notion of nondeterministic polynomial-time decidability defining `NP`.
- Polynomial-time many-one reduction as the completeness reduction notion.
- Existence of a language `L` that is both in `NP` and hard for every language in `NP` under that
  reduction.
- A Boolean satisfiability language as the intended existential witness, after its syntax, semantic
  truth relation, and binary encoding have been fixed.

## Statement-phase decisions

The formal statement must freeze the alphabet and word representation; deterministic and
nondeterministic machine or verifier model; polynomial bounds and cost model; encoding of machines,
formulas, assignments, and tuples; reduction composition conventions; and whether `NP` is defined
by nondeterministic machines or polynomially bounded certificates. Any equivalence used between
models or encodings must be a checked transport rather than prose.

Degenerate cases must be settled explicitly. In particular, the alphabet cannot be empty or unary
without an encoding theorem; malformed formula encodings need a defined accept/reject convention;
constant and zero-length inputs must be covered by the time model; and a reduction must be total on
all input words, not merely on well-formed instances.

## Explicit exclusions

- `P = NP`, `P != NP`, or any separation between complexity classes.
- The assertion that every problem in `NP` is NP-complete.
- NP-hardness alone without membership in `NP`, or membership alone without universal hardness.
- Completeness under an unspecified, oracle, Turing, randomized, or nonuniform reduction in place
  of polynomial-time many-one reducibility.
- A finite toy universe in which completeness is obtained by enumeration.
- An abstract structure that assumes an NP-complete language as a field.
- The stronger Cook-Levin target "SAT is NP-complete" as a substitute for this existential target;
  it may later be a bridge supplying the witness, with its full obligations retained.

The exact Lean statement remains open until these representations elaborate against pinned APIs.
