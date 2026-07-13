# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1408-1413` records:

- title: `欧拉线定理`;
- attribution: Leonhard Euler;
- year: 1767;
- gloss: `三角形垂心、重心、外心共线`;
- importance: high;
- untrusted formalization label: `已验证`.

Git blame places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record gives no publication, edition,
section, page, theorem number, original wording, definitions, formula, assumptions, proof,
correction history, reviewer, or formal source. The Stage0 projection explicitly marks the exact
definitions, premises, proof route, equivalent formulations, axioms, machine status, and artifact
links as open. These records establish catalog identity only.

## Primary-source lead

The University of the Pacific Euler Archive record for Enestrom E325 identifies Leonhard Euler,
*Solutio facilis problematum quorundam geometricorum difficillimorum*, *Novi Commentarii
academiae scientiarum Petropolitanae* 11 (1767), pages 103-123. The archive records that the work
was written in 1763 and published in 1767, so the catalog year is best treated as publication year,
not an unaudited claim about the first discovery date. Stable record:
`https://scholarlycommons.pacific.edu/euler-works/325/`.

The institutional primary scan was inspected. In the opening sections Euler distinguishes the
intersection of the altitudes, center of gravity, incenter, and circumcenter; later sections derive
relations among the relevant points that support a stronger order/ratio form of the Euler-line
result. The historical lettering is not the modern `H`, `G`, `O` notation and must be translated
carefully. The archive HTML observed during intake had SHA-256
`365eafbc7a489c2c840659cd10dee0b6779e8c81812838feb89a656e09e8147e`. PDF bytes were inspected
visually, but unstable partial HTTP responses prevented a reproducible immutable PDF hash; no PDF
digest is admitted.

These remote observations are strong primary-source discovery evidence, not an admitted immutable
H0 packet. The complete Latin definition chain, exact theorem and proof boundaries, page/section
transcription, assumptions, modern notation and ratio translation, corrections or errata, and
independent source review remain open.

## Human-source status

The matching primary work and relevant center/ratio passages make the provisional human axis `H1`,
not `H4` or `H5`. It is not `H0`: the primary edition has not been admitted as content-addressed
repository evidence, the exact Latin statement and proof have not been completely transcribed and
mapped, no correction audit exists, and no independent source reviewer has approved the mapping.

| Repository element | Mathematical information plausibly indicated | Missing source decision | Intake result |
|---|---|---|---|
| `三角形` | a Euclidean triangle | ordered versus unordered vertices, nondegeneracy, ambient dimension | open |
| `垂心` | intersection of the altitudes | altitude definition, existence/uniqueness, exterior cases | candidate mathlib definition only |
| `重心` | equal-weight affine centroid | affine versus coordinate definition | candidate mathlib definition only |
| `外心` | center of a circumscribed circle | construction, existence/uniqueness, affine-span convention | candidate mathlib definition only |
| `共线` | the three centers lie on one line | rank, affine-span membership, existential parameter, order/ratio | canonical encoding open |
| Euler / 1767 | matching E325 publication year | written 1763; exact historical statement, section/line transcription, and proof provenance still need review | primary lead only |
| `已验证` | inventory label | accepted human or kernel evidence | no credit |

## Formal-source crosswalk

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies a direct
exact-topic source in `Mathlib.Geometry.Euclidean.MongePoint`. Its module documentation says the
circumcenter `O`, centroid `G`, and Monge point `M` are collinear in that order on the Euler line,
with `OG : GM = (n - 1) : 2`; it then specializes the Monge point to the triangle orthocenter.
This is formal-library documentation and candidate code provenance, not the missing human-source
H0 record.

| Catalog component | Pinned declaration or definition | Relationship | Credit boundary |
|---|---|---|---|
| nondegenerate triangle | `Affine.Triangle` / `Affine.Simplex` | three affinely independent points indexed by `Fin 3` | candidate representation; source transport open |
| centroid | `Affine.Simplex.centroid` | equal-weight affine centroid | candidate definition; exact source identity open |
| circumcenter | `Affine.Simplex.circumcenter` | circumsphere center in the simplex affine span | candidate definition; source convention open |
| orthocenter | `Affine.Triangle.orthocenter` | defined as the two-dimensional Monge point | supported by altitude theorems; source definition mapping open |
| altitude characterization | `Affine.Triangle.orthocenter_mem_altitude` | orthocenter lies in every altitude | adjacent semantic interface only |
| Euler position | `Affine.Triangle.orthocenter_eq_smul_vsub_vadd_circumcenter` | `H = 3 • (G - O) + O` | stronger candidate bridge; no root or proof credit at intake |
| collinearity | `Collinear` | rank of the vector span is at most one | plausible conclusion encoding; not frozen |

`IntakeProbe.lean` checks these declarations and prints axiom diagnostics for two supporting
theorems. It creates no declaration. Successful elaboration establishes only that the candidate
interfaces exist in the pinned environment.

## Candidate future statement crosswalk

The following candidate is intentionally not canonical:

```text
For every affinely independent triangle t in a real Euclidean affine space,
the set {t.orthocenter, t.centroid, t.circumcenter} is collinear.
```

It preserves the catalog's bare collinearity conclusion and makes nondegeneracy explicit through
the triangle type. It may nevertheless differ from the intended source in ambient dimension,
triangle representation, center definitions, and inclusion or omission of the Euler ratio/order.
The statement phase must decide and check those relationships rather than inferring identity from
a familiar theorem name.

## H0 and downstream gates

Before H0, reviewers must admit a versioned primary proof source, locate the exact theorem and all
incorporated definitions, map every hypothesis and material proof transition to the chosen root,
resolve translation and historical-date questions, audit corrections and errata, and independently
approve the crosswalk. Before statement acceptance, Lean work must freeze exact binders and minimal
imports, preserve an elaborated expression and environment fingerprint, compile checked alternate-
form transports, and pass all semantic mutations. Proof-body provenance and exact trust closure
belong to the later anchor-audit and proof phases.
