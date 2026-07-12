# Scope map

## Included result family

- The propositional pigeonhole-principle contradiction, conventionally with more pigeons than
  holes and usually represented as a CNF family.
- Resolution refutations under the exact rule and derivation conventions selected from the primary
  source.
- A lower bound on a precisely defined resolution-proof length or size, quantified over the family
  parameter and stated with explicit constants or an explicit asymptotic predicate.
- Definitions and combinatorial lemmas needed to relate clauses in a refutation to restrictions or
  partial assignments used by the lower-bound argument.

## Decisions required at statement freeze

The repository record leaves all of the following open:

1. Whether the family has `n + 1` pigeons and `n` holes or general parameters `m > n`.
2. Whether the clauses include both "every pigeon occupies a hole" and only pairwise collision
   clauses, and the precise variable indexing.
3. The resolution calculus: binary resolution alone or additional weakening, deletion,
   factoring, tautology, and repeated-clause conventions.
4. DAG-like versus tree-like derivations and whether the measure counts derived clauses, proof
   lines, literal occurrences, symbols, or another representation-dependent size.
5. The exact lower-bound function, constants, threshold for `n`, and the interpretation of any
   asymptotic notation in a source statement.

These choices can change the formal proposition. They must come from an immutable source passage,
not from a convenient Lean encoding.

## Explicit exclusions

- The ordinary combinatorial pigeonhole principle as a substitute for its resolution proof-size
  lower bound.
- Lower bounds for bounded-depth Frege, polynomial calculus, cutting planes, extended resolution,
  or a tree-resolution-only result unless the source explicitly selects that system.
- The fact that the pigeonhole CNF is unsatisfiable; unsatisfiability is necessary context but is
  strictly weaker than an exponential resolution lower bound.
- An assumed predicate called `ResolutionProof` followed by a tautological theorem about it.
- A finite computation for selected values of `n` as evidence for a uniform lower bound.
- The repository label `已验证` as evidence of either a human-source audit or a machine proof.

No canonical Lean target is frozen during intake.
