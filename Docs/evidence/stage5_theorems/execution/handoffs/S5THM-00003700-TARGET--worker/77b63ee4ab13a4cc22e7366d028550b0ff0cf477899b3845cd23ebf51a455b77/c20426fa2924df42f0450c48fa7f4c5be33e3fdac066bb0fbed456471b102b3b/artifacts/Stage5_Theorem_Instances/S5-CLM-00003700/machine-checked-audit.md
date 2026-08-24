# Machine-checked audit candidate

The claim-owned Lean surface consists of `Statement.lean`, `Proof.lean`, and
`Audit.lean`. Each imports `Mathlib`; each retains the frozen numeric provider
module and qualified declaration in a non-executable provenance comment. The
surface introduces theorem declarations only. A source scan found no local
semantic definition, alias, parser extension, unsafe declaration, claim axiom,
bodyless oracle, or proof placeholder.

`machine-closure.json` binds the proposed root, declaration census, dependency
edges, observed axiom set, empty machine cut set, and cold-from-source replay
predicate. Because this generation is expressly no-Lean, those records are
preflight evidence for mandatory independent Master recomputation, not a
canonical acceptance receipt. Master acceptance must fail if elaboration,
dependency census, trust-zero replay, or any substitution mutation differs.
