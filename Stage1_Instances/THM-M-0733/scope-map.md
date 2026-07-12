# Scope map

## Included topic boundary

- Ensembles of Boolean functions indexed by input length and the selected circuit class.
- A source-exact property of truth tables, with explicit largeness/density and constructivity bounds.
- Usefulness against a named circuit class, with its quantifier order and asymptotic size bound.
- The precise pseudorandom-function or one-way-function hypothesis used by the barrier result.
- The conditional conclusion connecting the cryptographic hypothesis to the absence of a property
  satisfying the selected naturalness and usefulness conditions.

## Ambiguities to resolve at statement freeze

1. **Naturalness parameters:** largeness may use different density thresholds, and constructivity
   depends on whether the input is a truth table and on the allowed time bound.
2. **Usefulness target:** the circuit family, circuit-size function, and whether usefulness is
   eventual or infinitely often materially alter the claim.
3. **Cryptographic premise:** existence and hardness of pseudorandom functions, strong
   pseudorandom generators, and one-way functions are not interchangeable without bridges.
4. **Barrier conclusion:** a conditional impossibility for a defined proof property is not an
   unconditional prohibition on every possible lower-bound proof.
5. **Published version:** the 1994 conference account and later journal version must not be treated
   as identical without inspecting theorem numbering, definitions, and revisions.

The statement phase must select and independently inspect an immutable primary source, then freeze
all asymptotic quantifiers, encodings, size functions, density bounds, algorithms, advantages, and
security assumptions. It must explicitly address small input lengths and vacuous parameter choices.

## Explicit exclusions

- Translating the gloss as "no circuit lower bounds can be proved."
- Omitting the cryptographic assumption or turning a conditional barrier into an absolute one.
- Replacing the barrier theorem by definitions of largeness, constructivity, or usefulness alone.
- Substituting a survey formulation without crosswalking it to a primary-source theorem.
- Encoding the desired incompatibility as a hypothesis and merely projecting it.
- Treating the inventory label `已验证` as source or machine-proof evidence.

No canonical Lean target is frozen at intake because the repository record does not provide enough
information to choose among the materially different formulations.

