# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6994-6999` supplies exactly the title `Elkin construction`,
Michael Elkin, 2011, the gloss `improvement of the Behrend construction`, importance `high`, and
status `verified` (the English phrases here translate the Chinese catalog fields). All six uncited
lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:26119-26144` repeats the gloss while explicitly leaving exact definitions
and premises, proof route, dependencies, alternate forms, axioms, machine status, and artifact
links open. The rev-5.6 manifest retains the source label only as `source_status_untrusted` and
resets this target to `L0 / rework_required`.

## Primary-source lead

The matching work is Michael Elkin, *An Improved Construction of Progression-Free Sets*. The
inspected version is arXiv `0801.4310v1`, submitted 2008-01-28. A 2010 SODA proceedings version is
pages 886-905, DOI `10.1137/1.9781611973075.72`. The catalog's 2011 date matches the journal
publication in *Israel Journal of Mathematics* 184(1), pages 93-128, DOI
`10.1007/s11856-011-0061-1`.

The arXiv v1 PDF is 242,272 bytes with SHA-256
`f2be0497fb1be4653343463a6ca95b647c9c880402f4b1115f77e98c5843022b`. It was inspected but not
added as a repository artifact. ArXiv records only this one version. Section 2 on printed page 2
defines arithmetic triples, progression-free sets, `nu(n)`, `Omega`, and base-2 `log`; Section 3
equation (5) on printed page 3 states Elkin's improved extremal bound; and Section 4 equation (12)
and its concluding paragraph on printed page 6 state the improved construction bound. These
passages identify a complete self-contained proof route. The statement phase selects this immutable
arXiv version as its authoritative statement edition. The final journal text was not lawfully
preserved and compared against the preprint; no correction or errata audit and no independent
source review were completed. This supports exact statement identity at provisional `H1`, not
`H0`.

## Candidate statement map

| Catalog component | Primary-source component | Prospective Lean surface | Intake status |
|---|---|---|---|
| Elkin construction | equation (5) extremal bound, realized by the Section 4 construction | one-based `addRothNumber` root plus explicit witness alternate | root and checked iff frozen |
| Behrend improvement | factor `Theta(sqrt(log n))` over the cited Behrend bound | exact improved lower-bound conclusion | improved conclusion selected; comparison excluded from root |
| progression-free | no three distinct integers with one the average of the other two | ordered-middle `SourceProgressionFree` (universal binders cover every permutation) and `ThreeAPFree` | checked iff frozen |
| `{1, ..., n}` | source interval `[{n}]` | `Finset.Ico 1 (n + 1)` and translated `rothNumberNat n` | checked equality and target iff frozen |
| size lower bound | `Omega((log_2 n)^(1/4) * n / 2^(2 sqrt(2) sqrt(log_2 n)))` | positive `c`, positive `N`, every `n >= N`, Real-coerced extremum | exact binder expansion frozen |
| 2011 | journal publication year | immutable edition/revision identity | journal metadata found; journal text/version comparison open |
| `verified` | untrusted inventory metadata | no declaration or proof body | no H0, machine, or readability credit |

The source defines `Omega` through a positive universal constant and a positive integer threshold,
then says the result holds for positive `n` while noting that small values can be handled by reducing
the constant. The canonical root uses the literal asymptotic expansion. The all-positive form is
not credited without a separate finite-case transport.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the inspected modules provide:

- `ThreeAPFree`, `threeAPFree_iff_eq_right`, `rothNumberNat`, and `rothNumberNat_spec`;
- `addRothNumber_Ico`, useful substrate for interval translation; and
- `Behrend.roth_lower_bound`, the checked bound
  `(N : Real) * exp (-4 * sqrt (log N)) <= rothNumberNat N`.

The pinned Behrend theorem differs from Elkin's candidate in both the exponential constant after
log normalization and the extra fourth-root logarithmic factor. It is a related weaker theorem,
not an exact formal anchor. A bounded search found no declaration named for Elkin or the improved
formula. This is intake discovery only, not a complete local or external anchor audit.

## Statement resolution and remaining admission

`Statement.lean` and `statement.json` select arXiv v1, transcribe its definitions, binders, formula,
conclusion, and finite-case convention, elaborate the exact target with deletion-minimal imports,
serialize expression and environment fingerprints, check interval and progression transports,
and run all four required mutation classes.

The SODA 2010 and journal 2011 headline formulas agree with arXiv v1, but their complete bodies
were not compared. The 36-page journal version has many more references and explicitly adds a
discrete-geometry application, so whole-edition identity is not claimed. Before H0, accountable
reviewers must lawfully admit the selected source, compare available editions, audit corrections
and errata, map the source proof to obligations, and independently approve the packet.
