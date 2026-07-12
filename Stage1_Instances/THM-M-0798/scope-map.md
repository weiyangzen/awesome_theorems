# Scope map

## Included topic boundary

- Jensen-style coherent sequences of closed unbounded subsets of ordinals.
- A source-selected indexing cardinal or ordinal and its limit points.
- The exact club, order-type, coherence, width, and thread conditions of that source.
- The source-selected assertion: existence in a specified universe/model, a consequence, or a
  consistency/independence theorem.
- Any hypotheses on regularity, singularity, successor formation, transitivity, or the ambient
  foundation that the selected proposition actually uses.

## Ambiguities to resolve at statement freeze

The repository record does not decide among these non-identical targets:

1. A successor-cardinal principle commonly written `square_kappa`, indexing limit ordinals below
   `kappa^+` with a club of order type at most `kappa` and a coherence condition.
2. A principle commonly written `square(kappa)`, whose indexing, order-type, and explicit
   no-thread conventions vary across sources.
3. Weak, indexed, finite-width, or global square principles.
4. An existence theorem inside the constructible universe, rather than the bare combinatorial
   principle as a proposition.
5. A theorem about a consequence, failure, consistency strength, or independence of square.

The statement phase must freeze ordered binders and decide whether a square sequence is a function
or family, what "club" and "limit point" mean, strict versus non-strict order-type bounds, sequence
width, whether coherence is equality or inclusion, and whether absence of a thread is stated or
proved. It must also settle small-cardinal and singular-cardinal boundary behavior.

## Explicit exclusions

- The diamond principle, club guessing, stationary reflection, approachability, or a morass as a
  substitute.
- Replacing the requested principle with a definition followed by a tautological projection.
- Treating all notations containing `square` as checked equivalent without Lean transports.
- Treating Jensen's attribution and the year 1972 as an exact bibliographic theorem anchor.
- Treating the repository label `已验证` as evidence of human proof or kernel closure.

No canonical Lean target is frozen at intake because the source record does not identify a unique
proposition.
