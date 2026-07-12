# Intake validation

Base revision: `ea6d9ac3942ade0c65c13eccb6bcec945e698e69` (tree
`16e4f4fa87955d7ae7392859a6713a56bcfe7b7e`). Validation ran on 2026-07-12 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier-local structure and scope invariants,
bibliographic candidate identification, pinned environment identity, a narrow Lean API probe,
bounded local topic searches, proof-escape hygiene, and whitespace. The catalog subject label and
gloss are not a proposition, so elaborating a purported canonical target would invent missing
mathematics. `IntakeProbe.lean` checks only possible substrate and supplies no statement or proof
credit. No published generic JSON Schema for this new intake shape is present in the checkout; the
owned checker therefore validates explicit dossier invariants rather than claiming JSON Schema
conformance.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1424` | 0 | rank 922, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `curl -L --fail --silent --show-error https://api.crossref.org/works/10.1007/978-3-662-12878-7` | 0 | Ludwig Arnold, *Random Dynamical Systems*, Springer, 1998, and ISBN metadata agree; bibliographic discovery only |
| `curl -L --fail --silent --show-error https://link.springer.com/chapter/10.1007/978-3-662-12878-7_1` and the corresponding `_2` URL | 0 | chapter titles/pages and summaries identify numerous distinct definition, perfection, generation, converse, invariant-measure, and regularity results; no one theorem selected |
| `curl -L --fail --silent --show-error https://link.springer.com/content/pdf/10.1007/BF01192196.pdf -o /tmp/thm-m-1424-arnold-scheutzow.pdf`; `sha256sum` that file; `pdftotext -layout` it to `/tmp/thm-m-1424-arnold-scheutzow.txt` | 0 | 1,046,566-byte PDF, SHA-256 `5e231795...c8581`, 1,230 text lines; Theorems 28, 30, and 31 are distinct generation, converse, and perfection candidates; none selected or credited |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1424/IntakeProbe.lean)` | 0 | eight generic filtration, adapted-process, kernel, measure-preserving, and deterministic-flow APIs elaborated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386...` and tree `bdc39a31...` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned source tree clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...2d81` |
| `rg -n -i '\brandom dynamical systems?\b|\brandom dynamics\b|\brandom cocycle\b|\bmetric dynamical system\b|\bdriving system\b|\bstochastic flow\b|\bstochastic differential equations?\b|\bsemimartingale\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | expected no-match exit; intake discovery only, not a complete anchor audit |
| `python3 -m json.tool` on the three finalized JSON artifacts and `.stage1-worker-selftest.json` | 0 | all are valid JSON |
| `python3 -B Stage1_Instances/THM-M-1424/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, H5/M4/R4 planned boundary, null target, exact artifact inventory, worker packet, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)[[:space:]]\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1424` | 1 | expected no-match exit; no prohibited proof declaration in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-1424 .stage1-worker-selftest.json` plus a per-file `git diff --no-index --check /dev/null <file>` loop | 0 | no whitespace diagnostics; no-index exit 1 was accepted only as the expected added-file difference |

Known downstream failures remain deliberately open: an approved target correction with one exact
immutable primary-source theorem and independent review; exact base, time, state, equation/cocycle,
solution, measurability, local/global, exceptional-set, hypothesis, conclusion, and boundary
choices; canonical Lean elaboration, expression and environment fingerprints, checked transports,
and statement mutations; immutable anchor audit; discovery and obligation freezes; proof and
composition; hermetic replay; deterministic evidence bundling; independent release verification;
and master acceptance. These block ordinary theorem execution and completion but do not invalidate
a truthful, self-tested `planned` intake.
