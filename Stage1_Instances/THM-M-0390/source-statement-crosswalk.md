# Source-statement crosswalk

## Primary source candidate

Preda Mihailescu, "Primary Cyclotomic Units and a Proof of Catalan's Conjecture", *Journal fur die
reine und angewandte Mathematik* **572** (2004), 167-195, DOI `10.1515/crll.2004.048` is the
primary proof publication identified for intake. Before H0, a reviewer must inspect a stable copy,
record the exact theorem label and page containing the formal statement, enumerate definitions and
assumptions used there, check errata, and independently approve this mapping. The bibliographic
record alone is discovery evidence, not an H0 receipt.

## Crosswalk

| Repository/source phrase | Provisional formal component | Disposition |
|---|---|---|
| "Catalan conjecture" | theorem historically conjectured by Eugene Catalan and proved by Mihailescu | identity only; no proof credit |
| "8 and 9 are the only consecutive powers" | all consecutive nontrivial positive perfect-power values are `(8,9)` | included, with "power" narrowed by four strict bounds |
| oriented source equation `x^p - y^q = 1` | after renaming, `x^p + 1 = y^q` | equivalence must be checked in Lean |
| unique solution `3^2 - 2^3 = 1` | tuple `(2,3,3,2)` for the plus-one orientation | included |
| source's positive-integer domain | `Nat` plus explicit `1 <` hypotheses | transport and boundary mutations remain open |

## Repository discovery boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_004.lean` proposes both a consecutive-pair shape
and an oriented equation shape, and kernel-checks only the exceptional witness and bounded cases.
It explicitly disclaims a proof of Mihailescu's theorem. It is useful for statement discovery but
receives no rev-5.6 statement, source, or proof credit. The untrusted manifest label `已验证` likewise
does not establish human-source fidelity or machine closure.
