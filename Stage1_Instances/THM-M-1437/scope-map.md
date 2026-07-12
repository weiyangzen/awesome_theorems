# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-1437`, the label `Feigenbaum普适性`, Mitchell Feigenbaum,
the year 1975, and the gloss `倍周期分岔的普适常数`. Importance "high" and status `已验证`
are catalog metadata, not theorem or proof evidence. Intake preserves the period-doubling
universality subject boundary without turning that phrase into a theorem from memory.

## Proposition-changing decisions

An approved target correction must select an exact source proposition and freeze:

- whether the root concerns parameter scaling delta, orbit/spatial scaling alpha, a universal
  fixed-point function, convergence under renormalization, or a spectral/hyperbolicity result;
- the one-parameter family, its parameterization, interval or function-space domain, codomain,
  topology, differentiability or analyticity, unimodality, critical point, and critical order;
- whether the critical order is exactly quadratic or an arbitrary fixed `z > 1`, and which
  normalization and coordinate/conjugacy equivalences are permitted;
- the definition, indexing, existence, uniqueness, and stability/minimal-period conventions for
  the bifurcation parameters and their `2^n` cycles;
- existence and meaning of the accumulation parameter and the orientation of the successive-gap
  ratio, including signs, inverses, offsets, and whether the conclusion is a limit or asymptotic;
- whether delta merely exists, equals a defined limit or eigenvalue, is universal over a stated
  map class, or lies within a proved exact error interval around a decimal approximation;
- the renormalization operator, Banach/function space, normalization, fixed-point equation,
  differentiability/compactness, spectrum, and number of expanding directions when relevant; and
- degenerate maps, flat or multiple critical points, nongeneric crossings, reparameterizations,
  finite cascades, nonunique cycles, and all other boundary cases.

These choices produce materially different propositions. They are a resolution ledger, not a
canonical statement.

## Candidate families not credited

- Convergence of successive period-doubling parameter-gap ratios to the Feigenbaum delta for a
  source-specified normalized class of quadratic-critical unimodal families.
- Existence and universality of delta as the expanding eigenvalue of a specified renormalization
  fixed point.
- Existence, uniqueness, or hyperbolicity of that fixed point and convergence of renormalizations.
- Spatial/orbit scaling governed by alpha and a universal fixed-point function.
- A rigorous enclosure or decimal computation for delta in one selected map family.

No family in this list is selected or credited at intake.

## Explicit exclusions

The adjacent `THM-M-1436` renormalization-theory topic, `THM-M-1438` Lanford computer-assisted
proof, and `THM-M-1439` Lyubich analytic proof are distinct roots. Their statements or proofs must
not be imported as the identity of this target. The separate physics record `THM-P-0784`, which
mentions `delta ≈ 4.669`, is outside the rev-5.6 M-target set and supplies only another ambiguous
catalog gloss.

Also excluded are confusing alpha with delta, proving only a generic ratio-limit lemma, computing
finitely many logistic-map ratios, returning a decimal, plotting or simulating orbits, assuming the
desired limit or universality as a structure field, assuming a constant exists and projecting it,
and using a tautological fixed-point or convergence package. The catalog label `已验证` supplies
neither human-source nor Lean kernel credit.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib exposes iterates, periodic and fixed points,
minimal periods, semiconjugacy, and limits. These generic APIs do not encode a parameterized
unimodal family, bifurcation parameters, quadratic criticality, stability, renormalization,
hyperbolicity, or universal ratios. The bounded intake search found no target-specific Feigenbaum,
period-doubling, Coullet-Tresser, or Lanford declaration. This is discovery input only, not an
exhaustive anchor audit or evidence that no external formalization exists.
