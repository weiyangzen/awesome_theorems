# Proof outline

Fix `k ≥ 3`. Ramsey monotonicity gives the eventual lower bound

`1 ≤ R(k,l+1) / R(k,l)`.

The quantitative increment argument supplies constants `c>0` and `C≥0` such that, eventually,

`R(k,l+1) ≤ (1 + C l^(-c/k²)) R(k,l)`.

After division by the positive Ramsey number, the quotient is at most `1 + C l^(-c/k²)`. The exponent is negative, so the error tends to zero. Squeezing proves the fixed-`k` limit, and universal introduction discharges `k`. The detailed hypotheses, exceptional cases, anchors, uses, and trust boundaries occur exactly once in `full-study.md` and `proof-units.json`.
