# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2` (tree
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source-statement and scope
boundaries, the open downstream DAG, JSON/scoped invariants, and a narrow pinned Lean API probe. It
does not validate a canonical Omega statement or proof because the source result and all
proposition-changing conventions remain open. The automation-provided `.lake` symlink was
pre-existing and used read-only; no update, build, clone, fetch, or dependency mutation was run.
This dirty worker evidence is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1584` | exit 0; rank 1206, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | pre-edit exit 0; only the automation-provided `Formalizations/Lean/.lake` symlink existed; base revision/tree recorded above |
| `git blame -L 11672,11677 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref queries for DOI `10.1145/321892.321894` and `10.1038/scientificamerican0575-47`, plus DBLP record retrieval | exit 0; two exact author/year source leads recorded; response hashes `29ba813f...6456`, `911c8ada...6402`, and `67c7384b...23f8f`; metadata only, no H0 |
| publisher PDF request for DOI `10.1145/321892.321894` | curl exit 22 after HTTP 403; no full text accepted and no primary theorem-page claim made |
| `curl ... https://arxiv.org/pdf/1707.08109v5`, `pdftotext`, scoped inspection, and hashes | exit 0; secondary survey defines the machine-indexed family and attributes randomness to Chaitin 1975; PDF SHA-256 `a5d9f7f4...f26b`, text SHA-256 `98fbc714...c0f7`; scope evidence only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision/tree recorded above; empty package status |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1584/IntakeProbe.lean)` | exit 0; seven adjacent partial-recursive, halting, unique-decoding, and Kraft-McMillan APIs elaborated; complete output SHA-256 `683a3c55c42ba4e2a7f8e8f06c2fb7bf434d97fd8a3e065f1d9219ad531728da`; no target declaration or proof body |
| bounded case-insensitive exact-topic `rg` over repo-local Lean and pinned mathlib | exit 1 as expected for no match; no Chaitin/Omega/halting-probability/prefix-free-machine/algorithmic-randomness target found; intake discovery only |
| `python3 -m json.tool` on all owned JSON and worker packet | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1584-pycache python3 -m py_compile Stage1_Instances/THM-M-1584/check_intake.py` | exit 0; scoped validator compiled without adding generated owned files |
| `python3 -B Stage1_Instances/THM-M-1584/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; target/DAG identity, null canonical target, H1/M4/R4 boundary, source hashes, inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1584/check_intake.py` | exit 0 after finalization; public replay mode passes without the scheduler-only worker packet |
| prohibited-declaration `rg` over owned Lean | exit 1 as expected for no match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1584 .stage1-worker-selftest.json` plus per-file `git diff --no-index --check /dev/null FILE` | exit 0 for tracked check; expected new-file differences had no whitespace diagnostic |

## Known open gates

Lawful primary full-text admission, exact definition/result locator, complete premise/conclusion/
proof-boundary/errata crosswalk, and independent source review remain open. So do machine,
prefix-free, universality, halting-probability, exact-real computability, quantifier, and boundary
choices; the canonical Lean expression and mutations; checked alternate encodings; discovery
protocol; obligation registry and typed graphs; exhaustive formal anchor/provenance audit; proof and
composition; trust closure; readable reconstruction; hermetic replay; deterministic evidence
bundle; independent verification; master acceptance; audit completion; and theorem completion.
These failures do not invalidate a truthful self-tested `planned` intake.
