# Intake validation

Base revision: `a8d6489fd935cd71fa4499f2f3f5b051998203f4`.

The worker ran the repository standard validator, target-manifest validator,
target lookup, JSON/YAML parsing, scoped hygiene checks, and confirmed that the
planned dossier contains no theorem-completion claim. Exact commands and exit
codes are recorded in the workspace self-test manifest.

Known open gates: Lean elaboration and expression/environment fingerprints;
checked alternate-encoding transport and mutations; pinpoint primary-source
theorem/page/assumption/errata review; formal-anchor audit; frozen obligation
registry; proof, validation, and release. These belong to later DAG nodes.
