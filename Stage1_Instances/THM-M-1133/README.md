# THM-M-1133 rev-5.6 intake

This is the `planned` dossier for the heat equation maximum principle. The Stage0 phrase
"maximum principle for solutions of the heat equation" is underspecified: it can denote weak,
strong, subsolution, or comparison forms. This intake selects the classical weak maximum principle
on a bounded finite-time cylinder. It does not silently claim any stronger form.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Root | A classical solution of `u_t - Delta u = 0` attains its cylinder maximum on the parabolic boundary | Exact Lean expression is open |
| Geometry | Bounded open `U` in finite-dimensional Euclidean space; finite `T > 0` | No unbounded-domain or manifold variant |
| Regularity | Continuity on the closed cylinder and classical `C2`-space/`C1`-time interior regularity | No weak or distributional solutions |
| Boundary | Initial face plus lateral boundary; terminal interior face is not parabolic boundary | Set encoding and compact-extremum API remain open |
| Sign convention | Forward heat operator `partial_t - Delta` | Opposite Laplacian conventions require checked transport |
| Related results | Inequality/subsolution and comparison forms are candidate generalizations | Strong maximum principle is excluded from the root |
| Foundations | Lean 4 kernel and pinned mathlib real analysis | Imports, axiom closure, and TCB fingerprint remain open |

The frozen prose claim, ordered assumptions, exclusions, and provisional formal domains live in
`intake.json`. `source_statement_crosswalk.md` records why the selected reading matches standard
PDE sources and which source checks remain outstanding.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. `H2` reflects a standard theorem
with identifiable textbook anchors but no accepted immutable page-level source receipt or errata
review. `M4` reflects that no exact Lean declaration has yet been identified or elaborated. The
first failed theorem gate is the exact-statement gate. No proof, anchor, audit, or theorem completion
is claimed.

## Open task DAG

1. `S56-M-1133-STATEMENT`: encode and elaborate the exact cylinder, parabolic boundary, regularity,
   heat operator, and maximum assertion; test domain, sign, boundary, and regularity mutations.
2. `S56-M-1133-ANCHOR_AUDIT`: pin source editions and search pinned mathlib/external Lean projects.
3. `S56-M-1133-OBLIGATION_TREE`: freeze proof, provenance, evidence, trust, documentation, and
   workflow graphs before proof credit is observed.
4. `S56-M-1133-PROOF`: implement or pin an exact proof without weakening the root.
5. `S56-M-1133-VALIDATION`: run kernel, trust, provenance, composition, and hermetic checks.
6. `S56-M-1133-RELEASE`: independently review receipts and decide audit/theorem completion.

## Validation boundary

The commands and results in `validation.md` establish manifest membership, rev-5.6 structural
consistency, JSON syntax, dossier-local references, and whitespace hygiene only.
