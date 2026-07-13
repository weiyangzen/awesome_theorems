# THM-M-1585 scope map

## Preserved repository scope

The intake preserves target `THM-M-1585`, the title `编码理论` (coding theory), the gloss
`纠错码的理论` (the theory of error-correcting codes), attribution to many mathematicians, and the
20th-century date. Importance `high` and status `已验证` are catalog metadata, not human-source or
kernel evidence. The title and gloss identify an umbrella subject, not a proposition.

## Candidate theorem families not credited

An accountable source correction could select one of many distinct families, including:

1. A finite-code packing, covering, or existence bound with fixed alphabet, length, size, and
   Hamming-distance conventions.
2. A construction and parameter theorem for a linear, cyclic, BCH, Reed-Solomon, LDPC, Turbo,
   Polar, or another specified code family.
3. A unique-decipherability or source-coding statement such as Kraft-McMillan.
4. A decoder soundness, error-correction-radius, list-decoding, or algorithmic complexity theorem.
5. An asymptotic rate-distance, random-coding, reliable-channel-coding, or capacity-achievement
   theorem under a fixed channel and probability model.

These roots differ in domains, quantifier order, hypotheses, conclusions, and proof architecture.
None is selected, asserted, or credited at intake.

## Proposition-changing decisions

Before statement work can close, an immutable source and independent review must fix:

- a named theorem, edition, theorem/section/page locator, incorporated definitions, proof boundary,
  correction and errata status, and historical attribution;
- error-correcting channel coding versus uniquely decodable source coding, and whether the root is
  finite, probabilistic, algorithmic, or asymptotic;
- alphabet or field, word carrier and block length, finite/nonempty assumptions, code as a set,
  submodule, encoder image, language, ensemble, or family, and all universes and typeclasses;
- Hamming or another distance, minimum-distance convention, weight, code size or dimension, rate,
  logarithm base, redundancy, and normalization and rounding conventions;
- channel, error pattern or probability law, encoder, decoder, tie-breaking, received-word model,
  deterministic versus randomized behavior, and allowed computation or oracle boundary;
- the exact result type: upper or lower bound, existence, construction parameters, correction or
  detection guarantee, decoding success, duality or enumerator identity, convergence, capacity,
  complexity, or a checked conjunction;
- ordered binders and whether a conclusion is uniform, existential, eventual, high-probability,
  average-case, worst-case, or asymptotic, including strict/non-strict endpoints; and
- the foundation, classical-choice, finite-computation, certificate, and TCB policies.

Choosing values for these rows creates a theorem; the catalog does not provide them.

## Boundary and degenerate cases

The statement phase must explicitly decide empty and singleton alphabets; block lengths zero and
one; empty and singleton codes; zero-dimensional linear codes; distance zero or larger than the
block length; code size zero; rate and error endpoints; no errors and uncorrectable error patterns;
noninjective encoders; incomplete, ambiguous, or tie-producing decoders; zero-probability channel
events; nonexistent extrema; divisibility and field-size constraints; finite versus infinite
families; and limsup/liminf versus actual limits. No case is silently excluded here.

## Neighbor and substitution exclusions

- `THM-M-1577` through `THM-M-1581` separately own information theory, entropy, capacity, and
  Shannon coding theorems. Their statements or evidence do not repair this topic label.
- `THM-M-1586`, `THM-M-1587`, and `THM-M-1588` separately own the Hamming, Singleton, and
  Gilbert-Varshamov bounds.
- `THM-M-1589` through `THM-M-1595` separately own linear, cyclic, BCH, Reed-Solomon, LDPC, Turbo,
  and Polar code families.
- The named rows under `Docs/researches/cs_theorems.md` sections 10.2 and 10.3 are taxonomy and
  discovery leads. They cannot be conjoined into a new general root or transfer proof credit.
- Hamming distance, a set of codewords, unique decodability, a parity-check matrix, a toy code, or
  the Kraft-McMillan inequality cannot be presented as the unspecified whole of coding theory.
- A structure field, decoder oracle, simulation, numerical experiment, unchecked certificate, or
  the catalog label `已验证` cannot assume or establish a requested theorem.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.InformationTheory.Hamming` supplies Hamming distance, norm, and metric interfaces, while
`Mathlib.InformationTheory.Coding.UniquelyDecodable` and `KraftMcMillan` supply a source-code
definition, elementary consequences, and the Kraft-McMillan inequality. `IntakeProbe.lean` checks
representative types and their reported axioms. These are discovery-only adjacent APIs. Because no
canonical proposition exists, none is a usable artifact for the root, which remains `M4`; they
neither define a selected error-correcting-code problem nor prove an umbrella proposition.

This scope map supports the planned intake only. Source selection, statement elaboration, anchor
audit, obligation freeze, proof, validation, and release remain separate open phases.
