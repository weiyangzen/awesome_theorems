# Source-statement crosswalk

The current intake selects the classical coefficient-defined Shimura lift as a
theorem family, but it does not yet identify one exact primary result or one
reviewed composition as the root. That ambiguity is theorem-changing and is
therefore a statement blocker rather than a license to choose conventions.

| Component | Primary source surface | Intake surface | Exact statement status |
|---|---|---|---|
| Weight convention | Shimura 1973 uses an odd source weight parameter and an integral target weight one less | modern `k + 1/2` to `2k` wording | a checked parameter transport is missing |
| Level and character | Section 3 Main Theorem uses level divisible by four, a character modulo that level, a derived character, and a theorem-specific target level | level and character are named but not frozen | target level, conductor, and character transport are unresolved |
| Squarefree parameter | Main Theorem quantifies a positive squarefree parameter and defines a derived character and coefficients from it | each admissible squarefree parameter | admissibility and conductor interaction are unresolved |
| Coefficient normalization | Main Theorem defines the lift through a Dirichlet-series coefficient identity and a power-of-two Fourier normalization | Shimura's divisor-sum formula | the exact equality, indexing, and normalization have not been accepted |
| Cuspidality | Main Theorem separates its modular-form and cusp-form weight boundaries | cuspidal input gives a cuspidal lift | the low-weight boundary or a later refinement must be selected explicitly |
| Hecke content | Corollary 1.8 and Theorem 1.9 state coefficient/eigenvalue facts; the corollary after the Main Theorem composes earlier results | compatible with relevant Hecke operators | operator form, eigenform versus commutation claim, and prime restrictions are unresolved |

Primary identity: Goro Shimura, *On modular forms of half integral weight*,
Annals of Mathematics (2) 97 (1973), 440-481,
DOI `10.2307/1970831`. The locally inspected discovery scan has SHA-256
`78105f883d5a6646110de8a819d42d051f1f3a2ba221ac8cfb6ab8773bcc64f4`.
Those external bytes are not vendored or credited as accepted `H0` evidence.
Exact glyph review, lawful preservation, result selection or composition,
definition genealogy, corrections/errata disposition, and independent source
review remain open.

The historical `AwesomeTheorems.Stage1.S1_M_047.StatementShape` is excluded as
an exact encoding: theorem-critical transformation, cusp, coefficient, and
Hecke laws are stored as unconstrained propositions, while the squarefree
parameter and actual coefficient equality are absent. A bare nonempty ordinary
cusp-form target, including one inhabited by zero, is also excluded.

No exact canonical Lean proposition, alternate transport, statement
fingerprint, proof body, or theorem-completion credit is asserted here.
