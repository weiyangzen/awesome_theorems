# Scope map

## Included subject boundary

- An elliptic curve over the rationals (or the exact number-field domain selected by the source),
  an odd prime, its reduction type, and the associated complex and p-adic L-functions.
- Characters, conductors, periods, Euler factors, measures or modular symbols, and interpolation
  normalization needed by the selected source theorem.
- If the exceptional-zero interpretation is selected: split multiplicative reduction, the Tate
  period, p-adic logarithm, L-invariant, derivative order, and the leading-term formula.
- If Mazur-Tate elements are selected: the finite group rings, augmentation filtration,
  specialization maps, and normalized modular-symbol coefficients.

## Required source decision

The Chinese title and one-line gloss do not determine whether the root is (1) construction and
interpolation of an elliptic-curve p-adic L-function, (2) the exceptional-zero formula commonly
associated with Mazur, Tate, and Teitelbaum, or (3) a theorem about Mazur-Tate elements and their
specializations. These have different hypotheses and conclusions. The statement phase must select
one theorem from a stable primary source and transcribe its complete assumptions before authoring a
Lean proposition; it must not merge the alternatives.

## Explicit exclusions

- The complex analytic continuation or functional equation alone.
- A generic interpolation predicate assumed as a hypothesis and returned as the conclusion.
- A special-case modular-symbol computation presented as the named general theorem.
- The manifest's untrusted `已验证` label as source, statement, or proof evidence.

The later statement phase must freeze universes, coefficient fields, embeddings and valuations,
period and Euler-factor conventions, reduction and conductor conditions, boundary cases, imports,
declaration type, environment fingerprint, transports, and hypothesis mutations.
