# Scope map

## Preserved repository scope

The mathematical catalog fixes only the title `BCH码`, attribution
`Bose/Chaudhuri/Hocquenghem`, year 1959, and gloss `能纠正多个错误的码`. A parallel
computer-science catalog record says 1959-60 and `循环纠错码` ("cyclic error-correcting code").
The latter is outside the rev-5.6 target set and supplies no accepted state, but it confirms that
the repository records a code family rather than one binder-complete proposition.

Intake preserves the narrow family identity: algebraically constructed BCH codes and their
multiple-error-correction properties. It does not yet select a binary or q-ary statement,
construction or bound, finite or algorithmic conclusion, or exact formula.

## Proposition-changing decisions

An approved statement phase must select all of the following from an immutable reviewed source:

- the base finite field and its cardinality, including binary versus q-ary scope;
- the finite extension, embedding, primitive root or element, and multiplicative-order convention;
- the word index type, block length, and whether the code is represented as a polynomial ideal,
  residue class, linear subspace, set of words, encoder image, or equivalent structure;
- primitive versus nonprimitive and narrow-sense versus general starting exponent;
- the generator or check polynomial and the exact interval of consecutive roots, including modular
  wraparound and duplicate-root conventions;
- designed distance `delta`, actual minimum Hamming distance, correction radius `t`, and the exact
  bridge from distance to the selected decoder/correction notion;
- whether the conclusion is existence/construction, the BCH lower bound on distance, a
  dimension/redundancy estimate, unique-decoding capability, or correctness of a named decoder;
- strict and non-strict inequalities, floors, natural subtraction, divisibility, and every
  admissible range for length, extension degree, starting exponent, distance, and radius;
- all ordered binders, typeclasses, hypotheses, witnesses, and claimed alternate encodings; and
- zero-length, trivial-field, empty-root, zero/full-code, endpoint-distance, and decoding-tie cases.

These decisions change the proposition. They are a resolution ledger, not an asserted theorem.

## Candidate families not credited

- General BCH construction: choose consecutive powers of a suitable element in a finite extension
  as zeros of a generator polynomial, producing a cyclic code over the base field.
- BCH designed-distance bound: an appropriate consecutive-root hypothesis implies actual minimum
  Hamming distance at least `delta`.
- Error-correction corollary: under a fixed decoding definition, minimum distance at least
  `2 * t + 1` permits correction of up to `t` errors.
- Primitive narrow-sense specialization: length `q^m - 1`, starting exponent one, with a common
  binary version using designed distance `2 * t + 1`.
- Dimension or redundancy bound, typically obtained from degrees of minimal-polynomial factors.
- Syndrome, locator-polynomial, or other algebraic decoder correctness.

None is the canonical target until source review selects it and checks its relationship to the
catalog wording. A proof of one does not silently prove every other family member.

## Explicit exclusions

- THM-M-1589 (`线性码`) and THM-M-1590 (`循环码`) are broader neighboring targets. Linearity and
  cyclicity alone do not provide BCH distance or decoding behavior.
- THM-M-1592 (`Reed-Solomon码`) is a distinct algebraic code family whose evaluation and MDS claims
  must not be imported as BCH proof credit.
- Stage0-only THM-C-0382 is a parallel inventory record, not an accepted duplicate theorem.
- A binary primitive example, small finite computation, simulation, or successful decoder run
  cannot establish an unspecified universal BCH statement.
- Hamming distance, finite fields, primitive roots, and cyclotomic polynomials are ingredients. An
  API check for them is neither a BCH definition nor a proof.
- A structure field or hypothesis that assumes the desired distance or correction guarantee is
  circular and excluded.

## Formal surface and current boundary

Pinned mathlib has generic Hamming metric/weight APIs, finite-field cardinality and Frobenius APIs,
and polynomial/root-of-unity APIs. The discovery-only Lean probe checks ten adjacent declarations.
The bounded repository and pinned-mathlib search found no exact-topic BCH or coding declaration.
That result is not an exhaustive formal anchor audit and gives no proof credit.

Until statement selection, the Lean module, declaration/expression, normalized expression hash,
environment fingerprint, quantifiers, hypotheses, checked transports, excluded cases, discovery
hash, and obligation-registry hash remain null or empty. This is a hard blocker for tree
construction, not permission to broaden the source claim.

## Open gate

An independent coding-theory reviewer must admit an immutable primary source proposition and map
every definition, binder, assumption, conclusion, proof boundary, correction, and degenerate case.
Only then may the statement phase choose a matching Lean encoding and run its required expression,
transport, and mutation gates.
