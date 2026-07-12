# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1435`, the label `McMullen定理`, Curtis McMullen, the year
1994, and the gloss `有理函数的Julia集` (`Julia sets of rational functions/maps`). Importance
"high" and status `已验证` are catalog metadata, not theorem or proof evidence. Intake preserves
this historical and complex-dynamical subject boundary without turning it into a theorem from
memory.

## Duplicate-target boundary

Target `THM-M-0259` has the translated title `麦克马伦定理` and otherwise identical author, year,
gloss, importance, and status. It is a separate eligible target at rank 1267 under complex
analysis, while this target is rank 933 under dynamical systems. Both remain in the authoritative
1546-target manifest. This apparent semantic duplicate cannot lend statement, source, task,
receipt, or proof credit to this ID. A merge, redirect, or denominator change requires a master
target-set correction and regenerated authorities; it is outside this owned path.

## Proposition-changing decisions

An approved target correction must select one exact source proposition and freeze:

- the immutable McMullen work, edition or version, theorem/page locator, incorporated definitions,
  proof boundary, corrections, errata, and the relationship between the stated 1994 date and any
  later publication;
- whether the dynamical object is a general rational self-map of the Riemann sphere, a polynomial,
  a real or complex quadratic polynomial, a polynomial-like map, or a named parameter family;
- coefficient domain, degree, normalization, critical points, postcritical behavior,
  renormalizability, hyperbolicity, and every exceptional or rigidity hypothesis;
- the ambient Riemann sphere or affine complex plane, including infinity, poles, the spherical
  topology or metric, and the meaning and domain of every iterate;
- the exact Julia-set definition and all supporting Fatou, normal-family, filled-set, periodic,
  multiplier, line-field, measure, dimension, connectivity, and local-connectivity conventions;
- the conclusion: a definition or characterization, density or invariance result, absence of an
  invariant line field, measure or Hausdorff-dimension claim, rigidity or universality theorem,
  connectivity statement, or another source-specific result;
- the ordered quantifiers over maps, parameters, points, periods, neighborhoods, measurable fields,
  renormalizations, and constants, together with the direction of every implication; and
- degree-zero and degree-one maps, constant and identity maps, Lattes and other exceptional maps,
  infinity and poles, empty or whole-space sets, finite versus infinite renormalization, null sets,
  and all other boundary cases.

These choices yield inequivalent propositions. They are a resolution ledger, not a statement.

## Candidate families not credited

- McMullen's Theorem 5.2 in the 1994 survey: an infinitely renormalizable real quadratic
  polynomial has a Julia set carrying no invariant line field.
- The survey's corollary about hyperbolicity of Mandelbrot-set interior components meeting the
  real axis.
- A source-specified theorem about density of hyperbolicity, structural stability, rigidity,
  renormalization, Julia-set connectivity, area, or Hausdorff dimension.
- A general rational-map characterization of a Julia set, or a theorem about the Julia set of one
  concrete polynomial or rational map.
- A result from the later book *Complex Dynamics and Renormalization* selected solely because the
  1994 survey cites it as forthcoming.

No family in this list is selected, asserted, or credited at intake.

## Explicit exclusions

The intake must not silently substitute `THM-M-0259`, the Julia-set object target `THM-M-1428`,
the Mandelbrot-set target `THM-M-1430`, the Douady-Hubbard target `THM-M-1431`, the Yoccoz target
`THM-M-1432`, the Sullivan no-wandering-domain target `THM-M-1434`, or the neighboring
renormalization and Feigenbaum targets. A theorem quoted by McMullen is not thereby "McMullen's
theorem," and a theorem by McMullen is not selected merely by matching its year and topic.

Generic facts about complex numbers, meromorphic functions, iteration, periodic points, closure,
frontier, or one-point compactification do not identify the root. Nor do a definition repackaged as
a theorem, an abstract structure containing the desired conclusion as a field, a convenient
special case, an orbit plot, a numerical fractal, or an unchecked computation.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides complex and meromorphic analysis,
function iteration, periodic points, topology, and one-point compactification APIs. Its algebraic
`RatFunc` type is not by itself a total rational self-map of a chosen Riemann-sphere model with
poles and iterates resolved. A bounded source-name search found no target-specific McMullen,
Julia-set, rational-dynamics, or complex-dynamics declaration. These facts are intake discovery
only, not an exhaustive anchor audit, exact-statement elaboration, or machine-proof evidence.
