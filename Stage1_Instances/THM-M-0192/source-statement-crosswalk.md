# Source-statement crosswalk

## Primary-source anchor

Pierre Deligne, "La conjecture de Weil. I," *Publications Mathematiques de l'IHES* **43**
(1974), 273-307, DOI `10.1007/BF02684373`. The candidate exact root is the numbered smooth,
projective Frobenius-eigenvalue theorem customarily cited as Theorem 1.6. An immutable scan must be
inspected before statement freeze to verify the numbering, original French wording, notation,
quantifiers, Frobenius convention, and any corrections.

This bibliographic identification is discovery evidence, not an accepted `H0` crosswalk, a source
snapshot, or machine-proof evidence. The historical phrase "proof of the Weil conjectures" must be
read together with the division of responsibility: Deligne's result supplies the remaining
Riemann-hypothesis/weight assertion, while rationality and cohomological/functional-equation
infrastructure have separate antecedent sources.

## Crosswalk

| Repository/source phrase | Intake interpretation | Required Lean-side object or proposition | Status |
|---|---|---|---|
| "Deligne theorem" | Deligne's 1974 Weil I smooth-projective weight theorem | one canonical root with source-identical binders and hypotheses | included; exact transcription open |
| "proof of the Weil conjectures" | completion via the remaining Riemann-hypothesis component | explicit status boundary against the full package | included as historical role, not four duplicate roots |
| variety over a finite field | smooth projective source object over `F_q` | scheme/variety, structure morphism, smoothness, projectivity | encoding and edge cases open |
| degree `i` cohomology | l-adic etale cohomology in degree `i` | coefficient system, finite-dimensional space, Frobenius action | APIs/imports open |
| Frobenius eigenvalue | eigenvalue of the source's chosen Frobenius convention | endomorphism, characteristic polynomial/eigenvalue predicate | arithmetic/geometric convention open |
| weight `i` | algebraicity plus complex absolute value `q^(i/2)` | algebraic-number embedding and real absolute-value equality | exact embedding quantifier open |
| zeta-function RH | reciprocal-root reformulation of the cohomological weight assertion | checked transport through trace/factorization results | alternate form only; transport not yet available |

## Metadata and machine boundary

Stage0 provides only the title, gloss, year 1974, Pierre Deligne's name, and an untrusted `已验证`
label. It provides no formal hypotheses or theorem number. Repository search found no legacy slot
or accepted target-specific Lean declaration for `THM-M-0192`; adjacent dossiers and generic
Deligne mentions are not proof credit. No Lean module, external formalization, proof body, or axiom
closure is credited at intake.

Before `H0`, an independent reviewer must approve a row-by-row source transcription including
assumptions, notation, theorem dependencies, and errata. Before any machine claim, the exact Lean
expression and all claimed alternate forms must elaborate under the pinned environment.
