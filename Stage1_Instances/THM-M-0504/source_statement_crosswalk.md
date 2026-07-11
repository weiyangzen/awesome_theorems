# Source-statement crosswalk

| Claim component | Repository source anchor | Candidate mathematical reading | Intake assessment |
|---|---|---|---|
| Title | Stage0: `黎曼假设的推论` | Consequences of RH | Broader than the theorem-content field |
| Theorem content | Stage0 and legacy Stage1: `黎曼假设的等价命题` | Some proposition `P` with `RH ↔ P` | `P` is absent, so this is not a uniquely formalizable claim |
| Status | Stage0 `已验证`; manifest calls it untrusted | Possibly a known proved equivalence | Discovery metadata only; it cannot establish H0 or M0 |
| Direct analytic reading | No repository pinpoint | Nontrivial zeta zeros have real part `1/2` | This is RH itself unless paired with a separately specified formulation |
| Robin reading | No repository pinpoint | A divisor-sum inequality equivalent to RH | Plausible candidate, not selected |
| Lagarias reading | No repository pinpoint | A harmonic-number/divisor-sum inequality equivalent to RH | Plausible candidate, not selected |

No primary mathematical source is cited by the target metadata. Consequently there is no honest
edition/theorem/page/assumption/errata crosswalk yet. The missing datum is not merely bibliographic:
it determines the domains, quantifiers, exceptional cases, and Lean APIs of the target.

Acceptance of a canonical statement requires one of the following: (1) a source pinpoint carrying
the literal intended equivalence, or (2) an explicit master decision naming the exact equivalence
and treating that decision as a scope correction. Until then, candidate formulas are excluded from
canonical status and there is no source-to-Lean mapping to credit.
