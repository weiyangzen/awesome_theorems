# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2` (tree
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, planned-dossier structure and scope invariants,
repository-source provenance, pinned environment identity, a narrow Lean API probe, truth-boundary
inspection, proof-escape hygiene, JSON integrity, and whitespace. It does not validate a canonical
theorem statement. The literal catalog gloss is false without a missing domain or topological
hypothesis, and the catalog does not select one valid repair. `IntakeProbe.lean` therefore checks
restricted candidate declarations and the formal counterexample interface only; it declares no
target theorem and supplies no root proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0221` | 0 | rank 1234, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation `Formalizations/Lean/.lake` symlink was untracked; preserved read-only |
| `git blame -L 1598,1603 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| source and scope inspection | 0 | the catalog supplies no truth-critical domain/interior/homotopy/winding/primitive premise; `f(z)=1/z` on the punctured plane around the unit circle refutes the unrestricted reading; a modern authoritative source lead confirms multiple nonidentical formulations |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake 5.0.0 at the same revision |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0221/IntakeProbe.lean)` | 0 | nine restricted rectangle, circle, primitive, curve-integral, homotopy, and counterexample APIs elaborated; four axiom reports were `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `130573b8...4148` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `python3 -m json.tool` on owned JSON and root worker packet | 0 | all finalized structured artifacts parse as JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0221-pycache python3 -m py_compile Stage1_Instances/THM-M-0221/check_intake.py` | 0 | intake validator compiles without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0221/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, current authority and pin hashes, planned H1/M3/R4 null-target boundary, exact inventory, packet agreement, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0221` | 1 | expected no match; no prohibited declaration in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-0221 .stage1-worker-selftest.json` plus scoped no-index checks for new files | 0 | no whitespace diagnostics |

Known downstream failures remain deliberately open: an immutable and independently accepted exact
source assertion, definitions, premise map, historical attribution and errata review; selection of
one valid rectangle, disk, simply connected, null-homotopic, homological, primitive, or other
source form; exact curve and integral encodings; ordered binders and boundary cases; canonical Lean
elaboration, minimal imports, expression/environment fingerprints, checked transports, and all
statement mutations; full formal anchor and terminal-body audit; discovery and obligation freezes;
typed graphs; proof and composition; source-faithful readable reconstruction; hermetic replay;
deterministic bundling; independent verification; and master acceptance.

These failures prevent statement, H0, exact proof, audit-completion, and theorem-completion claims.
They do not invalidate a truthful self-tested `planned` intake. Only the integration lane may
accept the provisional worker receipt.
