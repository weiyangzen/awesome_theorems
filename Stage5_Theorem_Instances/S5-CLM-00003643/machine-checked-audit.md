# Machine-checked audit — S5-CLM-00003643

The proposed root is classified `M0-L`: its claim-owned composition body is local, contains no placeholder command, unsafe declaration, claim-specific axiom, opaque oracle, local definition, notation, macro, alias, or instance. The exact root expression is bound in `statement-crosswalk.json`, and all three Lean surfaces carry the frozen source module and qualified declaration as non-executable provenance.

The structured census and dependency edges are in `machine-closure.json`. The machine cut set is empty and the proposed trust level is zero. The task-local run is deliberately `--no-lean`; therefore these are harvest candidates, not a claim of canonical acceptance. The Master must rebuild from source offline, re-elaborate the root, recompute every non-foundation provider binding, inspect axioms and bodies, run semantic-substitution mutations, and reject this package if any digest or dependency differs.
