# Statement-phase blocker

Item: `S56-M-1546-STATEMENT`  
Theorem: `THM-M-1546`  
Base revision: `7ec88ede0f01b2584a3d33be7960e61e8aa7eae5`

## Verdict

The rev-5.6 exact-statement gate remains blocked. No canonical Lean declaration was added, and no
statement-phase self-test receipt is claimed.

The intake correctly identifies Hitchin's 1987 paper as a source family, but neither the repository
nor the accessible publisher metadata identifies the exact theorem/proposition and page whose
logical content is to be encoded. The repository phrase "algebraic integrable system" is not enough
to decide the following source-sensitive choices:

- whether the target is the cotangent bundle of stable bundles, a stable Higgs-bundle moduli space,
  or an explicitly delimited open locus;
- whether determinant and trace are fixed, hence whether the characteristic-coefficient base is the
  `GL(n)` base or a trace-free/Prym variant;
- the rank, degree, genus, stability, smoothness, and coprimality assumptions;
- whether the conclusion is Poisson independence/involutivity, algebraic complete integrability,
  a generic Jacobian/Prym fiber identification, or a conjunction of these results;
- the precise exceptional/discriminant locus and the status of rank one and low genus.

Choosing values for those fields without the primary theorem text would invent mathematics and
could broaden or substitute the requested theorem. Encoding the legacy
`AwesomeTheorems.Stage1.S1_M_205.HitchinSystemData` is not an acceptable fallback: it stores
Poisson commutation, smooth spectral curves, abelian and Lagrangian fibers, the dimension count, and
complete integrability as proposition fields. Its `StatementShape` therefore models an interface
over assumed conclusions rather than the exact Hitchin theorem.

## Source access evidence

Crossref resolves DOI `10.1215/S0012-7094-87-05408-1` to Nigel Hitchin, "Stable bundles and
integrable systems," *Duke Mathematical Journal* 54(1), 1987, but exposes only bibliographic
metadata. OpenAlex likewise reports the article as closed access. The Project Euclid download URL
returned an Incapsula HTML challenge rather than the paper. This is sufficient to confirm the
bibliographic family, not theorem wording, numbering, pages, or assumptions.

The blocker can be cleared by supplying or locating an immutable copy of the primary paper and
recording the exact theorem/proposition, printed pages, full assumptions, and notation crosswalk.
Only then can the canonical Lean expression, checked alternate-form transports, expression hash,
and semantic mutations be truthfully produced.

## Commands and results

Run from the repository root on 2026-07-12:

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1546` | exit 0; rank 205, planned, L0/rework-required, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `curl` Crossref/OpenAlex metadata queries for the DOI | exit 0; bibliography found, no primary theorem text |
| `curl` Project Euclid article/download URLs | transport exit 0, invalid evidence payload; HTML anti-bot challenge, not PDF |

The pre-existing untracked `Formalizations/Lean/.lake` link/artifact was not modified. No `lake
update`, build, clone, or fetch was run. Because no exact target can yet be authored, running Lean on
a guessed target would not validate this assigned phase.

## Status boundary

First failed gate: primary-source exact-statement identification. The provisional vector remains
`[H2, M4, R4]`; audit completion and theorem completion remain false. This artifact records an
actionable blocker only and is not a node-specific completion receipt.
