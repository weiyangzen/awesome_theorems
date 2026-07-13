# Intake validation

## Boundary

This is nonrelease evidence for the `planned` intake node only. The worker clone began at commit
`fd0fab2ab7f4f514a5cc625bbce92879e718ba13`, tree
`4116d53bcf2573069e4b67205353fe3469dbe7bd`, with only the automation-provided
`Formalizations/Lean/.lake` link untracked. That link resolves to the canonical pinned dependency
artifacts and was used read-only. No `lake update`, `lake build`, clone, fetch, dependency edit, or
other `.lake` mutation was performed.

The Lean probe authenticates adjacent language and Turing-machine interfaces only. It does not
define an LBA or context-sensitive grammar, elaborate a canonical theorem, or prove a language-class
result. Remote metadata, publisher preview, and OCR are discovery observations rather than an
accepted source edition or review. The receipt is unsigned and non-content-addressed; only the
integration lane can accept the intake node.

## Commands and results

All commands were run from the repository root unless a `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0766` | 0 | rank 1352; planned; L0/rework required; no legacy slot; legacy artifacts unaccepted; theorem complete false |
| `git status --short --untracked-files=all` (pre-edit) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | commit and tree shown above |
| `git blame -L 5640,5645 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over the manifest, blueprint, DAG, skill, guidelines, both source corpora, Stage0, toolchain, lockfile, and pinned Lean sources | 0 | hashes agree with `instance.json` and `intake-receipt.json` |
| `lake env lean --version` (`cwd=Formalizations/Lean`) | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `lake --version` (`cwd=Formalizations/Lean`) | 0 | Lake 5.0.0-src+98dc76e; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `lake env lean ../../Stage1_Instances/THM-M-0766/IntakeProbe.lean` (`cwd=Formalizations/Lean`) | 0 | twelve adjacent language, tape, TM0, reachability, evaluation, support, and finite TM2 interfaces elaborated; no target theorem declared; stdout SHA-256 `e87dc22e0f0f4423a8d51bb494b1b2ce6d303303ef7ba0fbc4a5e1249e8eb82b` |
| `rg -n -i --glob '*.lean' 'linear.?bounded\|context.?sensitive\|Kuroda\|Ginsburg\|Greibach\|LBAs?\b' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/.lake/packages/mathlib/Archive` | 0 | all matches were unrelated: Ginsburg citations about Presburger-semilinear languages and one multilinear-bounded import; bounded discovery found no matching LBA/CSL declaration |
| Crossref DOI queries for Kuroda 1964, Landweber 1963, Stanley's 1967 review of Landweber, Landweber's 1967 review of Kuroda, and Ginsburg/Greibach 1966 | 0 | bibliographic identities and chronology confirmed; exact response hashes are in the receipt |
| `curl -L --max-time 60 -sS` on the Cambridge publisher page and page-116 preview | 0 | preview is a 503241-byte JPEG, SHA-256 `539484228ceb87f45a18f519e8965583c83b0c44aa542889ff1b3eab1cb17af8`; it distinguishes the deterministic one-way theorem from Kuroda's nondeterministic equivalence |
| `python3 -m json.tool` on all owned JSON and the root worker packet | 0 | valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/thm-m-0766-pycache python3 -m py_compile Stage1_Instances/THM-M-0766/check_intake.py` | 0 | scoped validator compiled with bytecode redirected outside the repository |
| `python3 -B Stage1_Instances/THM-M-0766/check_intake.py` | 0 | planned intake invariants, exact nine-file inventory, source pins, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0766/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | worker handoff agrees with the provisional receipt and scoped artifacts |
| prohibited Lean escape scan for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` | 1 | expected no match |
| `git diff --check -- Stage1_Instances/THM-M-0766 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics; scoped checker also covers final newlines and trailing whitespace |

## Result

The intake deliverable is self-tested and may be proposed as worker state `[_]`. Its provisional
vector is `[H5, M4, R4]`. The first unmet node gate is integration-lane review and master acceptance
of a node-specific receipt. The received target must also be corrected into a stable proposition
before ordinary statement or proof execution: exact source selection, attribution repair,
canonical Lean elaboration, source/formal anchor audit, obligation freeze, proof, trust closure,
readable reconstruction, hermetic validation, and release all remain downstream. Consequently
`audit_complete=false` and `theorem_complete=false`.
