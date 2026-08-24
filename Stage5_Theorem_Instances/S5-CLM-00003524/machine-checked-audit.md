# Machine-checked audit

The intended root is
`AwesomeTheorems.Stage5.S5_CLM_00003524.audit_root`, at machine level M0-W.
The declaration census, dependency edges, empty observed-axiom list, empty
machine cut set, semantic-environment binding, and trust level are recorded in
`machine-closure.json`.

The task-local validator is deliberately run with `--no-lean`.  Consequently,
this worker records only the required semantic/evidence preflight.  The
canonical Master must independently elaborate Statement, Proof, and Audit from
source with trust zero, recompute all expression/type/body/dependency/axiom
hashes, and reject this candidate if any provisional digest or declaration
differs.
