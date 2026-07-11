# Source-statement crosswalk

| Claim component | Located source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Entry identity | `Docs/researches/math_theorems.md`, entry "Hecke L-functions": Hecke, 1917, "L-functions of Hecke characters" | no exact declaration | Repository metadata only; it gives no bibliography, theorem number, hypotheses, or conclusion |
| General Hecke character | Same terse entry | legacy `HeckeCharacterDatum` in `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_079.lean` | Discovery model only: several essential conditions are opaque `Prop` fields |
| Associated L-function | Same terse entry | legacy `HeckeLFunctionBoundary` and `StatementShape` | Not source-faithful closure: agreement fields return `Prop`, and the package can be populated without proving agreement |
| Trivial-character specialization | Not asserted by the source entry | `NumberField.dedekindZeta` adjacent wrapper | Useful boundary probe, not a replacement for the general theorem |
| Rational/Dirichlet specialization | Not asserted by the source entry | mathlib Dirichlet L-series modules imported by the legacy file | Useful transport candidate only; no checked general-to-special bridge credited |
| Functional equation | Separate repository entry THM-M-0426 | none credited here | Explicitly excluded from this intake unless later primary-source evidence changes the partition |

The repository's `source_status_untrusted` value `已验证` is not human-source
evidence and gives no machine-proof credit. A primary-source audit must locate
an edition or scan, exact theorem/pages, definitions of the character and
L-series, convergence assumptions, normalization, and errata. It must then
decide whether the intended 1917 result is construction, convergence/Euler
product, analytic continuation, or a larger theorem package.

No `H0` claim is made. Until that ambiguity is resolved, there is deliberately
no canonical Lean expression. The exact-statement phase must also reject the
legacy boundary as a theorem substitute and mutation-test character domain,
conductor assumptions, bad-prime factors, convergence half-plane, and the
separation from THM-M-0426.
