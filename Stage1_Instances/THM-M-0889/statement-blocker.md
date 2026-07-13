# THM-M-0889 exact-statement gate: blocked

- Item: `S56-M-0889-STATEMENT`
- Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a`
- Base tree: `fdfff18dea4c6798c5b322b6088dfe556109c134`
- Attempt date: 2026-07-13 (`Asia/Shanghai`)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete catalog wording is the name `Alon-Milman` theorem, attribution to Noga Alon and
Vitali Milman, the year 1985, and the gloss `spectral gap and expansion`. It supplies no formula,
theorem number, graph convention, spectral operator, expansion invariant, ordered binder,
hypothesis, conclusion, proof boundary, correction or erratum disposition, or reviewer. Stage0
explicitly leaves precise definitions and premises open, and the catalog's `verified` label is
untrusted under rev-5.6.

The matching primary paper is N. Alon and V. D. Milman, *lambda_1, Isoperimetric Inequalities for
Graphs, and Superconcentrators*, JCTB 38(1) (1985), 73-88, DOI
`10.1016/0095-8956(85)90092-9`. The intake inspected an author-hosted scan with SHA-256
`5942686400daeac3383624c285ae24d795f39de838726d5fa24c231a4e3fe868`. That paper contains several
inequivalent candidate roots:

- Lemma 2.1 is a separation inequality for two disjoint vertex subsets.
- Theorem 2.5 is a metric-neighborhood bound involving maximum degree, set distance, and the
  second combinatorial-Laplacian eigenvalue.
- Theorem 2.6 is an iterated exponential concentration bound.
- Theorem 2.7 is a diameter bound.
- Theorem 4.3 maps an enlarger to an extended-double-cover expander with a source-specific
  nonlinear neighborhood inequality.

The familiar later two-sided regular-graph edge-expansion inequality is yet another packaging. It
changes definitions and proof provenance, and AM85 Remark 4.4 explicitly defers a properly stated
converse. Selecting it would also risk merging this target with `THM-M-0888` Cheeger inequality.
Thus choosing any candidate by familiarity would invent or substitute proposition-changing
mathematics rather than elaborate the exact received target.

The unresolved choices include finite/simple/connected/regular graph hypotheses; the adjacency,
combinatorial-Laplacian, or normalized-Laplacian spectrum; eigenvalue indexing and multiplicity;
edge boundary, external neighborhood, conductance, metric concentration, enlarger, or bipartite
expander definitions; every normalization and constant; inequality direction; ordered binders;
and empty, singleton, disconnected, degree-zero, zero-gap, denominator, distance, and equality
cases.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. The intake correctly leaves the canonical mathematical claim, Lean
module and expression, expression hash, and canonical-target environment fingerprint null at
`[H1, M4, R4]`. Consequently there is no target for which minimal imports, alternate transports,
or removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can be
certified. Those four mutation classes are undefined, not passed. No `Statement.lean`, theorem
declaration, proof body, weakened special case, or broadened substitute was added.

The prerequisite `S56-M-0889-INTAKE` is only provisional worker state `[_]`, not master-accepted
state `[x]`. Its receipt declares `accepted: false`, is not content-addressed, and supplies no
accepted receipt ID. Rev-5.6 section 10.2 permits this dependency-ordered blocker investigation,
but dependency status independently prevents accepted statement closure.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates under pinned Lean 4.29.0 and mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. Its four direct imports expose finite simple
graphs, distance, degree, adjacency and Laplacian matrices, positivity, and Hermitian eigenvalues.
All eleven checks pass; complete output has SHA-256
`0521ebbf5bcf2117e7160a635dce98b3e36cc21da3fa567d8cbd2770e127b835`.

These interfaces are adjacent encoding substrate only. The probe defines no expansion invariant,
spectral gap, canonical Alon-Milman target, checked source transport, or proof body, and its imports
cannot be certified minimal for an absent target. A bounded exact-topic search over pinned mathlib
and repository-local Lean found only unrelated spectral-gap prose and the probe disclaimer. This
is discovery-only evidence, not the downstream anchor audit or a global absence claim.

The automation-provided `Formalizations/Lean/.lake` symlink was used read-only and the pinned
mathlib package worktree remained clean. No `lake update`, `lake build`, dependency clone or fetch,
or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`). Lean commands ran from
`Formalizations/Lean`; all others ran from the repository root unless noted. Exact arguments,
exits, result summaries, and current input fingerprints are preserved in
`statement-blocker.json`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0889` | 0 | rank 1439; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped reads of the standard, skill, target manifest, catalog, Stage0 projection, and complete intake dossier | 0 | confirmed competing primary roots, a null canonical target, and unresolved proposition-defining choices |
| current `sha256sum` over authority, intake, source, probe, toolchain, lockfile, and pinned mathlib inputs | 0 | exact digests are recorded in the structured blocker |
| `python3 -B Stage1_Instances/THM-M-0889/check_intake.py` | 1 | historical intake replay expects state `[ ]` and attempts 0; current authority records provisional `[_]` and attempts 1, so historical evidence was not rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree and package-status checks | 0 | expected revision and tree passed; package worktree was clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0889/IntakeProbe.lean` | 0 | eleven adjacent graph/matrix APIs elaborated; output hash recorded above; no target or proof body |
| bounded exact-topic search over pinned mathlib and repository-local Lean | 0 | only unrelated spectral-gap text and the intake disclaimer matched; no target-family statement is inferred |
| prohibited-construct scan over owned Lean | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, scoped blocker invariants, whitespace, and absent-self-test checks are recorded in the
structured blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must first refresh and master-accept the intake dependency. Accountable
reviewers must then preserve and hash one immutable primary root or explicitly approved modern
reformulation and independently approve every incorporated definition, premise, proof boundary,
correction, erratum, and neighboring-target boundary. That decision must fix the graph model,
spectral operator and indexing, expansion invariant, normalization, constants, directions,
ordered binders, hypotheses, conclusion, alternate encodings, and all degenerate cases.

A fresh statement attempt can then encode precisely that reviewed claim in Lean, prove its pinned
direct imports minimal, serialize and hash the elaborated expression and environment, compile
every credited transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; the root stays `[H1, M4, R4]`;
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, or master acceptance is claimed.
