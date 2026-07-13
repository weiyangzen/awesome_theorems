# THM-M-0945 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Green-Tao theorem. The
repository catalog supplies the slogan "the primes contain arbitrarily long arithmetic
progressions," attributes it to Ben Green and Terence Tao in 2004, and labels it `verified`.
Under rev-5.6 that label is untrusted inventory metadata, not source review, an exact Lean
proposition, or machine-proof evidence.

The matching primary paper was inspected. Green and Tao's Theorem 1.1 says that the prime numbers
contain infinitely many arithmetic progressions of length `k` for every `k`. This identifies the
intended theorem family far more sharply than the catalog slogan, but intake does not silently
choose a Lean encoding. The source passage does not itself spell out the quantifier domain for
`k`, the witness representation, the positive common-difference condition, or the treatment of
small lengths. Those choices, the source-to-catalog mapping, corrections and errata, and an
independent review remain open.

The provisional vector is `[H1, M4, R4]`: a matching complete human proof and pinpoint theorem
source are known but not fully crosswalked and reviewed; no usable exact formal artifact is
credited; and no source-faithful readable reconstruction has been admitted. `IntakeProbe.lean`
checks only adjacent pinned prime, three-term-progression, Roth, and finite-color APIs. None is the
Green-Tao theorem, and the probe contains no target declaration or proof body.

`instance.json` is the structured scope authority. `scope-map.md` freezes proposition-changing
choices and exclusions, `source-statement-crosswalk.md` records source and formal boundaries, and
`task-dag.json` leaves all six downstream phases open. No canonical Lean proposition, H0, M0, R0,
accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
