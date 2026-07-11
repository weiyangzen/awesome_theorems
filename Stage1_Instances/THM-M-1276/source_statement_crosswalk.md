# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Critical Sobolev embedding into an Orlicz class | N. S. Trudinger, *On imbeddings into Orlicz spaces and some applications*, Journal of Mathematics and Mechanics **17** (1967), 473-483 | No repo-local declaration identified at intake | Primary mathematical source identified bibliographically, but exact theorem number, scan hash, hypotheses, and errata are not yet audited (`H2`) |
| Exponential growth `exp(alpha |u|^(n/(n-1)))` | Modern integral presentation of the critical Orlicz embedding; must be checked against Trudinger's Young-function notation | Planned measure integral over a Euclidean domain | Mathematical correspondence is plausible, not yet a reviewed source-to-statement equivalence |
| Zero-boundary normalization and gradient-energy bound | Standard `W_0^{1,n}` specialization using Poincare control | Planned zero-trace Sobolev membership plus weak-gradient integral | Exact domain and norm conventions remain unresolved; no transport is credited |
| Sharp endpoint coefficient | Later sharp refinement associated with Moser and represented separately by `THM-M-1277` | Out of scope | This target asserts existence of some positive coefficient, not sharpness or optimal failure |

The repository's Stage0 record contributes only the Chinese title `Trudinger不等式`, the gloss
`临界Sobolev嵌入`, the year 1967, and attribution to Neil Trudinger. Its label `已验证` is explicitly
untrusted under rev-5.6 and supplies neither human-source nor machine-proof credit.

Before the statement gate, the source audit must acquire an immutable copy of the 1967 paper and
record its hash, exact theorem/page, definitions of the domain and Orlicz function, all premises,
and any corrections. It must then either justify the selected integral form in both directions or
revise the planned root transparently before freezing a Lean expression. In particular, it may not
replace weak Sobolev functions by smooth compactly supported functions without a checked density
argument.

No `H0`, Lean anchor, or theorem completion is claimed.
