# Machine-checked audit

- Root: `AwesomeTheorems.Stage5.S5_CLM_00003514.claim_owned_four`
- Closure: `M0-L`, trust `0`, observed axiom set empty
- Semantic environment: `0c178d564752ce7e0ae6626000b8f0d1d954ee919ad2f252a4438b0d105efdb3`
- Root expression: `2f16739e0c86185b7fe1b816a38a68ad706c9e72381fb5fb8089cf0bbda63c8c`
- Source provider body: explicitly excluded as proof authority because its frozen declaration uses `sorryAx`
- Replay: cold-from-source recorded; independent canonical Master replay still required

`machine-closure.json` is the authoritative declaration and dependency census. `Audit.lean` supplies independent forward, reverse, and round-trip transport checks.
