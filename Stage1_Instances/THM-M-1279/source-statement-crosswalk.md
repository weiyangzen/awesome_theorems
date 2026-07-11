# Source-statement crosswalk

## Candidate primary source

William Beckner, "Sharp Sobolev inequalities on the sphere and the Moser-Trudinger inequality,"
*Annals of Mathematics*, Second Series 138 (1993), 213-242, is the primary candidate matching the
repository gloss and year. This bibliographic identification is discovery evidence only. A stable
scan must be inspected for the exact numbered theorem, page, hypotheses, notation, normalization,
and any journal errata before `H0` or exact-statement credit.

## Crosswalk

| Repository metadata | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "Beckner inequality" | named sharp inequality from the 1993 paper | one exact theorem, not a name-based surrogate | candidate family bounded |
| "higher-dimensional Moser-Trudinger inequality" | limiting/endpoint exponential inequality on a sphere | sphere, measure, exponential integral, and energy expression | included; formula open |
| proposed in 1993 | publication-year attribution | immutable edition metadata | candidate matches; page-level check open |
| "verified" | untrusted source label | kernel-checked declaration and accepted receipts | no credit |
| sharpness | optimal source constant and possibly extremizers | exact constant plus sharpness/equality clauses if in theorem | source inspection open |

## Source-to-formal boundary

The phrase alone does not determine a unique proposition: several Sobolev, logarithmic Sobolev,
and interpolation results are called Beckner inequalities. Consequently this intake freezes the
paper and theorem family, not a fabricated formula. The statement phase must transcribe a numbered
primary statement and separately map every domain, operator, normalization, hypothesis, conclusion,
and equality clause to Lean. A secondary exposition may explain notation but cannot replace the
primary anchor. No repo-local or upstream Lean candidate has yet been audited.
