# Source-statement crosswalk

## Repository source record

`Docs/Stage0_Blueprint.md` supplies only the label `Alinhac定理`, the gloss `非线性双曲型方程的奇性`,
the year 1986, and attribution to Serge Alinhac. It explicitly leaves the precise definitions,
hypotheses, proof route, equivalent formulations, axioms, and machine artifact unresolved. The
rev-5.6 manifest repeats the label/category and carries an untrusted `已验证` source status.

## Primary-source discovery leads

- Serge Alinhac's publications from or surrounding 1986 on blow-up/singularity formation for
  nonlinear hyperbolic equations must be searched by title and bibliography, then inspected in a
  stable scan or publisher edition.
- Serge Alinhac, *Blowup for Nonlinear Hyperbolic Equations*, Progress in Nonlinear Differential
  Equations and Their Applications 17, Birkhauser (1995), is a later authorial synthesis and a
  useful bibliography lead, but it is not accepted here as the unidentified 1986 primary theorem.

These are discovery leads only. No exact theorem/page or H0 evidence is claimed.

## Crosswalk

| Catalog field | Required source fact | Required Lean component | Intake status |
|---|---|---|---|
| "Alinhac theorem" | unique publication and theorem identifier | canonical declaration name and type | blocked by ambiguous eponym |
| nonlinear hyperbolic equation | exact PDE/operator and hyperbolicity regime | functions, derivatives, operator, solution predicate | open |
| singularity | precise blow-up or loss-of-regularity predicate | norm/derivative divergence or maximal-solution endpoint | open |
| 1986 | publication/announcement date and edition | provenance metadata only | unverified |
| `已验证` | primary proof and any formal artifact | pinned declaration and terminal proof body | untrusted; no credit |

The statement phase must reject every candidate that cannot explain every catalog field. Before H0,
an independent reviewer must verify edition, theorem/page, definitions, all hypotheses, conclusion,
errata, and the row-by-row source-to-Lean mapping.

## Existing Lean boundary

No repo-local file or pinned upstream declaration has been identified for this target at intake.
An anchor search belongs to the later anchor-audit node and cannot repair the missing source
identity by silently choosing a more formalization-friendly theorem.

