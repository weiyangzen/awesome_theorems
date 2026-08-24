# Build validation

Validation environment: canonical repository `Formalizations/Lean`, pinned `lean-toolchain`, offline lake environment, trust level zero.

Independently checked artifacts:

- `Statement.lean`: exit 0; only an unused-variable linter warning.
- `Proof.lean`: exit 0; deprecation and unused-tactic linter warnings only. Root axiom output: `[propext, Classical.choice, Quot.sound]`.
- `Audit.lean`: exit 0; no diagnostics.

Static declaration-policy scan: no `sorry`, `admit`, axiom, unsafe declaration, opaque declaration, `def`, `abbrev`, structure, inductive, class, instance, notation, syntax, macro, namespace alias, or local instance.

The authoritative release gate is the frozen command `complete-target-semantic-proof-debt`; its final receipt is recorded in `receipts/current-validation.json`.
