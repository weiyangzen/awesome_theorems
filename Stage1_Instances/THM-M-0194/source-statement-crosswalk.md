# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:1401-1406` records only:

- title: `泰勒斯定理`;
- attribution: Thales of Miletus;
- date: approximately 600 BCE;
- gloss: `圆周角等于圆心角的一半`;
- importance: high;
- untrusted formalization label: `已验证`.

Those lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:5401-5426`
repeats them while leaving exact definitions, premises, proof route, equivalent forms, axioms,
machine status, and artifact links open. The records establish catalogue identity only.

## Human-source lead

Euclid, *Elements*, Book III, Proposition 20 is a matching proposition-level lead. David E. Joyce's
1996 web edition, "Euclid's Elements, Book III, Proposition 20," was retrieved from
`https://mathcs.clarku.edu/~djoyce/java/elements/bookIII/propIII20.html` for bounded inspection on
2026-07-13. The observed 3,343-byte HTML had SHA-256
`da95719836c9460d640343db776cea2f893411e3f582544b668829158208dfe2`.

Its statement reads: "In a circle the angle at the center is double the angle at the circumference
when the angles have the same circumference as base." The construction names a circle `ABC`, its
center `E`, central angle `BEC`, circumference angle `BAC`, and their common circumference `BC`.
The displayed proof then treats two diagrammatic configurations using equal-radius isosceles
triangles and exterior-angle arithmetic.

This is a stable matching locator, not H0 evidence. The inspected web edition is a modern English
edition rather than an independently reviewed primary-language artifact. Intake has not audited
the edition and translation history, Euclidean definitions of angle and "same circumference as
base," every diagram-dependent case, attribution to Thales, later corrections, or errata. A source
reviewer has not signed the crosswalk.

## Clause crosswalk

| Repository or source phrase | Information fixed | Pinned Lean candidate | Intake decision |
|---|---|---|---|
| "in a circle" | a common circle is intended | `hp1`, `hp2`, and `hp3` assert membership in one `Sphere P` | candidate only; dimension, radius, and degeneracies remain open |
| "angle at the center" | apex is the circle center | `oangle p1 s.center p3` | candidate uses an oriented angle class, not an ordinary representative |
| "angle at the circumference" | apex lies on the circle | `oangle p1 p2 p3` with `hp2` | candidate only; endpoint distinctness and arc convention need review |
| "same circumference as base" | both angles subtend endpoints `p1`, `p3` | both candidate angles share those endpoints | close structural match; exact arc/side semantics are not yet transported |
| "double" / catalogue "half" | central-to-inscribed factor two relation | equality with `(2 : Int) •` in `Real.Angle` | direction matches after rewriting prose, but division by two is not credited as an inverse transport |
| Thales' theorem | historical catalogue name | mathlib's alias names the semicircle/right-angle theorem | name collision; the alias is not the catalogue root |
| `已验证` | secondary inventory metadata | no proposition or kernel receipt | no H or M credit |

## Formal candidate crosswalk

The intake probe elaborates these declarations at the pinned mathlib revision:

| Declaration | Candidate role | Unclosed gate |
|---|---|---|
| `Orientation.oangle_eq_two_zsmul_oangle_sub_of_norm_eq` | vector form using equal norms | affine/source transport and exact target selection |
| `Orientation.oangle_eq_two_zsmul_oangle_sub_of_norm_eq_real` | vector form with explicit radius | same, plus radius and origin conventions |
| `Sphere.oangle_center_eq_two_zsmul_oangle` | closest general inscribed-angle theorem | source identity, angle/arc semantics, expression fingerprint, provenance and trust audit |
| `Sphere.angle_eq_pi_div_two_iff_mem_sphere_of_isDiameter` | semicircle/right-angle theorem | distinct result; prohibited as a silent substitute |
| `Sphere.angle_eq_pi_div_two_iff_mem_sphere_ofDiameter` | canonical diameter-sphere specialization | distinct result; prohibited as a silent substitute |
| `Sphere.thales_theorem` | alias of the is-diameter semicircle theorem | theorem-name match supplies no statement identity |

The probe's diagnostic axiom reports for both the exact-topic and named candidates are
`[propext, Classical.choice, Quot.sound]`. This only describes the probed pinned declarations. It
does not select a foundation profile for an unfrozen root or award proof credit.

Before leaving H1, an accountable source reviewer must admit an immutable edition, pinpoint and
transcribe the exact proposition and incorporated definitions, map every premise and case, audit
corrections/errata and attribution, and approve the source-to-catalogue boundary. Before statement
acceptance, Lean work must freeze a minimal import and elaborated expression, compile any claimed
transport, and pass the required statement mutations.
