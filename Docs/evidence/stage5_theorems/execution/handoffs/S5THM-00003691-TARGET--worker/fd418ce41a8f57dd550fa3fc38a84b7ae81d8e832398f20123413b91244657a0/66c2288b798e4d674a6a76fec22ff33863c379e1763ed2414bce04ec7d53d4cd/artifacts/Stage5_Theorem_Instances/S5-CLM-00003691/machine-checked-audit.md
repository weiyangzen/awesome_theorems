# Machine-checked audit — S5-CLM-00003691

Machine level proposed: **M0-L**. The root is
`AwesomeTheorems.Stage5.S5_CLM_00003691.path_formula_iff`.

The closure consists of two transparent directions. Forward specialization
applies the exact formula premise at `k`, `n`, `hk`, and `hkn`; reverse
packaging introduces the same variables and returns the normalized premise.
The only conversion is zeta reduction of `ℓ` and `ε`. There are no recursive
definitions, generated aliases, parser extensions, local instances, bodyless
oracles, unsafe declarations, `opaque`, placeholders, or claim-specific
axioms. The source theorem is mentioned only as frozen provenance and its
`sorryAx` proof body is not referenced.

The task-local worker is forbidden to invoke Lean/Lake/Elan. Accordingly,
`machine-closure.json` records the exact declarations and empty cut set for the
authorized `--no-lean` preflight, while canonical trust-zero compilation,
axiom inspection, elaborated-root hashing, and complete transitive constant
census remain mandatory Master recomputations after harvest.

Semantic mutations covered by the audit surface:

1. Replacing `antiRamsey` with an arbitrary `altered` function cannot change
   the conclusion proved by `audit_exact_output`.
2. Dropping either `5 ≤ k` or `k ≤ n` breaks specialization.
3. Altering the path graph, either maximum branch, parity term, or equality
   output no longer matches the exact premise.
4. Reverse transport is independently stated in `Audit.lean`, which imports
   only `Mathlib` and not another generated module.

The worker-observed axiom list is empty by construction of the claim-owned
proof. Master is the authority that confirms it through kernel replay.
