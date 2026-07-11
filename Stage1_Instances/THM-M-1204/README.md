# THM-M-1204 rev-5.6 intake

This is a `planned` dossier for Kruzkov's theorem. The upstream phrase "entropy solutions of
multidimensional conservation laws" does not uniquely select a formal proposition. Accordingly,
the intake freezes the ambiguity rather than silently substituting a convenient uniqueness theorem.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Root | well-posedness of the scalar Cauchy problem `u_t + div f(u) = 0` on `R^d` | exact source theorem and hypotheses remain open |
| Definition | weak equation, all constant-level entropy inequalities, and initial trace | Lean encoding not selected |
| Existence | approximation, estimates, compactness, and limit identification | architecture only |
| Uniqueness | doubling of variables and comparison | architecture only |
| Stability | source-supported local/global `L1` estimate and consequences | exact estimate requires pinpoint audit |
| Foundations | measure theory, distributions, integration, function spaces | pinned imports and trust profile remain open |

The structured scope and open choices are in `intake.json`; the source-to-statement mapping is in
`source_statement_crosswalk.md`. The next phase must choose one exact primary-source claim before
elaborating Lean. Provisional vector: `[H1, M4, R3]`. The first failed theorem gate is exact-statement
identification. This dossier makes no theorem-completion claim.

## Validation

See `validation.md` for commands and results. These checks establish dossier syntax, manifest
membership, and repository consistency only.
