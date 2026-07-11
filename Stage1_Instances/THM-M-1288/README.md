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
