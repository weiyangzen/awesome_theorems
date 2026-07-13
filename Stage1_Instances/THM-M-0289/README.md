# THM-M-0289 rev-5.6 intake

`THM-M-0289` is the catalog item "Hardy-Littlewood maximal function theorem." The repository
supplies only the gloss "weak-type estimate for the maximal function," attributes it to Godfrey
Hardy and John Littlewood in 1930, and carries an untrusted `verified` label. This dossier records
a fail-closed `planned` intake from the uniform `L0 / rework_required` baseline.

## Intake result

The bibliographic record for Hardy and Littlewood, "A maximal theorem with function-theoretic
applications," *Acta Mathematica* 54 (1930), 81-116, DOI `10.1007/BF02547518`, was verified
through Crossref. The article text could not be retrieved as a PDF during this run, so no theorem
number, page-level statement, definition, hypothesis, proof boundary, or errata conclusion is
credited. The citation is a primary-source lead only.

The catalog identifies the weak `(1,1)` maximal-function theorem family, but does not determine a
canonical proposition. Centeredness, averaging sets, domain and dimension, input model, threshold,
normalization, estimate constant, and boundary cases all change the statement. Selecting them at
intake would invent missing mathematics. The human and Lean canonical statements therefore remain
null, with the exact choices recorded in `scope-map.md`.

## Boundaries

The repository separately schedules the same apparent mathematical family as `THM-M-0368`. Its
dossier is read-only discovery input. The two IDs share no scope authority, status, receipt, proof
credit, or target ownership; duplicate identity and any future evidence transport require an
integration-lane decision.

`IntakeProbe.lean` checks only adjacent pinned measure, ball, lower-integral, Besicovitch, and Vitali
interfaces. A bounded name search found no Hardy-Littlewood maximal-function definition or weak
`(1,1)` theorem in pinned mathlib. Immutable external discovery did locate
`fpvandoorn/carleson@fdcce451.../Carleson/ToMathlib/HardyLittlewood.lean`, which defines an
uncentered ball maximal function on doubling metric-measure spaces and proves a weak `(1,1)`
theorem. It is a strong formal lead, but it uses Lean `v4.30.0-rc2` and mathlib `1a4917a...`, is
absent from the repo-local dependency closure, and has not been transported to an inspected or
frozen exact human source statement. No target declaration or proof body is introduced locally.

The provisional root vector is `[H1, M4, R4]`: a primary bibliographic lead is identified, but its
statement and proof have not been inspected or reviewed; the external formal lead cannot be
classified as an exact M1 root before statement identity, trust, and independent build evidence are
audited; and no source-faithful readable proof reconstruction is accepted. All six downstream tasks
remain open. Neither audit completion nor theorem completion is claimed.
