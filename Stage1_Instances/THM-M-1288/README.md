# THM-M-1288 rev-5.6 intake

This is the rev-5.6 `planned` dossier for Talenti's sharp Sobolev inequality. The
Stage0 label `已验证` is untrusted discovery metadata and supplies no proof credit.

The root intended here is the Euclidean sharp first-order Sobolev inequality:
for `1 < p < n`, with `p* = np/(n-p)`, compactly supported smooth real-valued
functions on `R^n` satisfy `||u||_(p*) <= C(n,p) ||grad u||_p`, where Talenti's
constant is optimal. Equality/extremizer classification is part of the source
theorem family but is not silently included in the inequality-only root.

The structured scope is in `intake.json`, the included and excluded surfaces are
in `scope-map.md`, and source wording is compared with the prospective Lean
statement in `source-statement-crosswalk.md`. Exact constants, endpoint
conventions, completion from test functions to the homogeneous Sobolev space,
and any equality statement remain statement-phase decisions requiring checked
transports.

## Intake verdict

Lifecycle is `planned` and the provisional vector is `[H1, M4, R3]`. A primary
paper has been identified, but no immutable copy, page-level premise audit, or
independent source review is accepted. No canonical Lean declaration has yet
been elaborated. The theorem is not complete.

## Validation

`validation.md` records the exact structural checks run for this intake. They
validate repository membership and dossier syntax/references only, not the
mathematical claim or a Lean proof.

## Statement phase

`Statement.lean` now freezes and kernel-elaborates the inequality-plus-least-
constant target under three direct pinned mathlib imports. `statement.json` and
`statement-validation.md` bind its exact declaration, formula, environment,
hashes, structural mutations, and validation command. This advances only the
provisional statement node; the primary-source formula audit, proof, and all
later assurance gates remain open, and the theorem remains incomplete.

## Obligation-tree phase

`obligation-registry.json` freezes 19 canonical semantic obligations before
proof status, with separate machine, human-source, and readability
denominators. `typed-graphs.json` records proof/refinement, provenance,
evidence, trust, documentation, and workflow graphs. The checked
`ObligationTree.lean` composition consumes exact admissibility and optimality
packages and returns the frozen root; both packages remain open, so this phase
supplies no theorem-proof or completion claim. Validation and the precise root
cut set are recorded in `obligation-tree-validation.md`.

## Proof phase

`Proof.lean` closes the bounded elementary domain facts, the exact gradient to
Frechet-derivative norm transport, and the zero-function boundary branch. The
sharp rearrangement, radial, weighted, constant, and extremizing-sequence
obligations remain open, and the root is still conditional on explicit
admissibility and optimality packages. Exact commands and the remaining cut
set are recorded in `proof-validation.md`.
