# Intake validation

Base revision: `3ed74ce8b03564707b34b6e2314d2bb6d0a6206e`; base tree:
`5d5275ace8e7c0d1026c248e8f2760e18c3c8dda`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, an authoritative source-family inspection, JSON and scoped invariants, a narrow pinned
Lean substrate probe, bounded exact-name search, prohibited-construct hygiene, and whitespace. It
does not validate a canonical theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The author-hosted preliminary edition of Gerald Teschl's *Ordinary Differential Equations and
Dynamical Systems* was retrieved to `/tmp` and inspected at printed pages 255-260. Equations
(9.7)-(9.10) and Theorems 9.3-9.5 distinguish definitions, an exponential-rate graph theorem, a
stable/unstable manifold construction, and a hyperbolic stable-set identification. The Section 9.2
extract has SHA-256 `a0a4aa80...ad56e0`; Crossref confirmed the AMS monograph metadata and DOI
`10.1090/gsm/140`. No download was added to the repository. The catalog does not cite this source,
and no immutable source admission, complete errata or historical audit, or independent H0 review is
claimed.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless `cwd` is
shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1346` | 0 | rank 957; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 9817,9822 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 60 -A 'Mozilla/5.0' -sS 'https://www.mat.univie.ac.at/~gerald/ftp/book-ode/ode.pdf' -o /tmp/thm-m-1346-teschl-ode.pdf` | 0 | retrieved the author-hosted publisher-permitted preliminary edition outside the repository |
| `file`, `wc -c`, and `pdfinfo` on `/tmp/thm-m-1346-teschl-ode.pdf` | 0 | PDF 1.4; 4,133,331 bytes; 364 pages; Teschl title and author metadata |
| `pdftotext -layout /tmp/thm-m-1346-teschl-ode.pdf /tmp/thm-m-1346-teschl-ode.txt` | 0 | text extraction completed |
| `sed -n '13820,14135p' /tmp/thm-m-1346-teschl-ode.txt > /tmp/thm-m-1346-teschl-section-9.2.txt` | 0 | extracted the inspected Section 9.2 setup, definitions, Theorems 9.3-9.5, and proof context |
| `sha256sum /tmp/thm-m-1346-teschl-section-9.2.txt` | 0 | `a0a4aa8051f349eb10eae28160b71c6d030a31973f71bf78b25e791570ad56e0` |
| `rg -n 'Theorem 9\.3\|Theorem 9\.4 \(Stable manifold\)\|Theorem 9\.5' /tmp/thm-m-1346-teschl-section-9.2.txt` | 0 | located all three distinct candidate statements |
| Crossref API query for `10.1090/gsm/140`; `jq` metadata inspection; `sha256sum` | 0 | Teschl title, American Mathematical Society, 2012, DOI confirmed; response SHA-256 `1d7b3155...6a8f2` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...85b1d2` and `321626c8...d81` as recorded in structured artifacts |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1346/IntakeProbe.lean)` | 0 | seven generic integral-curve, flow, invariant-set, fixed-point, orbit, and smooth-embedding APIs elaborated; output SHA-256 `225e8bf5...f661` |
| `rg -n -i --glob '*.lean' 'stable[ _-]*manifold\|unstable[ _-]*manifold\|invariant[ _-]*manifold' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 (expected no match) | no exact stable/unstable/invariant-manifold declaration found in the bounded pinned and repo-local search; not a complete anchor audit or external absence claim |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1346-pycache python3 -m py_compile Stage1_Instances/THM-M-1346/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-1346/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H5/M4/R4 boundary, null formal target, exact artifact inventory, packet agreement, and six open downstream tasks agree |
| `python3 Stage1_Instances/THM-M-1346/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1346 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

## Status boundary

This is provisional worker self-test evidence for `S56-M-1346-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact source selection and independent review,
canonical Lean elaboration and statement mutations, complete anchor audit and discovery freeze,
obligation registry, typed graphs, proof, composition, trust closure, hermetic replay, deterministic
release bundle, and independent verification remain open. These failures prevent statement,
audit-completion, and theorem-completion claims, but they do not invalidate the planned intake.
