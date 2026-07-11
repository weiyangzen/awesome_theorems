# Source-statement crosswalk

| Required claim component | Available source text | Intake result |
|---|---|---|
| Theorem identity | `变分法与PDE` | A field/topic, not a uniquely identifiable theorem |
| Claim text | `PDE的变分方法` | No truth-valued proposition is stated |
| Domain and unknown | absent | Cannot select scalar/vector-valued functions, domain regularity, or function space |
| PDE and boundary conditions | absent | Cannot distinguish elliptic, parabolic, hyperbolic, or other problems |
| Functional and variational relation | absent | Cannot state minimization, stationarity, weak formulation, or Euler-Lagrange equivalence |
| Hypotheses | absent | Coercivity, convexity, semicontinuity, growth, and regularity are all undecided |
| Conclusion | absent | Existence, uniqueness, regularity, and equivalence are materially different claims |
| Attribution/source | `众多数学家` (many mathematicians) | Not a citable theorem-bearing primary source |
| Historical status | `已验证` (verified) | Untrusted metadata and not evidence for any exact claim |
| Lean declaration | absent | No declaration can be matched without first inventing the statement |

The sole current source anchor is the repository's `Docs/Stage0_Blueprint.md` entry at base revision
`73a92b5e63e8eb3c93a5c95d5aead1658ca24c79`. That entry explicitly marks exact definitions,
premises, proof route, dependencies, axioms, and machine artifact as pending. It therefore cannot
support `H0`, exact-statement eligibility, or a source-to-Lean transport.

## Recovery requirement

An authoritative upstream record must provide a specific theorem statement or an unambiguous
theorem citation. Intake can then be revised to crosswalk each ordered binder, hypothesis, and
conclusion against a primary edition/page/theorem, including errata. Until then, adopting any
standard result in variational PDE would be a prohibited substitution rather than clarification.
