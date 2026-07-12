# Intake validation

Base revision: `bbb685ee4adcd9f19b5a727d1523cc7d6ad3b07f` (tree
`aadea0300fd76d31a98264ab39039d2247f8e049`).

Validation date: `2026-07-13` (`Asia/Shanghai`). This phase covers target
membership, planned dossier invariants, repository and source provenance, JSON
integrity, a bounded exact-topic source-name search, and a narrow pinned Lean
API probe. The automation-provided `Formalizations/Lean/.lake` symlink existed
before this work and was used read-only. No `lake update`, `lake build`,
dependency clone or fetch, or `.lake` mutation was run.

The modern ODE source candidate was retrieved twice from arXiv as a 305,049
byte, 24-page PDF; both downloads had SHA-256
`f5edbddab5f7a1da7591a82dca7c5a1038b5ca0fe96e8f326a2c4d3ddf4a9b36`.
Its Theorem 1 is a precise candidate, not accepted source identity for the
uncited catalog record. Crossref confirms the historical 1875 PDE
bibliography, but the publisher full text was unavailable behind a WAF and no
historical theorem passage was inspected.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1334` | 0 | rank 945, planned, L0/rework-required, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git blame -L 9733,9738 -- Docs/researches/math_theorems.md` | 0 | all six uncited repository record lines originate at commit `bcf3f9fa...b74f` |
| two bounded arXiv PDF retrievals followed by `file`, `wc -c`, `sha256sum`, `cmp -s`, `pdfinfo`, `pdftotext -layout`, and a theorem-locator `rg` query | 0 | identical 305,049-byte, 24-page v3 PDFs; Theorems 1 and 11 inspected; PDF hash recorded |
| Crossref query for `10.1515/crll.1875.80.1` | 0 | historical PDE title, 1875 date, journal issue 80, pages 1-32, DOI, and publisher confirmed; no theorem text |
| bounded publisher/EUDML historical full-text retrieval attempts | 403/202 challenge | no historical primary text obtained; recorded as an open source gate, not silently replaced |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision `8a178386...a95`, tree `bdc39a31...c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81`, respectively |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1334/IntakeProbe.lean)` | 0 | eight integral-curve, analytic, Picard-Lindelof, regularity, and Euclidean-space APIs elaborated; no target theorem stated |
| exact-topic `rg` query over repository and pinned mathlib Lean sources | 1 | expected no-match for Cauchy-Kowalevskaya name variants; bounded intake evidence only, not an exhaustive anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| Python AST parse of `check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1334/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and authoritative item identity, H1/M4/R3 planned boundary, null target, source hashes, exact artifact inventory, receipt/packet agreement, hygiene, and six open tasks agree |
| prohibited-construct scan over owned Lean files | 1 | expected no-match; no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration |
| scoped `git diff --check` plus `git diff --no-index --check /dev/null` for every untracked changed file | 0 | no whitespace diagnostics; the invariant checker independently verifies final newline, LF-only content, and trailing whitespace |

The pinned `Mathlib/Analysis/ODE/PicardLindelof.lean` file contains local
existence and finite/`C-infinity` regularity infrastructure, but its line 555
TODO says to extend the relevant Picard lemma to the analytic case. This is a
useful concrete downstream blocker, not an absence theorem or proof result.

Known downstream failures remain deliberately open: approved ODE/PDE scope and
primary-source identity; pinpoint statement, assumptions, proof boundary,
errata and independent source review; canonical Lean expression/environment
fingerprints, transports and mutations; exhaustive formal anchor audit;
obligation and discovery freezes; proof and composition; trust closure;
hermetic replay; deterministic evidence bundle; independent verification; and
master acceptance. They prevent audit and theorem completion but do not
invalidate a truthful `planned` intake.
