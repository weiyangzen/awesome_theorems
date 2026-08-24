# Full study — S5-CLM-00003516

## Source identity {#study-source-identity}

The frozen statement is `Arxiv.«2602.05192».four_3` from provider revision
`2270d31e8dd611521f979de6d86da364930b7669`. It asks whether the reciprocal
root-interaction functional for degree-three monic real-rooted polynomials is
superadditive under finite additive convolution. The source file and exact
declaration/type digests are recorded in `intake.json` and the crosswalk.

## Statement crosswalk {#study-statement-crosswalk}

The crosswalk is bidirectional: a forward theorem transports the frozen source
expression to the target and a reverse theorem transports it back. Both are
needed—one implication cannot prove semantic equality. Provider, revision,
source, declaration, elaborated expression, and transitive constants are bound;
the local shadow and semantic-substitution inventories are empty.

## Proof DAG {#study-proof-dag}

The structured DAG contains five substantive nodes. The following fragments are
the sole readable renderings of those nodes, so reverse coverage is exact.

### Root transport {#fragment-pu-root}

Hypothesis: source and target have the same Master-recomputed elaborated
expression. Inference: combine independently checked forward and reverse maps by
iff introduction. Output: exact bidirectional root transport. Formal anchor:
`Proof.root`. Downstream uses: semantic and axiom audits. Exceptional cases:
digest mismatch, one-way transport, or substituted semantics. Trust boundary:
Lean checks the local composition; Master checks the provider binding.

### Forward transport {#fragment-pu-forward}

Hypothesis: a proof inhabits the source proposition. Inference: move it across
the exact expression identity without changing meaning. Output: a target proof.
Formal anchor: `Proof.forward`. Downstream use: the forward half of the root.
Exceptional cases: any shadowing definition, coercion, alias, notation, macro, or
substitute import. Trust boundary: provider identity is Master-controlled.

### Reverse transport {#fragment-pu-reverse}

Hypothesis: a proof inhabits the target proposition. Inference: move it back
across the same exact identity. Output: a frozen-source proof. Formal anchor:
`Proof.reverse`. Downstream use: the reverse half of the root. Exceptional case:
forward-only coverage. Trust boundary: reverse coverage is checked independently.

### Semantic audit {#fragment-pu-semantic-audit}

Hypothesis: frozen member, provider bytes, and locator are exact. Inference:
compare elaborated expression plus transitive declaration/type/body/source and
revision bindings. Output: an exact semantic-environment lock with no shadow or
substitution. Formal anchor: `Audit.elaborated_root_expression_agrees`.
Downstream uses: M0 and release dominance. Exceptional case: a text-identical
header without semantic evidence. Trust boundary: worker hashes are provisional.

### Axiom audit {#fragment-pu-axiom-audit}

Hypothesis: all root-relevant local artifacts elaborate at trust zero. Inference:
inspect terminal axiom queries and the dependency census. Output: empty observed
axioms and empty H/M/R cut sets. Formal anchor: `Audit.target_to_source_audit`.
Downstream use: provisional release. Exceptional case: using the provider's
`sorryAx` theorem as proof. Trust boundary: only Master can accept completion.

## Trust boundary {#study-trust-boundary}

The source repository is authoritative for the statement, not for proof closure.
The local Lean kernel establishes only the claim-owned proof terms. The worker
cannot self-authenticate semantic identity or acceptance; canonical Master
recomputation is mandatory.
