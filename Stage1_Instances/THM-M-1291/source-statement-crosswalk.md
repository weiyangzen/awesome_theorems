# Source-statement crosswalk

## Primary source

Haim Brezis and Elliott Lieb, "A Relation Between Pointwise Convergence of
Functions and Convergence of Functionals," *Proceedings of the American
Mathematical Society* **88** (1983), no. 3, 486-490, Theorem 1.
DOI: <https://doi.org/10.1090/S0002-9939-1983-0699419-3>.

This is a primary discovery anchor, not `H0`: the intake has not archived and
hashed a stable copy, checked every symbol against the printed theorem, searched
errata, or obtained independent review.

| Source component | Frozen repository meaning | Lean obligation for next phase |
|---|---|---|
| `0 < p < infinity` | every finite positive real exponent | encode `0 < p`; do not impose `1 <= p` |
| sequence converges a.e. | `f_n x -> f x` outside a null set | choose an `ae` filter statement and mutation-test it |
| uniformly bounded `p`-power integrals | one finite bound applies to all `n` | select `integral`/`lintegral` encoding without adding domination |
| remainder `f_n - f` | pointwise scalar subtraction | check scalar norm and measurability obligations |
| limiting identity | difference of integrals tends to the limit's integral | elaborate exact filter limit and coercions |

The repository gloss `弱收敛与强收敛的余项` is not sufficiently precise and
can misleadingly suggest weak convergence as the main premise. The primary
theorem's almost-everywhere convergence and uniform `L^p`-power bound govern
this dossier. No mathlib or external Lean declaration is credited during
intake; anchor discovery belongs to the dependent anchor-audit phase.

