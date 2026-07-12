# Scope map

## Included topic boundary

- Decision languages over a source-specified finite alphabet and encoding.
- A source-specified deterministic or nondeterministic machine model with a precise work-space
  measure and polynomial bound.
- PSPACE membership of one named decision problem.
- PSPACE hardness of that same problem under one fixed, resource-bounded many-one reduction.
- The conjunction of membership and hardness, only after the source fixes the preceding data.

## Ambiguities to resolve at statement freeze

The repository record does not name a complete language. At least these materially different
readings fit its wording:

1. TQBF (true quantified Boolean formula) is PSPACE-complete.
2. A different named problem, such as a game, planning problem, or model-checking problem, is
   PSPACE-complete.
3. There exists a PSPACE-complete language, without selecting the usual TQBF representative.
4. A survey-style collective claim classifying several problems as PSPACE-complete.

The statement phase must inspect an immutable source and freeze exactly one proposition. It must
fix syntax and well-formedness, encoders/decoders, the accept/reject and halting convention,
read-only input versus counted work tapes, whether the bound is on visited cells or configuration
size, and whether reductions are deterministic polynomial time, logspace, or another convention.
It must also fix binder order, malformed input behavior, empty input, polynomial coefficients, and
encoding invariance.

## Explicit exclusions

- `IP = PSPACE`, `NPSPACE = PSPACE`, or a hierarchy/separation theorem as a substitute.
- A proof that an unnamed or abstractly assumed language is complete.
- NP-completeness, EXPTIME-completeness, or LTL model-checking complexity without a source mapping.
- Computable many-one hardness in place of the source's polynomial-time or logspace hardness.
- Time bounds in place of space bounds.
- Treating the manifest label `已验证` as source, kernel, or proof evidence.
- Packaging the desired membership and hardness facts as assumed structure fields.

No canonical Lean target is frozen at intake. Mathlib's generic language and machine APIs are
encoding ingredients, while the bounded pinned search did not identify a general PSPACE predicate
or polynomial-space machine interface.
