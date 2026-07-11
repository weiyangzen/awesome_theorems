# Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Repository claim | a 1979 modular-forms identity attributed to Goro Shimura and labelled "quintuple product" | The metadata supplies neither a formula nor a bibliographic anchor |
| Mathematical objects | modular forms and a product with five factors or terms, if confirmed by the source | Group, weight, level, character, coefficient ring, and operands are unknown |
| Equality regime | analytic functions, q-expansions, formal power series, or sections, as selected by the source | No regime may be silently selected; convergence and equality principles differ |
| Product conventions | finite/infinite product indexing and normalization of `q` | Index set, exponents, domain, convergence, and boundary values are unknown |
| Root conclusion | the exact equality printed in the identified source | A generic product identity or coefficient coincidence is not an acceptable replacement |
| Lean surface | minimal pinned mathlib imports after source selection | No declaration or expression is frozen at intake |
| Foundations | Lean 4 kernel plus an audited classical/choice/quotient and analytic-computation profile | Exact profile depends on the eventual statement |

The dossier explicitly excludes silently choosing the commonly named classical quintuple product
identity, because the repository gives no evidence that this is the intended Shimura-attributed
1979 theorem. It also excludes Shimura lifting, reciprocity, correspondence, and variety results.

Once the source is identified, statement work must transcribe the exact formula, ordered parameters,
modularity assumptions, analytic domain, normalizations, convergence conditions, and exceptional
cases. Only then can it decide whether analytic-function equality and q-expansion/formal-series
equality are alternate encodings and supply checked transports between them.
