# Source-statement crosswalk

| Claim component | Repository anchor | Primary-source status | Intake assessment |
|---|---|---|---|
| Name | `张寿武-萨纳克定理` | No title, journal, DOI, theorem number, or page supplied | Not enough to identify a theorem |
| Attributed authors | Shou-Wu Zhang / Peter Sarnak | A joint source has not been established by the supplied evidence | Attribution requires verification |
| Date | 1999 | No edition or publication record supplied | Discovery datum only |
| Content | `博戈莫洛夫猜想的证明` | “Bogomolov conjecture” has multiple formulations and needs ambient data and an exact conclusion | Not a formalizable statement as written |
| Formal status | `已验证` | No proof-assistant project, immutable revision, module, or declaration supplied | Untrusted metadata; no machine credit |

The repo-local provenance chain is
`Docs/researches/math_theorems.md` -> `Docs/Stage0_Blueprint.md` ->
`Docs/Stage1_Targets_rev-5.6.json`. It preserves the same short description but adds no primary
source detail. Consequently, there is no truthful mapping yet from a source theorem to Lean
binders, hypotheses, or conclusion.

## Resolution required before statement work

1. Identify the intended primary publication and immutable edition, including title, venue, year,
   theorem/page, and any errata.
2. Determine whether Peter Sarnak is genuinely a coauthor/source for this named result or whether
   the metadata conflates a different theorem.
3. Freeze the exact Bogomolov formulation: base field, abelian variety, polarization and height,
   subvariety assumptions, definition of special/torsion locus, and lower-bound or density
   conclusion.
4. Crosswalk every source assumption to ordered Lean binders and record boundary cases.

Until those questions are resolved, nearby results by Zhang, Ullmo, or others are search leads only.
Using one of them as the target would be a broadened or substituted theorem. Human status remains
`H4`; exact Lean-statement status remains `M4`. No primary-source, formal-proof, or theorem-completion
claim is made.
