# Source-statement crosswalk

| Claim component | Human source anchor | Lean target surface | Intake assessment |
|---|---|---|---|
| Probability-form root | S. Bochner, *Monotone Funktionen, Stieltjessche Integrale und harmonische Analyse*, Mathematische Annalen 108 (1933), 378-410, DOI 10.1007/BF01452844 | an existential equivalence for `phi : Real -> Complex` and a Borel probability measure | Primary historical source identified, but exact Satz/page boundaries, assumptions, and corrections are not yet audited; `H1` only |
| Positive definiteness | Finite quadratic-form condition in the classical theorem | a predicate quantified over every finite family of real points and complex coefficients | Predicate spelling, conjugation order, and proof of real/nonnegative output must be fixed by the statement phase |
| Normalization | `phi(0)=1`, corresponding to total measure one | probability-measure typeclass or explicit `μ univ = 1` | Both encodings are candidates; no transport is checked |
| Continuity | Continuity of the characteristic function | `Continuous phi`; continuity-at-zero is an alternate encoding | Global continuity is canonical here; equivalence transport remains open |
| Representation | `phi(t) = integral x, exp(i*t*x) dμ` | mathlib Fourier/characteristic-function APIs, if suitable, otherwise an explicit integral | API and transform convention have not been selected or elaborated |
| Converse | Fourier transform of a probability measure satisfies the three conditions | reverse implication of the same root | Included in the root, not independently credited |
| Uniqueness | Uniqueness theorem for characteristic functions | separate future theorem/bridge | Explicitly excluded from this target to avoid broadening Bochner existence/characterization |

The repository source synopsis says only “正定函数的特征” (characterization of
positive-definite functions). The canonical scope above resolves that ambiguity
to the probability/characteristic-function form, consistent with the target's
probability-theory category and its neighboring characteristic-function items.
This resolution must be rejected rather than silently changed if the source
audit identifies a different intended Bochner theorem.

Discovery references, not accepted evidence receipts:

- Historical paper: <https://doi.org/10.1007/BF01452844>
- Repository synopsis: `Docs/researches/math_theorems.md`, Bochner theorem entry

No `H0` or machine-closure claim is made. Follow-up must obtain an immutable
source copy/hash, locate exact statement pages, map every premise, inspect
errata and translation issues, independently review the mapping, and inspect
the pinned mathlib environment before choosing a Lean declaration.
