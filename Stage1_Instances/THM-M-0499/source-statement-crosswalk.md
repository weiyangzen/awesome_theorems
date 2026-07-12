# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` attributes the result to Charles de la
Vallee Poussin, dates it to 1899, and gives the formula
`pi(x)-Li(x)=O(xe^(-c sqrt(ln x)))`. This is metadata-level discovery
provenance. It omits the quantifier on `c`, the limiting filter, definitions of
`pi` and `Li`, domains, endpoints, and a source locator. Its label `verified`
supplies no human-proof or machine-proof credit.

## Historical discovery anchor

Charles-Jean de la Vallee Poussin, *Sur la fonction zeta(s) de Riemann et le
nombre des nombres premiers inferieurs a une limite donnee*, Memoires couronnes
et autres memoires publies par l'Academie royale des sciences, des lettres et
des beaux-arts de Belgique, volume 59 (1899), is the primary historical
candidate for the theorem family. This dossier has not inspected and hashed an
immutable scan, selected an exact theorem/page/formula, mapped its notation and
premises, or completed an errata/correction search. It is therefore a discovery
anchor, not `H0` evidence.

## Crosswalk

| Repository component | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| `pi(x)` | number of primes at most `x` | `Nat.primeCounting`, plus a checked real extension if needed | pinned API located; extension open |
| `Li(x)` | logarithmic integral approximation | reviewed interval/principal-value integral definition | normalization and API open |
| `c` | an absolute positive constant | `Exists fun c : Real => 0 < c and ...` | positivity inferred from theorem family; source wording must confirm |
| `O(...)` | eventual constant-factor bound as `x -> infinity` | `Asymptotics.IsBigO Filter.atTop` or checked explicit-constant equivalent | API located; exact target open |
| `sqrt(ln x)` | square-root logarithmic decay scale | `Real.sqrt (Real.log x)` | APIs located; lower-domain handling open |
| `pi - Li` | signed error; Big-O controls its norm | real-valued function difference | included; coercions and discontinuities open |

## Fidelity boundary

The source phrase is specific enough to distinguish this result from the bare
prime number theorem, but not enough to freeze one formal proposition. A later
source audit must bind a stable edition or scan hash, pinpoint the displayed
formula and surrounding assumptions, determine the exact constant and
normalization conventions, check corrections, and obtain independent expert
review. Until then the human status is `H1`, not `H0`.

The intake's mathlib search and Lean probe locate statement ingredients only.
They do not establish that mathlib contains de la Vallee Poussin's theorem or
that any upstream formal proof exists.
