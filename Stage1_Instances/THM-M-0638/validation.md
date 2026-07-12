# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

This validation covers target membership, the planned dossier and open task DAG, source-family and
duplicate boundaries, JSON/text integrity, and a narrow pinned Lean API probe. No canonical Lean
expression, statement mutation, proof body, source acceptance, audit completion, or theorem
completion is tested or claimed. The scheduler-provided canonical `.lake` symlink and pinned
artifacts were used read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed. The pre-existing untracked symlink and new owned files make this
nonrelease worker evidence.

## Environment and source observations

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux.
- Lake: `5.0.0-src+98dc76e`.
- mathlib: revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, clean package status.
- Toolchain and dependency-lock SHA-256 values: `651c8acc...b1d2` and `321626c8...2d81`.
- Crossref returned A. Tychonoff, "Ein Fixpunktsatz," *Mathematische Annalen* 111(1), December
  1935, pp. 767-776, DOI `10.1007/BF01472256`.
- Goettingen work `PPN235181684_0111` maps canvas `00000774` to printed p. 770. Its OCR contains
  the section 2 fixed-point theorem quoted in the crosswalk. Observed discovery hashes were
  `b919152a...e85b` for the current IIIF manifest, `6a2cbc3e...596c` for page-770 OCR, and
  `ca0c98da...2043` for the page image. These external files were not added or admitted as H0.

## Exact command record

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0638` | 0 | rank 1055; point-set topology; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` before edits | 0 | only pre-existing `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| scoped repository/source searches for `THM-M-0638`, its Chinese title, gloss, attribution, and year | 0 | sparse target record found; separate `THM-M-0317` record has the same title/author/year and near-identical gloss |
| `git blame` on both repository source records | 0 | both six-line records originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref query for DOI `10.1007/BF01472256` | 0 | bibliographic identity and pagination above confirmed; discovery only |
| Goettingen IIIF manifest/OCR/image inspection for work `PPN235181684_0111`, canvas `00000774` | 0 | printed p. 770 theorem located and quoted; current hashes above; no source acceptance claimed |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update/build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision/tree above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0638/IntakeProbe.lean)` | 0 | seven pinned candidate vocabulary checks elaborated; output SHA-256 `2448892a...caeb`; no target theorem declared |
| bounded `rg` search for Tychonoff/Tikhonov/fixed-point-and-locally-convex patterns in pinned mathlib and repo-local Lean | 0 | only compact-product Tychonoff references plus unrelated uses; no exact target declaration; not an exhaustive anchor audit |
| `python3 -m json.tool` on the owned JSON files and root worker packet | 0 | all valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0638-pycache python3 -m py_compile Stage1_Instances/THM-M-0638/check_intake.py` | 0 | checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0638/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, null target, duplicate boundary, hashes, H1/M4/R4 vector, exact inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0638/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited construct scan over owned Lean | 1 | expected no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| per-new-file `git diff --no-index --check /dev/null <file>` checks plus scoped `git diff --check` | 0 | no whitespace diagnostics; no-index status 1 was accepted only for the expected new-file difference |

## Open gates

The first downstream gate is exact target identity: an independent source reviewer must approve a
complete source crosswalk, and the integration lane must reconcile `THM-M-0638` with the duplicate
`THM-M-0317` catalog record without transferring status. Scalar field, separation, nonemptiness,
continuity scope, domain encoding, exact binders, minimal imports, checked transports, statement
fingerprint, and mutations remain open. So do the formal anchor audit, discovery and obligation
freezes, typed graphs, proof and composition, trust/provenance/readability closure, hermetic replay,
deterministic bundle, independent verification, and master acceptance. These failures prevent any
theorem-completion claim but do not invalidate a truthful self-tested `planned` intake.
