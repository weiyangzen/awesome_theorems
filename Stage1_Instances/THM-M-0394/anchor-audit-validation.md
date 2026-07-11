# THM-M-0394 Anchor-Audit Validation

Item: `S56-M-0394-ANCHOR_AUDIT`  
Audit date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `e9c516bd976b6850ddcab868f808a7895bb7e826`

## Result

The pinned mathlib revision provides locally elaborated scheme predicates used
by the canonical object model and concrete `S`-integer and `S`-unit APIs. These
are partial infrastructure. `Mathlib.NumberTheory.SiegelsLemma` is a verified
name collision: its main theorem produces a small nonzero integer kernel vector
for a rectangular integer matrix, not finiteness of integral points on curves.

Searches over the repository, pinned mathlib, and every pinned non-mathlib Lake
dependency found no terminal proof body. Immutable recursive-tree queries for
`MichaelStollBayreuth/Heights@852034cf46fd65b6f76ff9970de6163b82a10091`
and `google-deepmind/formal-conjectures@7871d8fc7a8164a1ac16c3765b40c25ce015b681`
were complete and had no path matching the recorded aliases. Four GitHub
repository queries each returned zero results. GitHub code search returned HTTP
401 because authentication is unavailable; consequently no exhaustive public
search is claimed.

No identified external candidate carries an exact proof body, so there is
nothing truthful to pin or import. The root remains `M3`: its exact proposition
elaborates, but it is not kernel closed. This completes only the bounded anchor
inventory and candidate classification. It does not complete a proof,
validation, release, or the theorem.

## Commands And Results

Run from the repository root unless a working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks; all targets L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0394` | 0 | rank 7, planned, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| local `rg` alias search over mathlib, its docs, and `flt-regular` | 0 | 130 broad matches; relevant hits were only Siegel's lemma, S-integers, adjacent commentary, and documentation entries; no terminal curve theorem |
| source search over every pinned non-mathlib dependency | 1 | no terminal candidate match; exit 1 is ripgrep's expected no-match result |
| four GitHub repository API searches recorded in `anchor-audit.json` | 0 | totals `0, 0, 0, 0`; all `incomplete_results=false` |
| immutable GitHub recursive-tree probes for Heights and Formal Conjectures | 0 | exact requested SHA returned, `truncated=false`, no alias-matching path |
| unauthenticated GitHub code search for `"Siegel" "integral points" language:Lean` | 0 transport / HTTP 401 | `Requires authentication`; recorded limitation, not a negative exhaustive result |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0394/Statement.lean` | 0 | `Stage1Rev56.THMM0394.Statement.{u, v} : Prop` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0394/AnchorAudit.lean` | 0 | all nine pinned mathlib declaration probes elaborated; the matrix type of Siegel's lemma was printed |
| `python3 Stage1_Instances/THM-M-0394/check_anchor_audit.py` | 0 | immutable pin, statement hash, source witnesses, and eight non-closing rows verified |
| `python3 -m json.tool Stage1_Instances/THM-M-0394/anchor-audit.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0394 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The clone's pre-existing untracked `Formalizations/Lean/.lake` link reuses the
canonical pinned artifacts. No `lake update`, build, dependency clone/fetch, or
`.lake` mutation occurred. Accepted receipts remain empty pending master review.
