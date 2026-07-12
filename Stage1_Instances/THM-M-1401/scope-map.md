# Scope map

## Received scope

The mathematical catalog fixes only the Chinese title `符号动力学`, the gloss "symbolic
representation of dynamical systems," an attribution to many mathematicians in the twentieth
century, and the untrusted status `已验证`. It provides no primary source, theorem locator,
definitions, hypotheses, or proposition-level conclusion.

## Candidate mathematical boundary

An eventual exact target may concern a symbolic representation only if a reviewed source fixes all
of the following:

- a dynamical system: state space, topology or measurable structure, map or time action, and the
  invariant subset being represented;
- an alphabet and a one-sided or two-sided full shift or source-defined subshift;
- a partition, cover, Markov family, or other construction that assigns symbols to orbit segments;
- the exact coding map and whether it is total, continuous or measurable, injective, surjective,
  finite-to-one, or defined only away from a boundary or null set;
- the exact intertwining equation with the shift and whether the conclusion is semiconjugacy,
  conjugacy, factor, embedding, realization, or finite-type presentation;
- any compactness, continuity, expansivity, hyperbolicity, generating-partition, Markov, or
  regularity assumptions needed by that conclusion.

These bullets are a scope inventory, not a canonical claim. No one family is credited at intake.

## Ambiguities to resolve

1. Whether the target is a general definition/theory, a Morse-Hedlund sequence theorem, a coding
   theorem for a specified map, or a Markov-partition consequence for a hyperbolic system.
2. Whether the time index is `Nat`, `Int`, or a continuous action sampled by a return map.
3. Whether the symbolic system is the full shift, a subshift, a subshift of finite type, or a sofic
   system, and which topology, sigma-algebra, or measure it carries.
4. Whether the coding goes from the original system to the symbolic system or conversely, and
   whether it is a factor map, embedding, conjugacy, or weaker orbit-labeling function.
5. How points on partition boundaries, nonunique names, exceptional/null sets, empty cells, and
   non-generating partitions are treated.
6. Whether periodic-orbit, entropy, language-complexity, or realization consequences are part of
   the root or separate corollaries.

## Explicit exclusions

- The stream tail/shift definition or its elementary equations as the target. `THM-M-1402`
  separately owns the shift-map catalog item.
- Topological entropy, measure entropy, the Kolmogorov-Sinai theorem, Bernoulli shifts, and
  Ornstein isomorphism; these have their own nearby target IDs.
- A Markov partition theorem, Smale horseshoe theorem, or hyperbolic-system theorem substituted for
  a source-unspecified symbolic-dynamics root.
- A tautological structure containing a `Semiconj`, `Conj`, or desired representation field.
- A coding established only for one convenient special case when the selected source has broader
  domains, or a broad abstract existence claim when the source proves a narrower coding.
- The catalog label `已验证`, a topic-level citation, or a passing API check as source or proof
  evidence.

## Formal boundary

No canonical Lean expression is frozen at intake. Pinned mathlib contains generic streams,
function semiconjugacy, periodic-point transport, and topological-entropy infrastructure, but these
ingredients do not determine or prove a symbolic-dynamics theorem. Exact imports, binders,
expression fingerprint, alternate transports, and structural mutations belong to the dependent
statement phase after source identity is resolved.
