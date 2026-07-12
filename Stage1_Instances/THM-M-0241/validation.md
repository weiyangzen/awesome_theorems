# Intake validation

Base revision: `dd8846dbc83818f6ba7124151d5d4b7b29bb5b0d`; base tree:
`1bf3680085cf7338ac4d405cf4ef2188fa14ccec`.

This validation covers target membership, the planned dossier and open task DAG, source-record
provenance, JSON and scoped invariants, a narrow pinned Lean substrate probe, prohibited-construct
hygiene, and whitespace. It does not validate a canonical theorem statement or proof. The initial
worktree contained only the automation-provided untracked `Formalizations/Lean/.lake` symlink; it
was used read-only and not modified.

## Source discovery boundary

The AMS copy of Hilbert's 1902 English publication was retrieved to `/tmp`, inspected at printed
pages 470-471, and hashed. It supports the historical problem-family crosswalk only. Crossref
metadata was also checked for the Hilbert publication and Bolibrukh's 1990 survey. No downloaded
file was added to the repository, and no primary proof, correction theorem, or H0 source review is
claimed.

## Commands and results

All repository commands ran at the repository root unless `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0241` | 0 | rank 941; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD` / `git rev-parse HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 1738,1743 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0' -sS 'https://www.ams.org/journals/bull/1902-08-10/S0002-9904-1902-00923-3/S0002-9904-1902-00923-3.pdf' -o /tmp/hilbert1902.pdf` | 0 | retrieved the AMS-hosted discovery copy outside the repository |
| `file /tmp/hilbert1902.pdf`; `wc -c /tmp/hilbert1902.pdf`; `sha256sum /tmp/hilbert1902.pdf`; `pdfinfo /tmp/hilbert1902.pdf`; `pdftotext -layout /tmp/hilbert1902.pdf /tmp/hilbert1902.txt`; `rg -n -i -C 10 'prescribed monodrom\|monodromic group\|twenty-first\|differential equations' /tmp/hilbert1902.txt`; `sed -n '1575,1635p' /tmp/hilbert1902.txt` | 0 each | 43-page, 4,596,239-byte PDF; SHA-256 `e5d069ad0d3644b2527737b67d7bf293fd2cb8acc576f1dbe8f19e12059bd2b3`; Problem 21 inspected at printed pages 470-471 |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0' -sS 'https://api.crossref.org/works/10.1090/S0002-9904-1902-00923-3' \| jq '.message \| {title:.title,author:.author,published:.published,container:."container-title",volume:.volume,issue:.issue,page:.page,DOI:.DOI,URL:.URL}'` | 0 | Hilbert, *Mathematical problems*, Bulletin AMS 8(10), 1902, pages 437-479 |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0' -sS 'https://api.crossref.org/works/10.1070/RM1990v045n02ABEH002350' \| jq '.message \| {title:.title,author:.author,published:.published,container:."container-title",volume:.volume,issue:.issue,page:.page,DOI:.DOI,URL:.URL}'` | 0 | Bolibrukh, *The Riemann-Hilbert problem*, Russian Mathematical Surveys 45(2), 1990, pages 1-58; metadata only |
| the preceding two Crossref `curl` commands with `-o /tmp/hilbert-crossref.json` and `-o /tmp/bolibrukh-crossref.json`, followed by `sha256sum` and `wc -c` on each file | 0 | response hashes and byte counts recorded in the provisional receipt |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...85b1d2` and `321626c8...d81` as recorded in structured artifacts |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0241/IntakeProbe.lean)` | 0 | five pinned punctured-sphere, fundamental-group, general-linear-group, and monodromy-representation type checks elaborated; no target theorem stated |
| `python3 -m json.tool Stage1_Instances/THM-M-0241/instance.json`; same command for `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | all structured records valid after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0241-pycache python3 -m py_compile Stage1_Instances/THM-M-0241/check_intake.py` | 0 | scoped checker compiles without writing inside the owned path |
| `python3 Stage1_Instances/THM-M-0241/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, planned lifecycle, H5/M4/R4 boundary, null formal target, exact inventory, receipt packet, and six open tasks agree |
| `python3 Stage1_Instances/THM-M-0241/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet; it permits authoritative intake state `[ ]` or `[_]` but still requires no accepted theorem state |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0241` | 1 (expected no match) | no prohibited Lean proof escape or declaration |
| `for f in Stage1_Instances/THM-M-0241/* .stage1-worker-selftest.json; do output=$(git diff --no-index --check /dev/null "$f" 2>&1) || code=$?; test "${code:-0}" -le 1 && test -z "$output" || exit 1; unset code; done` | 0 | no whitespace diagnostics for any untracked new file; `git diff --no-index` returns 1 merely because each file is new |
| `git diff --check -- Stage1_Instances/THM-M-0241 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0241-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact source selection and independent review,
canonical Lean elaboration and mutation tests, anchor audit, discovery and obligation freezes,
typed graphs, proof, composition, trust closure, hermetic replay, deterministic release bundle,
and independent verification remain open. They prevent theorem completion but do not invalidate
the planned intake.
