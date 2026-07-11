# THM-M-1200 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the Rankine-Hugoniot condition. The repository
source says only "jump condition for shocks". To avoid silently mixing inequivalent PDE settings,
this instance selects the standard one-dimensional scalar conservation-law theorem. The selection
must be reviewed against primary sources before source fidelity can advance.

The structured claim and boundaries are in `intake.json`. `scope-map.md` records included and
excluded mathematical surfaces, while `source-statement-crosswalk.md` records exactly what the
repository sources do and do not establish.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H3, M4, R3]`. The first open dependent gate is
the statement gate: no Lean declaration, normalized expression fingerprint, environment fingerprint,
or mutation-tested weak-formulation encoding exists. No historical `已验证` label is proof evidence,
and the theorem is not complete.

## Validation boundary

The commands and exact results in `validation.md` establish target membership, standard consistency,
JSON syntax, required dossier fields, and local reference integrity only. They do not validate the
mathematics or elaborate a Lean proposition.
