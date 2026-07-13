# Intake validation

Validation date: 2026-07-13 (Asia/Shanghai).
Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a`.
Base tree: `fdfff18dea4c6798c5b322b6088dfe556109c134`.

The worker reused the automation-provided canonical `Formalizations/Lean/.lake` symlink read-only.
No `lake update`, `lake build`, dependency clone or fetch, package mutation, theorem declaration,
or proof was run. External primary-source bytes were inspected in temporary storage only. The
dirty worker snapshot and unsigned provisional receipt are nonrelease evidence.

## Commands and results

Commands ran from the repository root unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0959` | 0 | rank 1493, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 7001,7006 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error -o /tmp/clp-published.pdf https://annals.math.princeton.edu/wp-content/uploads/annals-v185-n1-p07-p.pdf` | 0 | 314538-byte publisher PDF retrieved to temporary storage; SHA-256 `9829dbcdb774826379ba2c98f62cc4267ca8d0e24ad7a89f596bcc2c5c224b3e` |
| `pdfinfo /tmp/clp-published.pdf` and `pdftotext -layout /tmp/clp-published.pdf /tmp/clp-published.txt` | 0 | 7-page published article; layout text SHA-256 `cd1c2cdcafb20f8c992abea737cc127d2c1828036a88de089dd12378be3b6ee8`; definition and numbered-result pinpoints inspected |
| `curl -L --fail --silent --show-error https://export.arxiv.org/api/query?id_list=1605.01506` | 0 | immutable lead `1605.01506v2`, updated 2016-05-21, with correction comment; observed response SHA-256 `4ebc1e51ab8ec130c5ac6706e106324f058c72d054f43322f72bb2c66709eb31` |
| `curl -L --fail --silent --show-error https://api.crossref.org/works/10.4007/annals.2017.185.1.7 -o /tmp/clp-crossref.json` | 0 | matching DOI/title/authors/year/volume/issue metadata; observed response SHA-256 `01a049bb0b4953affe0ee75e441c208178f9a2d714760020a305f16a0eb453e1` |
| published CLP text, arXiv revision history, and Ellenberg-Gijswijt neighbor-source comparison | 0 | definition, Theorem 1, Corollary 1, Lemma 1, Proposition 1, proof boundary, v1/v2 bound change, published correction boundary, and distinct `F_q^n` extension located; discovery evidence only |
| `rg -n -i --glob '*.lean' 'Croot[ _-]*Lev[ _-]*Pach\|progression.?free.*Z.?4\|Z.?4.*exponentially.?small\|4.*gamma.*n\|CLP method' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib Stage1_Instances` | 0 | matches only this intake wording; no source-identical pre-existing Lean declaration located; bounded intake search, not a global anchor audit |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned package worktree remained clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0959/IntakeProbe.lean` | 0 | eight adjacent pinned APIs elaborated; output SHA-256 `f5a4843fc8b1c60daf2a405ae8f28a656c8d412bc7739bfa2e72fb41ad9f90f7`; no target declaration or proof body |
| `python3 -m json.tool` on the three owned JSON documents and `.stage1-worker-selftest.json` | 0 | instance, task DAG, provisional receipt, and worker packet parse |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0959-pycache python3 -m py_compile Stage1_Instances/THM-M-0959/check_intake.py` | 0 | scoped validator compiled without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0959/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | authority identity, current hashes, null target, H5/M4/R4 boundary, exact inventory, recipes, receipt/packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0959/check_intake.py` | 0 | packet-independent replay passed |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-0959/*.lean` | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0959 .stage1-worker-selftest.json` plus new-file hygiene checks | 0 | no whitespace, final-newline, CR, NUL, or trailing-space defect |

## Known open gates

- The method/application label does not select a truth-valued root. Exact numbered-result or
  proof-provenance selection, complete incorporated definition/premise/correction crosswalk,
  `Z_4^n` versus `F_q^n` neighbor reconciliation, and independent review remain open.
- No canonical Lean expression, minimal imports, expression or environment fingerprint, checked
  alternate encoding, or removed-hypothesis/changed-domain/changed-binder/boundary mutation exists.
- The API probe provides only adjacent substrate. The source's pairwise-distinct progression
  predicate is not mathlib `ThreeAPFree` on `ZMod 4` (`{0, 2}` is a concrete mismatch); base-two
  entropy, open-interval maximum, real exponent, polynomial lemma, and CLP composition have not
  been formalized or credited.
- Complete formal anchor and proof-body audit, discovery and obligation freezes, typed graphs,
  proof, composition, trust/provenance closure, readable reconstruction, hermetic replay,
  deterministic bundle, independent verification, release, and master acceptance remain open.

These failures block statement and theorem execution but do not invalidate a truthful,
self-tested `planned` intake. Only the integration lane may accept the provisional worker receipt.
