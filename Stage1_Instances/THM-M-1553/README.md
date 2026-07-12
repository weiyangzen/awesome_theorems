# THM-M-1553 rev-5.6 dossier

This directory is the `planned` intake for the Hirota bilinear method. The repository label names
a method, not a single theorem. To avoid inventing a universal claim, the intended first theorem is
scoped to the KdV equation: under explicit smoothness and nonvanishing hypotheses, the standard
tau substitution and Hirota bilinear identity imply KdV, with a separately specified soliton-family
corollary only after its dispersion and bilinear identities are proved.

The legacy Lean module is discovery input only. It fixes useful KdV sign conventions and proves
abstract certificate plumbing, but its derivative data and bridge propositions are assumed fields;
it therefore receives no rev-5.6 statement or proof credit. The provisional root vector is
`[H3, M4, R4]`. No exact Lean target, audit completion, or theorem completion is claimed.

The statement phase now freezes and elaborates that intake-selected KdV bridge in `Statement.lean`;
its structured identity and replay evidence are in `statement.json` and `statement-validation.md`.
This is provisional statement evidence only. The scope map, source crosswalk, and open task DAG
continue to define downstream work, and intake validation remains recorded in `validation.md`.
