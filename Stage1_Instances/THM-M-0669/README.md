# THM-M-0669 rev-5.6 intake

This directory is the fail-closed `planned` intake for Tarski's quantifier-elimination theorem for
real closed fields. The repository gloss says only "quantifier elimination for real closed fields".
The human scope is therefore frozen to the standard theorem that every first-order formula over a
real closed field, in a fixed language of ordered rings or a checked definitionally equivalent
language, is equivalent over the theory of real closed fields to a quantifier-free formula.

The intake did not choose between ordered-ring primitives and a pure ring language with definable
order. The statement phase now selects the pure ring language and the complete theory of `Real`,
without silently identifying quantifier elimination with decidability. Pinpoint primary-source
review and the mathematical presentation bridge remain downstream obligations.

`Statement.lean` now freezes and elaborates the exact pure-ring formula target over the complete
theory of `Real`; `statement.json`, `statement.md`, and `statement-validation.md` record its binder,
theory, boundary, environment, and mutation-test contract. This advances only the statement
interface to `M3`. It does not prove the root or accept the source bridge identifying the selected
presentation with all real closed fields. Thus H0, M0, audit completion, and theorem completion
remain unclaimed.

The immutable anchor audit classifies pinned mathlib's real-closed-field and model-theory APIs as
supporting interfaces rather than a proof. It also rejects `avigad/qelim` at immutable revision
`b7d22864f1f0a2d21adad0f4fb3fc7ba665f8e60`: that repository is a Lean 3 DLO/LIA development, not
real-closed-field quantifier elimination. No exact Lean 4 closure was found, so the fail-closed root
classification after audit remains `H1/M3/R3`: usable artifacts stop at statement/interfaces. See
`anchor-audit.md` and `anchor-audit.json`. This phase
does not claim exhaustive global discovery, H0, audit completion, or theorem completion.

The obligation-tree phase freezes a 14-node denominator and separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs.
The architecture isolates atomic and Boolean normalization, one-variable
algebraic elimination through sign conditions and projection, the semantics
bridge, and formula recursion. `ObligationTree.lean` checks only an exact-type
identity boundary that assumes the still-open root. It adds no proof credit:
the root remains `H1/M3/R3`, and master acceptance, all substantive proof
nodes, source/foundation closure, validation, and release remain open.

The proof phase now adds checked local bodies in `Proof.lean`. It proves
pure-ring atomic equality normalization through universal integer polynomials,
the complete `IsQF` Boolean closure package, and formula recursion conditional
on an explicit `OneVariableEliminationPackage`. Only `M0669-C-BOOLEAN` is
proposed provisionally closed; atomic normalization is partial because the
source-theory presentation bridge is open, while formula recursion and final
assembly retain the missing one-variable package as a premise. The exact root
therefore remains `H1/M3/R3`, with accepted closure empty. See
`proof-validation.md`, `proof-receipt.json`, and `proof-blocker.json`.
