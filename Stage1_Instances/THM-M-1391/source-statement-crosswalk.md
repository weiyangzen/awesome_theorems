# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10132-10137` supplies exactly the title `Prufer变换`, attribution
to Heinz Pruefer, date 1926, gloss `Sturm-Liouville问题的相位分析` ("phase analysis of
Sturm-Liouville problems"), importance "high," and status `已验证`. The complete six-line block has
SHA-256 `779ee22f53ab010e61ea8181ec3ffdce38f3f185ae3bd0d87555b44f78f90af3`.
All six lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; they contain no citation or proposition.

`Docs/Stage0_Blueprint.md:37830-37855` repeats the gloss and explicitly leaves the background,
definitions and premises, proof route, dependencies, equivalent forms, axioms, machine status, and
artifact links open. Its generic tree and 100-step language is planning boilerplate, not
mathematical source evidence. The rev-5.6 manifest carries `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `Prufer变换` | amplitude-angle change of variables for a nontrivial ODE solution | exact state pair, amplitude, phase/lift, convention, existence and uniqueness claim | a named construction, not a proposition |
| Sturm-Liouville problem | a parameterized second-order equation plus interval and boundary data | coefficient functions, regularity/sign structures, solution and endpoint predicates | all open |
| phase analysis | phase equation, zero crossings, monotonicity, comparison, oscillation, or spectral conclusions | exactly one source-selected `Prop` and any checked consequences | no conclusion selected |
| Heinz Pruefer / 1926 | likely historical provenance | immutable edition and theorem/equation/page mapping | a strong source lead exists; catalog gives no locator |
| `已验证` | untrusted inventory metadata | accepted human-source and Lean kernel receipts would be required | no H or M credit |

## Inspected historical source

Heinz Pruefer, "Neue Herleitung der Sturm-Liouvilleschen Reihenentwicklung stetiger Funktionen,"
*Mathematische Annalen* 95(1), 499-518 (1926), DOI `10.1007/BF01206624`, is a credible primary
historical source. Crossref and Springer metadata agree on author, title, journal, volume, pages,
and December 1926 publication. The Goettingen Digitalisation Centre provides a 21-page scan under
volume `PPN235181684_0095`, article range `LOG_0033`; the downloaded PDF observed on 2026-07-13 has
SHA-256 `d452d9b2eb170c0505030457dbdec688bf2c739262ec2747bb4af6eb821b2f67`.

The scan makes the family and its ambiguity concrete:

| Source locator | Inspected source component | Prospective target component | Intake disposition |
|---|---|---|---|
| Section 1, p. 499 | equation `(k u')' + (l + lambda r) u = 0` on `[a,b]`, boundary ratios, and `k > 0`, `r > 0` in the main regular case | system, coefficient, interval, parameter and endpoint binders | source context only |
| Section 2, p. 502 | an oscillation theorem asserting a growing sequence of parameter values, corresponding solutions, and exact interior zero counts | possible spectral/oscillation root | materially larger than a transformation theorem |
| Section 2, p. 503 | first-order state `u' = v/k`, `v' = -(l + lambda r)u`; polar coordinates `v = rho cos theta`, `u = rho sin theta`; differential equations for `rho` and `theta` | forward Pruefer transform and phase equation | strongest transform passage, but not selected by the catalog |
| Section 2, pp. 503-504 | nonvanishing amplitude for a nontrivial solution, equivalence language, endpoint phase conditions, and phase crossing at zeros | lift, reconstruction/equivalence and zero-phase crosswalk | exact hypotheses and claim boundary still require translation/review |
| Section 2, pp. 504-505 | phase dependence on `lambda`, zero count, monotonic ordering, and limiting endpoint phase | oscillation/eigenvalue application | distinct consequence, not automatically part of the root |
| Sections 3-5, pp. 505-518 | interpolation, closure, and convergence arguments for the expansion theorem | larger paper architecture | outside a narrow transform root unless explicitly selected |

The scan was inspected for intake discrimination only. No complete German transcription or
translation, independent source review, errata/correction audit, incorporated-definition map,
proof-node crosswalk, or catalog decision selects one row as the canonical root. The scan is not
vendored in this dossier. It therefore supports source discovery but not `H0` or an exact statement.

## Modern formulation discriminator

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, American Mathematical Society (2012), DOI `10.1090/gsm/140`, supplies a modern
source-family discriminator. Section 5.3, equations (5.43)-(5.45), p. 153 fixes the regular
Sturm-Liouville setup and coefficient assumptions; Section 5.5, pp. 166-168 gives the transform.
The author's preliminary edition is made available with the
publisher's permission; the observed PDF has SHA-256
`362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e`. Equations (5.81)-(5.86)
use the regular operator `L = r^-1 (-(p u')' + q u)`, set
`u = rho sin theta` and `p u' = rho cos theta`, exclude the trivial real solution, choose a
continuous lift of the phase, and state equivalence with the amplitude/phase system. Lemma 5.14,
equation (5.88), is a separate zero-counting consequence.

The observed errata PDF has SHA-256
`3eacbac5b8fc762c5d3f21183cba3ae638b9ac5fbe703cc52cf2857b9605996e`; it corrects typography in
equation (5.87), not (5.81)-(5.86). Teschl also gives a scaled modified transform in
equations (5.102)-(5.106), pp. 172-173. These variations confirm that normalization, phase, and
root selection are proposition-changing. This modern exposition is not a primary 1926 source and
is not adopted or credited as the catalog's canonical statement.

## Source gate

The provisional human classification is `H5` because the received repository wording is a method
label plus purpose gloss, not a stable truth-valued proposition. This does not refute the inspected
paper or modern Pruefer theorems. Before ordinary proof execution, an accountable owner must approve
a corrected exact root, preserve one lawful immutable source, delimit the selected result and all
incorporated definitions, transcribe and translate its ordered binders, hypotheses, conclusion and
exceptional cases, inspect its proof and corrections or errata, and obtain independent approval of
the source-to-canonical-statement mapping.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
elaborates `IsIntegralCurve`, `HasDerivAt`, sine/cosine derivative rules, `polarCoord`,
`Complex.polarCoord`, `Complex.arg`, and the coordinate reconstruction formula. A bounded search
over repo-local and pinned-mathlib Lean sources found no Sturm-Liouville or Pruefer-transform
declaration. Text hits for "Pruefer" in mathlib concern a fixed-point subgroup and a TODO about
Pruefer domains, which are homonyms and explicitly ineligible.

The principal complex argument has a branch cut and cannot silently replace a continuous real
phase lift along the ODE state. The canonical module, expression, expression hash, checked
transports, and statement mutations remain null. The probe and name search are intake discovery
only, not an immutable external anchor audit or proof evidence.
