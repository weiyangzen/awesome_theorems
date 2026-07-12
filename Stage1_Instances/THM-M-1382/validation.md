# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, an authoritative historical source-family inspection, duplicate/neighbor boundaries,
JSON and scoped invariants, a narrow pinned Lean substrate probe, bounded exact-topic search,
prohibited-construct hygiene, and whitespace. It does not validate a canonical theorem statement
or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

The provisional receipt binds SHA-256 values for the eight non-self-referential owned artifacts
and aggregate path-plus-content hashes. The receipt itself and root packet are deliberately outside
that digest boundary; master acceptance must recapture a canonical content-addressed packet.

## Source discovery boundary

The David R. Wilkins 2000 electronic edition of William Rowan Hamilton's 1834 *On a General Method
in Dynamics* was retrieved to `/tmp` from Trinity College Dublin and inspected at Sections 1-3,
especially equations (A)-(B) and Wilkins edition pages 5-6 (original journal pages approximately
251-252). The source distinguishes fixed-energy stationary action from Hamilton's separate law of
varying action and records an action convention different from an unqualified modern `integral L
dt` slogan. The PDF has SHA-256 `4b07c76a...d0065`; the inspected extract has SHA-256
`8ac2ccdd...eb7d1`. Crossref confirmed Hamilton, title, journal, 1834, original pages 247-308, and
DOI `10.1098/rstl.1834.0017`.

The catalog does not cite this source or select a clause. It separately contains same-name or
overlapping mathematics and physics records, with no accepted alias or root-ownership decision.
No immutable source admission, complete historical-to-modern translation, proof/correction audit,
or independent H0 review is claimed.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless `cwd` is
shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1382` | 0 | rank 992; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 10062,10074 -- Docs/researches/math_theorems.md` | 0 | adjacent Maupertuis and THM-M-1382 catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 60 -A 'Mozilla/5.0' -sS 'https://www.maths.tcd.ie/pub/HistMath/People/Hamilton/Dynamics/GenMeth.pdf' -o /tmp/thm-m-1382-tcd.pdf` | 0 | retrieved the Wilkins electronic edition outside the repository; 355,692 bytes; SHA-256 `4b07c76a...d0065` |
| `pdftotext -layout /tmp/thm-m-1382-tcd.pdf /tmp/thm-m-1382-tcd.txt` | 0 | full 4,963-line text extraction completed |
| `sed -n '126,340p' /tmp/thm-m-1382-tcd.txt > /tmp/thm-m-1382-hamilton-sections1-3.txt` | 0 | captured 215 lines / 15,819 bytes containing the source model, equations (A)-(B), least/stationary-action discussion, varying-action boundary, and correction note; SHA-256 `8ac2ccdd...eb7d1` |
| Crossref API query for `10.1098/rstl.1834.0017`; `jq` metadata inspection; `sha256sum` | 0 | Hamilton, full title, journal, 1834, pages 247-308, and DOI confirmed; response SHA-256 `daa6d869...cd9d` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...85b1d2` and `321626c8...2d81` as recorded in structured artifacts |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1382/IntakeProbe.lean)` | 0 | six generic interval fundamental-theorem, integration-by-parts, and local-extremum derivative APIs elaborated; output SHA-256 `9f2242b5...e6b2` |
| exact-topic `rg` over pinned mathlib Lean sources | 1 (expected no match) | no least/stationary-action, Hamilton-principle, Euler-Lagrange, or first-variation occurrence; bounded intake discovery only |
| the same bounded `rg` over repository-local Lean sources | 0 | found foreign-target legacy and related mechanics artifacts; all explicitly excluded from source/statement/proof credit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1382-pycache python3 -m py_compile Stage1_Instances/THM-M-1382/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-1382/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H5/M4/R4 boundary, null formal target, exact artifact inventory, packet agreement, and six open downstream tasks agree |
| `python3 Stage1_Instances/THM-M-1382/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1382 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

## Status boundary

This is provisional worker self-test evidence for `S56-M-1382-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact source selection and independent review,
duplicate/root-ownership resolution, canonical Lean elaboration and statement mutations, complete
anchor audit and discovery freeze, obligation registry, typed graphs, proof, composition, trust
closure, hermetic replay, deterministic release bundle, and independent verification remain open.
These failures prevent statement, audit-completion, and theorem-completion claims, but they do not
invalidate the planned intake.
