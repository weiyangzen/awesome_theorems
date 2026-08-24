# Machine-checked audit

The three claim-owned Lean files import `Mathlib`, preserve the frozen numeric
provider import and `Arxiv.«2602.05192».four_3` in provenance comments, and
prove the polynomial Cauchy core using `ring` plus `sq_nonneg` only. No
claim-specific oracle is present. `Audit.lean` includes `#print axioms` for the
root declaration.

This worker is forbidden to invoke Lean/Lake/Elan. Consequently the local
receipt records a successful semantic/evidence preflight only. `M0-P` is the
package's claimed proof level; canonical cold trust-zero compilation and the
exact elaborated-root/environment recomputation are explicitly pending Master
confirmation and are not represented as Master acceptance.
