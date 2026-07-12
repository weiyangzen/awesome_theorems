# Scope map

## Received claim

The repository supplies only the title "Jacobson density theorem" and the gloss "the density
theorem for primitive rings." It does not supply a truth-valued proposition. Intake therefore
freezes a theorem-family boundary, not an invented canonical theorem.

## Candidate classical boundary

A standard candidate reading has the following ingredients, all still requiring a pinpoint source
and a checked Lean transport:

- an associative ring `R`, with unit conventions and left-versus-right handedness fixed;
- a faithful simple left `R`-module `M`, expressing the primitive-ring hypothesis;
- the division ring `D = End_R(M)`, with multiplication/opposite-ring and scalar-action conventions
  made explicit;
- a finite family `x_i` in `M` that is linearly independent over `D`;
- an arbitrary family `y_i` in `M` indexed by the same finite set;
- an element `r : R` such that `r • x_i = y_i` for every index;
- equivalently, after a checked bridge, density of the image of `R` in `End_D(M)` for the finite or
  pointwise topology.

The quantifier order, whether the empty family is allowed, and the precise action/op convention are
part of the statement and may not be filled in from memory.

## Pinned formal-candidate boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.RingTheory.SimpleModule.Basic` provides:

1. `jacobson_density`: for a ring `R`, an additive commutative group `M`, an `R`-module structure,
   and `IsSemisimpleModule R M`, every `End (End R M) M` map agrees on a finite set `s : Finset M`
   with scalar action by some `r : R`.
2. `Module.Finite.toModuleEnd_moduleEnd_surjective`: if `M` is additionally finite over
   `End R M`, the scalar-action map from `R` onto `End (End R M) M` is surjective.

The first is a semisimple-module generalization in a finite-set functional form. Specializing it to
a simple module is plausible because mathlib makes every simple module semisimple, but its
relationship to the classical faithful-simple/independent-family statement still needs checked
handedness, Schur-division-ring, independence-extension, and faithfulness bridges. The second adds
a finiteness hypothesis and is not a substitute for unrestricted finite interpolation.

## Decisions required at statement freeze

1. Pin and independently inspect the intended primary or authoritative source passage, including
   incorporated definitions, theorem number/page, assumptions, proof boundary, and errata.
2. Fix unitality, associativity, module handedness, and the exact definition of "primitive ring."
3. Fix the endomorphism ring or opposite ring and the induced scalar action on `M`.
4. Select the root form: primitive-ring interpolation, faithful-simple-module interpolation, or
   finite-topology density; record checked transports rather than treating names as equivalence.
5. Decide whether mathlib's semisimple finite-set statement is the canonical target, a stronger
   bridge theorem, or merely an anchor candidate.
6. Resolve empty/singleton index sets, the zero module or zero ring, repeated vectors, finite
   dimensionality over the endomorphism division ring, and nonfaithful modules.

## Explicit exclusions

- The Jacobson radical, Jacobson rings, or Nullstellensatz-style Jacobson properties.
- Analytic, measure-theoretic, topological-vector-space, or combinatorial density theorems.
- A matrix-density or finite-dimensional Artin-Wedderburn result as the unrestricted root.
- The finite-over-`End_R(M)` surjectivity corollary as a substitute for general finite
  interpolation.
- Mathlib's semisimple-module generalization without a source-fidelity and transport decision.
- A proposition that assumes the desired interpolation or surjectivity conclusion.
- The catalogue `已验证` label, a theorem-name match, or the intake probe as proof credit.

No canonical Lean expression, ordered binders, hypotheses, conclusion, alternate encoding, or
degenerate-case exclusion is frozen in this intake.
