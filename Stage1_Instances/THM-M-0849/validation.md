# Intake validation

Base revision: `444860f481e8bbf64a3357008fd4d01a52006f08` (tree
`dee24a14497f877ebd81712a99d2da08de62d7ad`). Validation date: `2026-07-13`
(`Asia/Shanghai`).

Validation is limited to target membership, repository-standard consistency, dossier structure,
primary-source family inspection, planned-state invariants, immutable input checks, a narrow pinned
Lean substrate probe, bounded discovery, proof-hole hygiene, JSON, and whitespace. The catalog does
not select a proposition, so an invented phase-transition expression would be substitution rather
than validation. No canonical target, expression fingerprint, mutation certificate, theorem
declaration, or proof is claimed.

The automation-provided `Formalizations/Lean/.lake` symlink exposes canonical pinned artifacts. It
existed before this work and was used read-only. No `lake update`, `lake build`, dependency clone or
fetch, or other `.lake` mutation was run. The owned files and root worker packet make this
worktree dirty and nonrelease.

## Primary-source inspection

The official 45-page scan of Erdos and Renyi's *On the Evolution of Random Graphs* was downloaded
in bounded HTTP byte ranges to temporary storage because ordinary transfer was unreliable. The
assembled PDF was checked with `sha256sum`, `pdfinfo`, `pdftotext`, bounded text searches, and
visual renderings of journal pages 17, 49-50, 52-53, and 56. Its size is 5,680,595 bytes and its
SHA-256 is `374daa0f45a834733e61622c5942a5f1dd4362bda1fff850b2c3ec01de9397da`.
The source bytes and tool-dependent extracted text were not added to the repository.

The inspection verifies the source family and page crosswalk in `source-statement-crosswalk.md`.
It does not select the catalog's root, perform a complete errata audit, or supply independent source
review. Consequently it does not establish `H0`.

## Environment fingerprint

- Platform: Linux 7.0.0-27-generic, x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

Commands ran from the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0849` | 0 | rank 1404, planned, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was present |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6229,6234 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git log -S'THM-M-0849 相变现象' ... -- Docs/Stage0_Blueprint.md` | 0 | target ID appears in deduplication commit `c61be3c80710c07c5f7626e3404e51f40ecb39a6` |
| ranged `curl` download of `https://www.renyi.hu/~p_erdos/1960-10.pdf`, assembly, `sha256sum`, `pdfinfo`, and `pdftotext -layout` | 0 | official PDF size/hash/page count above; extracted-text SHA-256 `37e1b44e2be77d81699e5fd41010d3c8c28cc323ab050b9b3412e7ba10459acc` |
| bounded extracted-text inspection plus visual render inspection of journal pages 17, 49-50, 52-53, and 56 | 0 | fixed-edge model, almost-all convention, critical scale, three-regime double jump, and supercritical formula agree with the crosswalk |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake agree with the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree agree with the fingerprint; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0849/IntakeProbe.lean)` | 0 | nine binomial-random-graph and connected-component APIs elaborated; complete stdout SHA-256 `84d48f03f55d3cf159fad639b89cee429f184521c8ad2fcd2569d82d89bae7c4`; no target theorem stated |
| `rg -n -i --glob '*.lean' 'phase.?transition.*(random graph\|component)\|(random graph\|component).*phase.?transition\|giant.?component' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 | expected no-match result; bounded exact-topic discovery only, not an exhaustive anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| Python `ast.parse` on `check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0849/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, source pins, H5/M4/R4 boundary, null target, exact inventory, provisional receipt, worker packet, and six open tasks agree |
| prohibited-construct scan over `Stage1_Instances/THM-M-0849/*.lean` | 1 | expected no-match result: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped final-newline, byte, and trailing-whitespace check over all owned files and worker packet | 0 | all ten files passed |
| `git diff --check -- Stage1_Instances/THM-M-0849 .stage1-worker-selftest.json` and per-new-file `git diff --no-index --check` | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each file is only the expected new-file difference |

## Known open gates

The exact source root, incorporated results, independent source and errata review, relation to
`THM-M-1113`, graph model, checked model transport, ordered binders, probability statement,
component observable, uniqueness strength, constants, and boundary cases remain open. So do the
canonical Lean expression and environment fingerprints, checked alternate encodings and statement
mutations, exhaustive formal anchor audit, discovery and obligation freezes, typed graphs, proof,
composition, trust closure, readable reconstruction, hermetic replay, deterministic evidence
bundle, independent verification, and master acceptance.

These open gates prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake proposal whose purpose is to freeze the ambiguity and open the
downstream DAG. Only the integration lane may accept the provisional worker receipt.
