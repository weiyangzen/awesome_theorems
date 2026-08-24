# Machine-checked audit — S5-CLM-00003579

## Closure record

The proposed root is `s5_clm_00003579_proof_transport`, at machine level
`M0-P`, with trust `0`, an empty observed-axiom list, and an empty machine cut
set.  Its root expression is bound to the semantic-environment digest in
`statement-crosswalk.json`.  The declaration census and dependency edges are
explicit rather than inferred from prose.

The task-local gate intentionally runs in semantic/evidence mode (`--no-lean`)
and does not claim canonical kernel acceptance.  A cold replay from source
must re-elaborate all three Lean surfaces at trust zero, recompute the
transitive non-foundation census by declaration/type/body/source/revision hash,
and reject any provider proof body or unreviewed oracle.

## Required replay assertions

- exact provider revision and source file digest;
- equal source and target elaborated-root digests;
- no local semantic shadowing or parser substitution;
- no placeholders, unsafe injection, or claim-specific axioms;
- exact-root M0-L/W/P closure and empty H/M/R cut sets;
- semantic-substitution mutation failures;
- offline cold-from-source replay.

The worker records these as requirements and leaves the independent Master
recomputation flag set.
