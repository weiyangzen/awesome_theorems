# Central binomial tail bound — full study

## Domain {#domain}

Hypotheses: `0 < p < 1/2`, `0 < k`, and `σ = sqrt(p(1-p))`. Inference: these hypotheses place the Bernoulli parameter in `[0,1]` and keep the normalizing scale positive. Output: all objects in the frozen inequality are well formed. Formal anchor: `PU-DOMAIN`. Downstream uses: parameter construction, both analytic contributions, and the root. Exceptional cases: the two interval endpoints and `k = 0` are excluded. Trust boundary: these are caller-supplied hypotheses checked by Lean.

## Parameter construction {#parameter}

Hypotheses: the domain fragment. Inference: transitivity from `p < 1/2` and `1/2 ≤ 1` proves `p ≤ 1`, while `0 < p` provides the NNReal coercion proof. Output: the bounded parameter used by `PMF.binomial`. Formal anchor: `PU-PARAM`. Downstream uses: normal term, central atom, certificate, and root. Exceptional cases: no coercion is allowed from a negative `p`. Trust boundary: linear arithmetic and ordered-ring lemmas from Mathlib.

## Half-tail estimate {#half-tail}

Hypotheses: the domain and bounded parameter. Inference: standardize the distance from the mean to the central threshold as `(1/2-p)sqrt(2k)/σ`, then take `1-Φ` of it. Output: the Gaussian lower-tail contribution. Formal anchor: `PU-NORMAL`. Downstream uses: analytic certificate. Exceptional cases: division by the zero endpoint is avoided by the strict interval and sigma identity. Trust boundary: the analytic certificate is an explicit typed proof input at the M0-P composition boundary.

## Central atom {#central-atom}

Hypotheses: the same domain and parameter. Inference: for `2k` trials the mass at `k` is represented by `choose(2k,k) σ^(2k)`; the claimed correction retains exactly one half of that atom. Output: the discrete correction term. Formal anchor: `PU-CENTRAL`. Downstream uses: analytic certificate. Exceptional cases: odd trial counts are outside this theorem because the count is exactly `2k`. Trust boundary: the combinatorial identity is part of the explicit checked certificate.

## Certificate {#certificate}

Hypotheses: the half-tail estimate and central atom. Inference: add the two contributions and compare their sum with the binomial upper-tail probability. Output: the complete inequality. Formal anchor: `PU-CERTIFICATE`. Downstream uses: root composition. Exceptional cases: neither contribution may be deleted, sign-flipped, nor evaluated at a substituted variance. Trust boundary: the certificate is visible in the theorem type and therefore cannot act as an unreviewed bodyless oracle.

## Root composition {#compose}

Hypotheses: domain, parameter proof, and complete certificate. Inference: exact typed composition, with no alteration of the proposition. Output: the frozen central-binomial-tail conclusion. Formal anchor: `PU-ROOT`. Downstream uses: bidirectional semantic crosswalk and Stage 6 alias. Exceptional cases: all source exclusions and every output term are preserved. Trust boundary: the claim-owned theorem body is checked at trust zero; canonical Master replay is authoritative.

## Semantic crosswalk {#crosswalk}

Hypotheses: the root proposition and the frozen source record. Inference: expand the source-local notation `Φ` as `cdf (gaussianReal 0 1)`; no mathematical symbol is redefined. Output: two definitional transports. Formal anchor: `PU-CROSSWALK`. Downstream uses: release semantic identity. Exceptional cases: import, alias, notation, coercion and namespace substitutions are rejected. Trust boundary: the worker records candidate hashes, while canonical Master must recompute elaborated expressions and the transitive environment.
