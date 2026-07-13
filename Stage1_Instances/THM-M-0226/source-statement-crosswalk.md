# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:1633-1638` supplies exactly the Chinese title "Schwarz lemma,"
Hermann Schwarz, 1869, the gloss "a holomorphic map from the unit disk to itself," high
importance, and status `已验证` ("verified"). All six uncited lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. There is no bibliographic work, edition, theorem or
page, formula, fixed-point premise, conclusion, proof boundary, errata, or formal artifact.

`Docs/Stage0_Blueprint.md:6275-6300` repeats the gloss while explicitly leaving precise definitions
and premises, proof route, dependencies, equivalents, axioms, machine status, and artifact links
open. The rev-5.6 manifest retains `已验证` only as `source_status_untrusted` and resets the target
to `L0 / rework_required`.

## Source status and discovery lead

The classical result is historically established, so the family is provisionally H1 rather than
an open problem. No source is admitted to H0. A modern secondary exposition inspected during
intake states the standard package: MathWorld, "Schwarz's Lemma," citing Steven G. Krantz,
*Handbook of Complex Variables*, section 5.5.1, page 78 (Birkhauser, 1999). Its retrieved HTML had
SHA-256 `9200b85b45eea6321b8d31f416c35d62b0d4fafb9e04c2bbf31ce5a30fddb8e8`.
It records an analytic unit-disk map, bound by one, fixing zero; both norm inequalities; and the
rotation equality case. This is an E5 discovery lead, not an accepted theorem source or H0 proof.

The catalog's historical data has a concrete primary-source lead: H. A. Schwarz, "Ueber einige
Abbildungsaufgaben," *Journal fuer die reine und angewandte Mathematik* 70 (1869), pages 105-120,
DOI `10.1515/crll.1869.70.105`. Crossref metadata had SHA-256
`b9653e50654b8b96664549ac88890e904c6985a90ef212b5ac12f3e58eff5030`; the Goettingen
Digitization Centre manifest had SHA-256
`01fcec858e85dd8120666a9723a55f9d5d19f63f720581b8a19795b6b8cfc313` and independently
identifies H. A. Schwarz as author. The lawfully accessed 17-page article scan had SHA-256
`907da8e8ce1ec6fe21ed5df1d8a712d4ba340851efd9bd3ef3c54c7e8dbd20f4`. A bounded
inspection shows that this article concerns conformal mapping problems, including disk/polygon
maps; it was not established to contain the modern normalized self-map lemma. It is a primary
historical lead only, not a pinpoint theorem/proof crosswalk.

The source phase must lawfully preserve an authoritative edition, inspect its exact theorem,
definitions, proof, corrections, and errata, decide whether all clauses form one root, and obtain
independent approval. The catalog's year and attribution now have a plausible primary publication
crosswalk, but the origin of the modern named lemma and its exact relationship to that article
remain unaudited.

## Clause crosswalk

| Repository/source-family component | Required mathematical decision | Prospective Lean component | Intake status |
|---|---|---|---|
| "unit disk" | open disk `D = {z : Complex | norm z < 1}` | `Metric.ball (0 : Complex) 1` | API checked; canonical representation open |
| "holomorphic" | complex differentiability/analyticity on all of `D` | `DifferentiableOn Complex f (Metric.ball 0 1)` | candidate encoding only |
| "to itself" | strict `f(D) subset D` versus non-strict `norm (f z) <= 1` | `Set.MapsTo f (ball 0 1) (ball 0 1)` or `closedBall 0 1` | source convention and direction open |
| fixed origin | `f(0)=0`, essential for the usual conclusion | equality hypothesis on a total function | absent from catalog gloss |
| pointwise conclusion | for every `z in D`, `norm (f z) <= norm z` | `Complex.norm_le_norm_of_mapsTo_ball` specialized to `Complex`, radius one | pinned candidate elaborates |
| derivative conclusion | `norm (f'(0)) <= 1` | `Complex.norm_deriv_le_one_of_mapsTo_ball` at center zero, radius one | pinned candidate elaborates |
| equality premise | equality at a nonzero point or derivative norm one | equality for `Complex.dslope` plus point membership | exact equivalence/wrapper open |
| rotation conclusion | some `a`, `norm a = 1`, and `f z = a*z` on `D` | affine `Set.EqOn` from `Complex.affine_of_mapsTo_ball_of_exists_norm_dslope_eq_div'` | candidate bridge only |
| `已验证` | untrusted inventory label | no proposition or proof object | explicitly rejected as evidence |

## Pinned formal provenance lead

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the candidates live in
`Mathlib/Analysis/Complex/Schwarz.lean`. The current generalized forms were introduced in mathlib
commit `60148e94959f3c8d21463b996fd16d4c37cb1a86` (2026-01-03, PR 33511); the file originated in
Lean 4 mathlib at `0c2078a5a9ce0c2828b4e71b3ac38009cbe3bc3e` and names Yury Kudryashov as author.
Pinned `docs/overview.yaml` maps "Schwarz lemma" to the deprecated alias of the pointwise theorem.

The intake probe checks exact current types for the pointwise, derivative, slope, and affine
equality candidates, and checks a prospective wrapper from a strict disk self-map to both usual
inequalities. Axiom reports for the principal candidates and wrapper are
`[propext, Classical.choice, Quot.sound]`. These facts justify only M3: no reviewed source root,
serialized canonical expression, checked equality-case transport, complete provenance/trust audit,
or accepted wrapper exists.

## First failed source gate

No immutable authoritative source theorem with a complete statement, incorporated definitions,
assumption/conclusion/proof mapping, errata disposition, and independent review has been accepted.
Freezing the familiar two-inequality statement or adding rigidity now would select mathematics not
specified by the repository gloss.
