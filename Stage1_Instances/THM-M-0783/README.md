# THM-M-0783 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for Martin's axiom. The repository source describes
the item only as an "axiomatization of forcing" and labels it verified. That wording does not state
a theorem, and the label supplies no source or machine-proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Claim identity | The usual family `MA(kappa)` for every cardinal `kappa` strictly below the continuum | MA is an additional set-theoretic axiom, not a theorem asserted to follow from ZFC |
| Order data | A nonempty partial order, dense subsets, a filter, and the requirement that the filter meet every specified dense set | Forcing-order orientation and filter closure conventions are not yet selected |
| Chain condition | The countable chain condition on the partial order | Antichain encodings and their transports require exact formal checking |
| Cardinal bound | At most `kappa` dense sets with `kappa < 2^aleph_0` | The strict bound must not become `<= continuum`; cardinal and continuum encodings remain open |
| Formal target | Lean 4 representation of the object-level axiom or of satisfaction in a set-theory model | No module, declaration, expression hash, or environment fingerprint is credited |
| Metatheory | Later source audit may separately model relative consistency, independence, or consequences | Such theorems are not substitutes for the axiom target |
| Exclusions | PFA, Martin's maximum, and `MA + not-CH` | Stronger forcing axioms and theories require separate theorem IDs and statements |

## Planned boundary

The intake freezes a standard definition family and records the unresolved foundational choice. It
does not introduce a proof body or an assumed Lean constant. In particular, representing MA by an
unproved `axiom` declaration would be faithful as a theory extension but would not be a machine
proof of MA and cannot close this target under rev-5.6.

The initial root vector is `[H5, M4, R3]`: the received item is an axiom rather than an ordinary
proved proposition, no exact Lean target is selected, and no independently reviewed reconstruction
exists. The statement phase must either preserve this barrier classification or explicitly redirect
the target to a precisely sourced metatheorem such as a relative-consistency result; it may not make
that substitution silently.

The canonical record and open intake DAG are in `intake.json`. Source fidelity and the distinction
between definition, consistency, and consequences are recorded in `source_statement_crosswalk.md`.
Commands and exact results for this worker's structural self-test are in `validation.md`.

## Status

Lifecycle is `planned`. Audit completion and theorem completion are both false. Master acceptance
is pending, and no later phase or checklist state is claimed here.
