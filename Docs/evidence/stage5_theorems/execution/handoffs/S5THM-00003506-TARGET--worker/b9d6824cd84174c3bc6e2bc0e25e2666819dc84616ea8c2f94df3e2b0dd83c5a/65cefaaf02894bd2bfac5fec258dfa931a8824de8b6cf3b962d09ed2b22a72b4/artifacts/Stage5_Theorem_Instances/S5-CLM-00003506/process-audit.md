# Process audit — S5-CLM-00003506

This claim-local dossier binds one TARGET to the frozen Formal Conjectures
provider record and its Stage6 alias.  The source bytes, declaration bytes and
formal type digest are recorded in `intake.json` and the bidirectional semantic
crosswalk.  No predecessor or sibling task material was used.

The three Lean surfaces are compiled cold with the pinned Lean toolchain at
`--trust=0`; each retains the exact provider module/declaration as a frozen
binding witness and introduces no local definitions, notation, parser rules,
axioms, unsafe code, placeholders, or import substitutions.

Sub-checklist: INTAKE, STATEMENT, ANCHOR, TREE, MACHINE, READABLE, VALIDATE,
RELEASE.  Master recomputation remains required for final acceptance.
