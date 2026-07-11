# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Integral equation of the second kind | I. Fredholm, *Sur une classe d'equations fonctionnelles*, Acta Mathematica 27 (1903), 365-390 | A future integral-operator definition | Primary historical source candidate identified; exact page/formula and assumptions need scan-level audit |
| Homogeneous versus inhomogeneous solvability alternative | Same paper; exact numbered result and translation pending | `Mathlib.Analysis.Normed.Operator.FredholmAlternative` | Operator-level candidate only; declaration/type audit belongs to the anchor phase |
| Compactness bridge from kernel to operator | Modern compact-operator reconstruction of Fredholm's kernel setting; primary modern source not yet selected | mathlib integral and compact-operator APIs | Required checked bridge, not present evidence |
| Adjoint compatibility condition | Historical/modern Fredholm alternative; convention and pairing depend on chosen function space | future adjoint/range orthogonality statement | Mandatory branch; omitting it would narrow the theorem |
| Potential-theory application | Repository source row, `Docs/researches/math_theorems.md`, lines 8499-8504 | no candidate | Metadata provenance only; too vague for H0 or an exact Lean target |

The title alone can mean an equation, the Fredholm alternative, a determinant/resolvent method, or
an application to potential theory. This dossier chooses the classical second-kind alternative
because it yields a theorem rather than merely an object, but retains the integral-kernel
specialization as essential scope. An abstract compact-operator eigenvalue/resolvent theorem alone
must not be substituted for the requested integral-equation result.

No H0 claim is made. The source audit must obtain an immutable scan, record exact formula and page
anchors, reconcile sign and parameter conventions, identify all continuity/integrability and
domain assumptions, inspect corrections/errata, and obtain independent review.
