# THM-M-1408 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Ornstein isomorphism theorem.
The repository's authoritative mathematics record supplies only the slogan "classification of
Bernoulli systems," Donald Ornstein, and the year 1970. It does not specify a Bernoulli-shift
model, entropy convention, or the meaning of isomorphism. The metadata label `已验证` is untrusted
and gives no human-source or machine-proof credit.

The likely historical referent is Donald Ornstein's 1970 paper *Bernoulli shifts with the same
entropy are isomorphic*. Its bibliographic metadata are stable, but this intake has not inspected
and pinned the theorem text, definitions, assumptions, proof boundary, or errata. In particular,
the repository record does not decide finite versus countable alphabets, finite versus infinite
entropy, one-sided versus invertible two-sided shifts, or pointwise versus modulo-null-set
isomorphism. Selecting those details from the paper title alone would invent an exact target.

This intake therefore freezes the source slogan, intended theorem family, scope decisions, and
explicit exclusions, not a canonical proposition. The provisional root vector is
`[H1, M4, R3]`. A pinned Lean probe checks only infinite-product probability measures,
measure-preserving maps, measurable equivalences, and scalar Shannon-entropy primitives. These are
encoding ingredients, not an Ornstein statement or proof.

The lifecycle remains `planned`; every downstream task and master acceptance remain open. Exact
commands and the worker-local receipt are recorded in `validation.md` and `intake-receipt.json`.

