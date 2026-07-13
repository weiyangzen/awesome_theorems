# Intake validation

Base revision: `0e5ae82e6d507ee607c3f011900571ffd8096800` (tree
`400e6edf1f69b971b60a367e3ea29be359b07907`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers manifest membership, the planned dossier and open task DAG, source-record
discrimination, JSON integrity, prohibited-construct absence, and a narrow pinned Lean API probe.
Because the catalog does not select one proposition from Post's creative-set family, no canonical
target, expression hash, mutation result, source-proof status, or theorem proof is claimed. The
pre-existing canonical `.lake` artifacts were reused read-only; no dependency update, dependency
build, dependency clone/fetch, or `.lake` mutation was run. Source-document HTTP fetches are
recorded separately below.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `git status --short` | 0 | before work, only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present |
| `git rev-parse HEAD HEAD^{tree}` | 0 | recorded base revision and tree above |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets validated |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0746` | 0 | rank 1333; planned; legacy artifacts unaccepted; theorem incomplete |
| source search over `Docs/researches/math_theorems.md`, `Docs/researches/cs_theorems.md`, and `Docs/Stage0_Blueprint.md` | 0 | found only the vague creative-set property gloss, explicit open Stage0 fields, and a weaker separate computer-science row |
| `curl -L --fail --max-time 30 -sS 'https://api.crossref.org/works/10.1090/S0002-9904-1944-08111-1' -o /tmp/thm-m-0746-crossref.json` | 0 | confirmed Post, title, *Bull. AMS* 50(5), pages 284-316, and 1944; raw response 2,143 bytes, SHA-256 `efa22b...48d0` |
| `curl -L --max-time 60 -sS -A 'Mozilla/5.0' 'https://www.ams.org/journals/bull/1944-50-05/S0002-9904-1944-08111-1/S0002-9904-1944-08111-1.pdf' -o /tmp/thm-m-0746-post.pdf` followed by `pdfinfo`, `pdftotext -layout`, and page inspection | 0 | inspected a 33-page, 3,959,828-byte PDF, SHA-256 `b2f200...d0c1d`; preliminary proof boundary at printed pages 292-296, definition at 295-296, existence theorem and distinct consequences at 296 |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e3...6740`; Lake 5.0.0-src+98dc76e |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib `8a178386...ea95`, tree `bdc39a31...5c2b` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0746/IntakeProbe.lean` | 0 | all twelve c.e./code/computability/reduction API checks elaborated; no theorem was declared |
| `rg -n -i '\bcreative\b\|creative set\|productive set' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib -g '*.lean'` | 1 | expected no-match result; no computability-theoretic creative/productive-set declaration found in the bounded search |
| `rg -n '\b(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-0746 -g '*.lean'` | 1 | expected no-match result; no prohibited Lean construct |
| `python3 -m json.tool` on all three owned JSON records | 0 | valid JSON with no parser errors |
| `python3 -B Stage1_Instances/THM-M-0746/check_intake.py` | 0 | identity, authority hashes, `planned`/`H5-M4-R4`, source boundaries, artifact inventory, receipt, and six-task chain passed |
| `python3 -B Stage1_Instances/THM-M-0746/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | scheduler-minimal root packet agrees with the owned provisional receipt |
| `git diff --check -- Stage1_Instances/THM-M-0746 .stage1-worker-selftest.json` plus per-file no-index checks | 0 | no whitespace diagnostics in tracked or untracked touched files |

## Evidence boundary

The source PDF and Crossref response were inspected from temporary copies and are identified by
digest, byte count, DOI, edition, section, and pages. They are not vendored evidence, signed source
reviews, or release inputs. OCR loses some complement overbars; page images were used to verify the
mathematical direction, but a source reviewer must independently preserve and transcribe the exact
passage before statement acceptance.

Known downstream failures remain intentionally open: catalog-root selection and independent source
review, exact Lean statement elaboration and four semantic mutation classes, frozen discovery and
obligation registries, exhaustive formal-anchor audit, proof and composition, trust closure,
readable reconstruction, hermetic replay, deterministic evidence bundle, independent verification,
release, and master acceptance. These prevent theorem completion but do not invalidate a truthful,
self-tested `planned` intake proposal.
