# THM-M-0387 release integration blocker

`S56-M-0387-RELEASE` remains blocked at `[H1, M2, R4]` with
`audit_complete=false` and `theorem_complete=false`. The mathematical cut is
`M0387-WTW`; validation is only `[_]`; H0/R0, trust, hermetic, supply-chain,
bundle, and independent-verifier gates remain open.

The immediate handoff blocker is scheduler-owned validator publication. The only
HEAD-declared release validator at worker base
`738c0e35f61cf22c1ab5e31a5cd0ad6432f12f01` is base blob
`05cd6cdd47b2e7a68053ce78b0e640852bf4eae3`; its stdout is legacy prose rather than
the required single `stage1-validator-semantic-result/1.0` object. A local repair
demonstrates the truthful typed negative result, but changes the validator candidate.
Current integration explicitly rejects worker validator changes, so a normal
self-test packet cannot be integrated.

The diagnostic repair was removed after confirming the typed negative result, so the
handoff leaves `check_release.py` byte-identical to its worker-base blob. The scheduler
must publish the typed validator itself and start a fresh claim whose worker-base blob
is identical. Until then, preserve this target-scoped blocker only; do not infer phase
acceptance or theorem completion from the local command result.

Only this blocker JSON/Markdown pair is retained in the owned delta. The diagnostic
receipt, specification, decision rewrite, ledger refresh, and narrative rewrite were
removed because a raw blocked claim cannot supply an integrable phase receipt and those
extra files would change the generated evidence inventory without closing the validator
publication gate.
