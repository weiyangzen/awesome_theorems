# Machine-checked audit — S5-CLM-00003528

The proposed root is `AwesomeTheorems.Stage5.S5_CLM_00003528.audit_exact_surface_expression` at level M0-L. The structured declaration census, dependency edges, observed axioms, semantic environment, and cut set live in `machine-closure.json`; they are not duplicated here.

The frozen Formal Conjectures declaration contains `sorryAx`. It is accepted solely as a statement locator and is never called by a claim-owned proof. The three claim-owned files import `Mathlib`, carry the exact provider module/declaration in provenance comments, and contain only theorem declarations with explicit bodies. There is no `sorry`, `admit`, axiom, opaque declaration, unsafe injection, local semantic definition, notation, macro, instance, coercion, or alias.

The task-local validation mode is deliberately `--no-lean`: this generation does not invoke Lean, Lake, or Elan. Consequently, its M0-L record is a provisional machine-closure proposal binding exact source and target bytes. Canonical Master must compile every harvested Lean file at trust zero from a clean offline source state; enumerate each declaration's actual type, body, dependencies, and axioms; reject stale object reuse; and independently recompute the root expression and transitive non-foundation environment before acceptance.

The cold-replay test must show that no object from the source provider's sorry-backed theorem body enters the claim-owned dependency closure. The mutation suite must reject carrier, index, coefficient, sine, exponent, denominator, predicate, import, parser, and alias substitutions. Any mismatch invalidates this proposal rather than downgrading it to partial completion.
