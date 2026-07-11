# THM-M-1239 rev-5.6 intake

This is the `planned` dossier for the PDE/Sobolev Poincare inequality. The repository fixes only
the name, the PDE category, and the gloss "an L^p estimate for Sobolev functions." It does not
specify a domain, function space, normalization, boundary condition, exponent, gradient notion, or
constant. Those choices distinguish materially different Poincare inequalities, so intake does not
invent one.

The structured record is in `intake.json`; `scope_map.md` records the included surface and explicit
exclusions; `source_statement_crosswalk.md` maps every available source field to what it actually
supports.

## Intake verdict

Lifecycle is `planned` and the root vector is `[H4, M4, R4]`. Exact source-statement identification
is the first failed gate. No Lean expression or proof is credited, and the theorem is not complete.

## Validation

`validation.md` records the exact structural checks for this intake. Master acceptance and every
dependent node remain outstanding.
