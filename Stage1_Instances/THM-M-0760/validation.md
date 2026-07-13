# Intake validation

Base revision: `d05520867fab3367a9b61b9544c3e12241204f54` (tree
`fb2cfc62077d5b53e9938632cd6361dd60872067`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation covers target membership, dossier structure, source and candidate crosswalk integrity,
JSON syntax, exact owned-file inventory, and a narrow pinned Lean candidate probe. The source has
not yet selected a unique root strength/domain/encoding, so this is not the statement gate and does
not establish a canonical expression fingerprint, accepted proof body, source fidelity, or theorem
completion. The canonical `.lake` symlink and pinned mathlib artifacts were read only. No update,
build, clone, fetch, or dependency mutation ran.

## Environment and preflight

- Initial worktree status: only the automation-provided untracked
  `Formalizations/Lean/.lake` symlink, preserved read only.
- Lean: 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Mathlib: revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, clean dependency worktree.
- Toolchain and manifest SHA-256: `651c8acc...b1d2` and `321626c8...6d81`.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0760` | 0 | rank 1346; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only the pre-existing `.lake` symlink was untracked |
| `git rev-parse HEAD HEAD^{tree}` | 0 | produced the base revision and tree above |
| repository source/target/name and cross-target searches | 0 | located the terse math row, distinct CS gloss, two Stage0 projections, and no pre-existing owned dossier |
| `git blame` and `git log --follow` over both catalog rows | 0 | both uncited records originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl` AMS version-of-record for Nerode 1958; `file`, `wc -c`, `sha256sum`, `pdfinfo`, `pdftotext` | 0 | inspected 4-page, 378,668-byte PDF; SHA-256 `61c6dea6...9823`; found stream-transformation intrinsic-state Lemma 2, not an exact modern language statement |
| `curl` Crossref DOI metadata for Nerode 1958 | 0 | confirmed author, title, journal 9(4), August 1958, pages 541-544, and DOI |
| `curl` and text extraction for the two PlanetMath entries | 0 | exact secondary finite-alphabet, finite-index, minimum-state, and right-invariance wording observed; HTML hashes recorded in the dossier |
| `cd Formalizations/Lean && lake env lean --version` | 0 | produced the pinned Lean version above |
| `cd Formalizations/Lean && lake --version` | 0 | produced the Lake version above; no update or build ran |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | produced the pinned mathlib revision/tree above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; pinned dependency remained clean |
| `git -C .../mathlib log --follow -- Mathlib/Computability/MyhillNerode.lean` | 0 | located origin commit `3f57df84...` and current file provenance |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0760/IntakeProbe.lean` | 0 | ten candidate interfaces elaborated; exact candidate type printed; axioms reported as `propext`, `Classical.choice`, `Quot.sound` |
| `python3 -m json.tool` on the three owned JSON files and root worker packet | 0 | all JSON syntax valid |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0760-pycache python3 -m py_compile Stage1_Instances/THM-M-0760/check_intake.py` | 0 | scoped validator compiled without writing into the owned path |
| `python3 -B Stage1_Instances/THM-M-0760/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, H5/M3/R4 boundary, null canonical target, source/dependency hashes, receipt, file inventory, packet agreement, and six open tasks passed |
| `python3 -B Stage1_Instances/THM-M-0760/check_intake.py` | 0 | public replay mode passed without requiring the scheduler-only root packet |
| prohibited Lean construct scan over `IntakeProbe.lean` | 1 | expected no-match result; no sorry, admit, sorryAx, axiom, constant, opaque, unsafe, theorem, lemma, or example declaration |
| `git diff --check -- Stage1_Instances/THM-M-0760 .stage1-worker-selftest.json` plus per-file no-index checks | 0 | no whitespace diagnostics |

## Status boundary

This self-test supports only provisional integration review of `S56-M-0760-INTAKE`. Known
downstream failures remain: an independently approved exact source statement; reconciliation of
finite-index versus minimum-state strength and arbitrary versus finite alphabet; a checked
relational/range transport; canonical elaboration and mutations; formal-candidate provenance and
trust audit; obligation/discovery freezes; proof/composition; readable reconstruction; hermetic
replay; deterministic evidence; independent verification; release; and master acceptance.

The first unmet assigned gate is master acceptance of this provisional worker receipt. The first
downstream theorem gate is exact source-statement identity. Neither failure invalidates a truthful,
self-tested `planned` intake, and neither permits a theorem-completion claim.
