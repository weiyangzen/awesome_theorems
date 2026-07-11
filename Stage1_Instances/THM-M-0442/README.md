# THM-M-0442 rev-5.6 intake

This directory is the `planned` rev-5.6 dossier for Mazur's rational torsion theorem. The frozen
human claim classifies the abstract torsion subgroup of an elliptic curve over `Q`: it is cyclic of
order `1` through `10` or `12`, or isomorphic to `Z/2Z x Z/2mZ` for `m = 1, 2, 3, 4`.

The historical Lean file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_088.lean` is discovery
input only. It expresses the same list using `ZMod 2 x ZMod n` with `n in {2,4,6,8}` and contains
checked cardinality bridges, but its `StatementShape` has no terminal proof. This intake gives that
file no inherited proof or acceptance credit.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. A primary proof source has been
identified but its exact theorem/page, assumptions, edition hash, and errata have not been audited.
An unaccepted Lean expression exists, but exact-statement elaboration, encoding transports, and
mutation tests belong to the next phase. No theorem completion is claimed.

See `scope-map.md`, `source-statement-crosswalk.md`, `instance.json`, and `task-dag.json`. The
commands and their limits are recorded in `validation.md`.
