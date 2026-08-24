# Machine-checked audit

The terminal declaration is
`AwesomeTheorems.Stage5.S5_CLM_00003549.machine_root`. `Audit.lean` reconstructs its witness,
finite exclusion, monotonicity lemma, and composition without importing claim-local proof output.
It then supplies the exact required witness against
`type_of% Erdos1.erdos_1.variants.least_N_5` and issues the terminal `#print axioms` query.

No provider proof term, claim-specific axiom, `sorry`, `admit`, unsafe declaration, opaque oracle,
or local semantic redefinition occurs. The finite decision uses file-scoped unbounded heartbeats
and recursion depth 100000 so that both generated proof construction and final kernel reduction
are covered. These options change resource limits only.

The worker records the expected permitted foundation set. Master must independently compile all
three Lean files with trust zero in the sealed provider-native environment, recompute the exact
root and semantic environment, and compare the observed terminal axiom report before acceptance.
