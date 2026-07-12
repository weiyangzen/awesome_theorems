# THM-M-0312 rev-5.6 dossier

This directory is the `planned` intake dossier for the theorem called the resonance theorem in the
repository and more commonly the Banach-Steinhaus theorem or Uniform Boundedness Principle. The
frozen root scope is the normed-space form: a pointwise bounded family of continuous semilinear maps
from a Banach space to a normed space has uniformly bounded operator norms.

`Statement.lean` now freezes and elaborates that exact root with the minimal direct import
`Mathlib.Analysis.Normed.Operator.BanachSteinhaus`. It also checks an `iff` with the published
extended-nonnegative-supremum encoding, distinguishes the four required structural mutations, and
checks the empty-index boundary. Exact fingerprints and commands are in `statement.json` and
`statement-validation.md`.

The statement node is only self-tested and pending master acceptance. The imported declarations
receive no proof or provenance credit here. The root therefore remains `[H1, M3, R3]`;
`audit_complete` and `theorem_complete` are both false.
