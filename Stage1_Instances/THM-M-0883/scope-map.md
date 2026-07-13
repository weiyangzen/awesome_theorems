# Scope map

## Preserved theorem family

The intake preserves the 1988 Lubotzky-Phillips-Sarnak construction of explicit Ramanujan graphs.
It does not silently reduce the target to the definition of a Ramanujan graph, generic expander
existence, one numerical example, or the spectral clause of the publisher abstract alone. The
abstract also advertises a girth conclusion, so source review must decide whether the catalog's
word `construction` denotes the paper's complete result bundle or a specific theorem within it.

The 2017 author survey describes the first LPS examples as explicit infinite families for
`k = q + 1`, with `q` prime. That is candidate scope, not a frozen root. The exact 1988 theorem
text and its incorporated definitions remain unavailable in this intake.

## Decisions required at statement freeze

1. Admit and independently review an immutable 1988 edition, select exact theorem and definition
   locators, map the proof boundary and corrections, and determine whether spectral, girth, and
   explicit-construction clauses form one root or separate results.
2. Freeze every number-theoretic parameter, primality and congruence condition, quadratic-residue
   relation, distinctness condition, and the order and dependency of the prime binders. The later
   survey's `q` used for the degree must not be conflated with source-specific auxiliary primes.
3. Fix the finite graph model: simple versus possible loops or multiple edges, connectedness,
   undirectedness, vertex type, equality of constructed graphs, and family indexing.
4. Fix the algebraic carrier and construction data, including the exact `PSL(2, F)` or
   `PGL(2, F)` branch, finite field, quotient, Cayley generating set, inverse closure, and proofs
   that the data yield the claimed graph.
5. Fix the degree and cardinality formula, one graph versus an infinite pairwise-nonisomorphic
   family, bipartite versus nonbipartite branches, and every exceptional small parameter.
6. Define the adjacency matrix or operator, coefficient field, eigenvalue enumeration and
   multiplicity, which `+/- k` eigenvalues are trivial, and the exact non-strict Ramanujan bound.
7. Define `explicit`: a closed algebraic formula, effective generator procedure, computable family,
   or a complexity claim. No stronger constructive or algorithmic meaning may be invented.
8. If girth is in scope, freeze the asymptotic quantifiers, logarithm base, family limit, constant
   `4/3`, rounding/additive terms, and whether the statement is a limit, liminf, or eventual bound.
9. Freeze ordered binders, universes, typeclasses, hypotheses, conclusion, minimal imports,
   checked transports, foundation/TCB/computation profiles, and rev-5.6 statement mutations.

## Degenerate and boundary cases

Source review must resolve the smallest allowed primes; equal or excluded prime parameters;
congruences modulo four; quadratic residue and nonresidue branches; empty, singleton, looped,
multiple-edge, or disconnected graphs; degenerate or duplicate generators; `PSL` versus `PGL`;
bipartite and nonbipartite trivial spectra; repeated eigenvalues; equality at
`2 * sqrt (k - 1)`; one graph versus an unbounded family; and the exact start and limit of any
girth asymptotic. No case is excluded before the proposition is frozen.

## Excluded substitutions and neighbor boundaries

- `THM-M-0881` concerns expander graphs generally; expansion alone is weaker than the LPS
  construction and Ramanujan spectrum.
- `THM-M-0882` is the separate Margulis construction; provenance and construction data cannot be
  shared without a checked statement transport.
- `THM-M-0884` is the general Ramanujan-graph topic, not the LPS construction theorem.
- `THM-M-0885` is Morgenstern's later construction/existence result with a different parameter
  family, and `THM-M-0886` is the later Marcus-Spielman-Srivastava existence result.
- A generic Cayley graph, regular graph, Hermitian adjacency matrix, projective linear group,
  Legendre symbol, Ramanujan predicate, or algebraic recipe does not establish the target.
- A structure or premise carrying the desired graph, spectral bound, girth, or explicitness as
  assumed data cannot count as a proof.
- One computed graph, numerical eigenspectrum, randomized experiment, unchecked certificate, the
  catalog label `verified`, or the publisher abstract cannot supply human or kernel proof credit.

## Formal boundary

Pinned mathlib has useful components but no source-selected LPS graph or theorem. Its
`SimpleGraph` API fixes simple graphs, while the source's graph convention has not been admitted.
Its `PSL` and `PGL` types, Legendre symbol, finite-graph regularity, adjacency-matrix spectrum, and
real square root do not build the source Cayley graphs or prove their spectrum and girth. The
statement phase must first freeze the source-identical claim, then elaborate and fingerprint it.
