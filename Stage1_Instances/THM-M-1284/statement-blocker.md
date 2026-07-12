# Exact-statement gate: blocked

Item: `S56-M-1284-STATEMENT`  
Theorem: `THM-M-1284`  
Base revision: `6fe9e10bc6bd77776ffbe03647af1d6c084ba5b9`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the available source record. The
repository supplies only the label "Ye theorem" and the phrase "convergence of Yamabe flow". The
accepted intake identifies Rugang Ye, *Global existence and convergence of Yamabe flow*, *Journal
of Differential Geometry* 39 (1994), 35-50, DOI `10.4310/jdg/1214454674`, as the primary source
family, but it deliberately leaves the theorem/page transcription and all assumptions open.

The source wording available in the repository does not determine:

- which numbered global-existence or convergence result in Ye's paper is the canonical root;
- the manifold dimension, compactness, local conformal-flatness, curvature, or Yamabe-invariant
  hypotheses;
- the normalized flow equation, sign and scaling conventions, initial metric, and time domain;
- the quantified solution object and its spatial/time regularity;
- the convergence topology or rate and the exact characterization of the limiting metric;
- exceptional, stationary, and boundary cases, or whether global existence and convergence form
  one compound target or separate results.

These choices distinguish inequivalent propositions. Selecting a standard Yamabe-flow theorem
from memory, encoding unconditional convergence on every closed manifold, or replacing the flow
theorem with the Yamabe problem would broaden or substitute the assigned claim. The metadata field
`已验证` is explicitly untrusted under rev-5.6 and supplies neither statement identity nor proof
credit.

An attempt to retrieve the published PDF from Project Euclid on 2026-07-12 returned an anti-bot
HTML response rather than a source document. Its SHA-256 is recorded below only to make the failed
retrieval auditable; it is not a source pin. Crossref and OpenAlex confirmed bibliographic identity
and the Project Euclid URL but did not expose the theorem text. Thus the first failed gate remains
rev-5.6 canonical human-claim identity. No canonical expression, minimal import set, checked
transport, expression hash, or removed-hypothesis/domain/binder-scope/boundary mutation suite can
be supplied without inventing the missing mathematics. Machine debt remains `M4`.

## Lean and repository boundary

There is no legacy Lean slot for this target (`legacy_priority_slot` is null), and no target Lean
file exists in the owned directory. A case-insensitive search of pinned mathlib found no source
match for `Yamabe`, `scalarCurvature`, `ScalarCurvature`, `RiemannianMetric.*flow`, or
`yamabeFlow`. This is a statement-feasibility probe, not the later anchor audit. The only
repo-local Stage1 matches for "scalar curvature" are unrelated historical discovery files, which
also report missing scalar-curvature APIs; none names or encodes Ye's result.

The pinned environment itself is usable: Lean is `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake is
`5.0.0-src+98dc76e`, and mathlib is pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The worker's untracked
`Formalizations/Lean/.lake` symlink points to the canonical pinned artifacts. It was read only; no
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed.

## Validation evidence

Commands ran from this worker clone on 2026-07-12 unless the table states a subdirectory.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1284` | 0 | rank 455, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | SHA-256 `651c8acc...b1d2` and `321626c8...2d81`, respectively |
| `rg -n -i 'Yamabe\|scalar[ _-]?curvature\|RiemannianMetric.*flow\|yamabeFlow' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching pinned mathlib source; exit 1 is ripgrep's no-match result |
| `curl -L --fail --silent --show-error -o /tmp/thm-m-1284-source.pdf 'https://projecteuclid.org/journals/journal-of-differential-geometry/volume-39/issue-1/Global-existence-and-convergence-of-Yamabe-flow/10.4310/jdg/1214454674.pdf'` | 0 | response was 1056-byte anti-bot HTML, not PDF; SHA-256 `53020215...fc` |

## Retry condition

An accountable source reviewer must provide an immutable copy of Ye's primary paper, select the
exact theorem or explicitly justified compound result, and transcribe its equation, ordered
binders, every hypothesis, conclusion, qualification, and boundary case with page-level anchors
and an errata check. Pinned Lean definitions must then be selected or implemented for the required
scalar curvature, normalized Yamabe flow, solution regularity, and convergence topology. A later
statement run can minimize imports, elaborate and serialize the exact expression, validate any
alternate encoding by checked transport, and run all four required mutation classes.

This artifact records a blocker only. It does not complete the statement node, accept a receipt,
modify execution state, or claim audit/theorem completion. The assigned phase is not genuinely
self-tested, so no `.stage1-worker-selftest.json` is emitted.
