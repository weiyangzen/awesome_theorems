# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`. Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, an authoritative source-family and errata inspection, JSON and scoped invariants, a
narrow pinned Lean substrate probe, bounded declaration search, prohibited-construct hygiene, and
whitespace. It does not validate a canonical theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The owned intake files and root worker packet make the final tree dirty and nonrelease.

## Environment and source boundary

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`; Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- The author-hosted, publisher-permitted preliminary edition of Teschl's ODE text and official
  errata were inspected temporarily. Section 5.5, printed pages 166-174, separates numerous
  zero-count, nodal, comparison, spectral, asymptotic, and oscillation-criterion results. The
  official errata changes formulas and proof details on pages 167-172. No external file was added
  to the repository, the catalog cites neither source, and no immutable H0 admission or independent
  review is claimed.

## Commands and results

All repository commands ran at the repository root unless `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1387` | 0 | rank 997, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 10104,10109 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error --max-time 60 'https://www.mat.univie.ac.at/~gerald/ftp/book-ode/ode.pdf' -o /tmp/teschl-ode-thm1387.pdf` | 0 | retrieved the author-hosted publisher-permitted preliminary edition outside the repository; SHA-256 `36243315...ffc36e` |
| `pdfinfo /tmp/teschl-ode-thm1387.pdf` | 0 | Teschl title and author; 364 pages; 4,133,331 bytes; PDF 1.4 |
| `pdftotext -layout /tmp/teschl-ode-thm1387.pdf /tmp/teschl-ode-thm1387.txt` | 0 | text extraction completed; SHA-256 `4ba05235...e5a57` |
| `sed -n '9235,9700p' /tmp/teschl-ode-thm1387.txt > /tmp/thm-m-1387-teschl-section-5.5.txt` | 0 | extracted 466 lines and 31,894 bytes of Section 5.5 context; SHA-256 `1570dafb...9d1` |
| `rg -n 'Lemma 5\.14\|Theorem 5\.17\|Theorem 5\.18\|Theorem 5\.20\|Lemma 5\.21\|Theorem 5\.22\|Corollary 5\.23\|Theorem 5\.25\|Theorem 5\.26' /tmp/thm-m-1387-teschl-section-5.5.txt` | 0 | located nine distinct named results and the nearby half-line oscillation definition; source-family discrimination only |
| `curl -L --fail --silent --show-error --max-time 60 'https://www.mat.univie.ac.at/~gerald/ftp/book-ode/errata.pdf' -o /tmp/teschl-ode-errata-thm1387.pdf` | 0 | retrieved official errata outside the repository; SHA-256 `3eacbac5...996e` |
| `pdftotext -layout /tmp/teschl-ode-errata-thm1387.pdf /tmp/teschl-ode-errata-thm1387.txt` | 0 | errata text extraction completed; SHA-256 `f4f4ce4c...c6af4` |
| `rg -n -i -C 3 'Page 167\|Page 168\|Page 169\|Page 172' /tmp/teschl-ode-errata-thm1387.txt` | 0 | located the Section 5.5 formula, caption, angle, proof, eigenvalue-count, and lead-in corrections; matched output SHA-256 `80d293f9...2e36` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...85b1d2` and `321626c8...d81` as recorded in structured artifacts |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1387/IntakeProbe.lean)` | 0 | seven adjacent pinned integral-curve, derivative, infinity, and filter APIs elaborated; output SHA-256 `760037e8...7ec7c4`; no target theorem declared |
| `rg -n -i --glob '*.lean' '^(theorem\|lemma\|def\|abbrev\|structure\|class)[[:space:]].*(ode.*oscillat\|oscillat.*ode\|sturm.*liouville\|kneser)' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 (expected no match) | no exact declaration in the bounded local search; not an exhaustive anchor audit or external absence claim |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1387-pycache python3 -m py_compile Stage1_Instances/THM-M-1387/check_intake.py` | 0 | scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1387/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and DAG identity, null target, planned H5/M4/R4 boundary, exact artifact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1387/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-1387` | 1 (expected no match) | no prohibited declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1387 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

## Status boundary

This is provisional worker self-test evidence for `S56-M-1387-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact source/root selection and independent review,
canonical Lean elaboration and statement mutations, complete anchor audit and discovery freeze,
obligation registry, typed graphs, proof, composition, trust closure, readable reconstruction,
hermetic replay, deterministic release bundle, and independent verification remain open. These
failures prevent statement, audit-completion, and theorem-completion claims, but they do not
invalidate the planned intake.
