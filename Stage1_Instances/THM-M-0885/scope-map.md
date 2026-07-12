# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-0885`, the name `Morgenstern theorem`, Moshe Morgenstern,
the year 1994, the subject `Ramanujan graph existence`, and an untrusted `verified` label. Intake
preserves that graph-theoretic subject boundary. It does not silently import a complete theorem
from the matching article title.

## Candidate source family, not a frozen claim

Bibliographic metadata identifies Morgenstern's 1994 article *Existence and Explicit Constructions
of q + 1 Regular Ramanujan Graphs for Every Prime Power q*. This suggests a degree parameter of the
form `q + 1`, with `q` a prime power, and an explicit-construction conclusion. None of those
quantifiers or conventions occurs in the repository record, and the article's exact theorem text,
definitions, hypotheses, and cases have not yet been source-audited. They remain candidate scope.

## Proposition-changing decisions

An approved source statement must freeze all of the following before Lean elaboration:

- the quantifier over prime powers, including whether `q` is a number equipped with a witness, a
  finite field cardinality, and whether all prime powers or only specified parity cases occur;
- whether the conclusion provides one graph, infinitely many pairwise nonisomorphic graphs, an
  indexed family, an effective construction, or a polynomial-time construction;
- the vertex model and finiteness, simplicity, undirectedness, loop and multiple-edge policy,
  connectedness, bipartiteness, and size or congruence restrictions;
- the exact meaning of `(q + 1)`-regular and every nondegeneracy condition on the vertex set;
- the adjacency operator or matrix, coefficient field, eigenvalue multiplicity convention, and
  whether the spectrum is indexed or treated as a multiset;
- the trivial eigenvalues removed in the Ramanujan bound: always the degree, and also its negative
  in the bipartite case, with the exact bound `2 * sqrt q` or an equivalent form;
- the relationship between the constructed algebraic or Cayley/quotient object and the finite
  graph, including any choices of auxiliary polynomial, place, group, generator set, or level;
- exceptional small prime powers, disconnected or empty graphs, zero-dimensional eigenspaces,
  repeated eigenvalues, and any one-family versus infinitely-many boundary;
- the ordered binders, hypotheses, conclusion bundle, constructive content, and all equivalences
  credited to the canonical target.

## Explicit exclusions and neighbor boundaries

- `THM-M-0883` (Lubotzky-Phillips-Sarnak construction) is a separate construction target; its
  degree restrictions and evidence cannot be substituted or shared without checked transport.
- `THM-M-0884` (Ramanujan graphs) is a general object/topic target, not this construction theorem.
- `THM-M-0886` (Marcus-Spielman-Srivastava theorem) concerns existence of bipartite Ramanujan
  graphs through a different result family and is not a replacement for Morgenstern's theorem.
- Existence of arbitrary regular graphs, generic adjacency-matrix spectral theory, a spectral-gap
  inequality assumed as a hypothesis, or a structure carrying its own desired proof is insufficient.
- A single small example, a random graph experiment, computed eigenvalues, or a prose construction
  recipe cannot replace the source's quantified theorem.
- The catalog's `verified` label and the matching title supply no human-proof or Lean proof credit.

No canonical Lean expression, excluded-case list, alternate encoding, discovery protocol, or
obligation registry is frozen at intake.
