# THM-M-1303 rev-5.6 intake

This directory is the `planned` intake for the catalogue target "paraproduct" (`仿积`). The only
repository statement is "paraproduct decomposition of functions". It does not specify a domain,
dyadic resolution, function spaces, convergence mode, or even whether the intended result is the
decomposition identity or a continuity estimate. Intake preserves that ambiguity rather than
inventing a theorem.

## Scope map

| Surface | Candidate scope | Intake boundary |
|---|---|---|
| Root selection | one precisely cited paraproduct decomposition theorem | exact source result remains unselected |
| Inputs | functions or distributions and a dyadic resolution | domain, scalar field, and regularities are open |
| Operators | low-high and high-low paraproducts, possibly a resonant term | definitions and normalization are open |
| Equality | recomposition of a product in a stated topology | convergence and product-definedness hypotheses are open |
| Estimates | Holder/Besov mapping bounds | a distinct theorem family, not silently included |
| Lean | a minimal pinned Lean 4 expression | no declaration is selected or credited |

The structured scope is in `intake.json`; `source-statement-crosswalk.md` separates the catalogue
wording, primary discovery anchor, neighboring duplicate-like target, and possible formal target.
`task-dag.json` keeps every later phase open.

## Intake verdict

Lifecycle is `planned` and the provisional root vector is `[H2, M4, R3]`. The first failed gate is
exact statement identification. The historical `已验证` label is untrusted metadata, and neither
the neighboring `THM-M-1301` dossier nor an abstract paraproduct field supplies proof credit.
The theorem is not complete.

