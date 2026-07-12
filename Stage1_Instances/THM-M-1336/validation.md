# Intake validation

Base revision: `85da7777da7cc5104d4bc4eaa1d947b8137ca5f5` (tree
`ae4ad4de219b61476e1ed10c008e8139247b9d77`). Validation ran on 2026-07-13 in
an isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants,
repository-source provenance, pinned environment identity, a narrow Lean API probe, proof-escape
hygiene, and whitespace. The source wording is not one proposition, so elaborating a purported
canonical target would invent missing mathematics. `IntakeProbe.lean` therefore checks several
materially different candidate APIs; it introduces no theorem and supplies no statement, anchor,
or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1336` | 0 | rank 947, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree above |
| `git blame -L 9747,9752 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1336/IntakeProbe.lean)` | 0 | seven pinned scalar fencing, Gronwall, approximate/exact trajectory comparison, and uniqueness declarations elaborated; no target declaration |
| bounded comparison/subsolution/quasimonotone/Gronwall search over repo-local and pinned mathlib `*.lean` | 0 | located multiple inequivalent candidate families; intake discovery only, not a complete anchor audit |
| four separate `python3 -m json.tool <file>` invocations for the three owned JSON files and `.stage1-worker-selftest.json` | 0 | instance, open task DAG, provisional intake receipt, and worker handoff are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1336-pycache python3 -m py_compile Stage1_Instances/THM-M-1336/check_intake.py` | 0 | scoped intake validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-1336/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/item identity, planned H5/M4/R4 boundary, null target, exact artifact inventory, handoff, and six open tasks agree |
| prohibited Lean proof-escape scan over `Stage1_Instances/THM-M-1336` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1336 .stage1-worker-selftest.json`, representative `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1336/README.md`, and scoped byte-level hygiene assertions | 0; 1 (expected new-file diff); 0 | no whitespace diagnostics; all ten untracked changed files have final LF newlines, no CR/NUL bytes, and no trailing spaces or tabs |

## Known downstream failures

- The catalog wording is not a stable proposition. No approved source selects scalar fencing,
  sub/supersolution order, an ordered system, a trajectory-distance estimate, or another comparison
  principle, and no review separates the choice from the neighboring Gronwall and Bihari-LaSalle
  targets.
- No independently reviewed immutable primary theorem, complete definition/assumption/proof/errata
  crosswalk, translation review, or theorem locator is accepted.
- No canonical Lean expression, expression/environment hash, exact imports, checked alternate
  encoding, or statement mutation test exists.
- Discovery protocol, complete anchor audit, obligation registry and typed graphs, proof,
  composition and trust checks, readable reconstruction, hermetic replay, deterministic evidence
  bundle, and independent release verification are open.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity boundary and open
DAG. Only the integration lane may accept the provisional worker receipt.
