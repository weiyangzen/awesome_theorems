# Full study — Erdős Problem 119, part (ii)

## Frozen mathematical object

The source asks whether there is a positive real exponent `c` for which the
unit-circle maximum `M z n` exceeds `n ^ c` on infinitely many natural
indices, for every sequence `z` whose terms have norm one.  The pinned source
declaration is `Erdos119.erdos_119.parts.ii`, at bytes 3179–3617 of the
revision recorded in `intake.json`.

## Formal transport

The statement crosswalk binds the source declaration/type digests, source file,
provider revision, elaborated source/target root digest, and a complete
transitive constant census.  The three Lean surfaces repeat the frozen module
and qualified declaration in provenance comments and use only claim-owned
transport theorem names in their executable portion.

## Mathematical content inventory

* Hypotheses: an arbitrary sequence `z : ℕ → ℂ` and the pointwise condition
  `‖z i‖ = 1`.
* Inference: choose a real `c` with `c > 0` and establish infinitude of the
  index set cut out by `M z n > n ^ c`.
* Output: the existential exponent, positivity witness, and infinite set.
* Exceptional cases: the natural-index convention and the source's
  zero-indexed product convention are retained in the source anchor.
* Trust boundary: worker evidence is provisional; only canonical Master
  replay can certify the elaborated root and release state.

Beck's cited result supplies the mathematical context for the positive answer,
but this package does not treat a citation or the provider's open proof as a
kernel proof.  The structured proof-unit, machine, readability, and release
ledgers are authoritative for the handoff.
