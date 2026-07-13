# Intake validation

Base revision: `fd0fab2ab7f4f514a5cc625bbce92879e718ba13` (tree
`4116d53bcf2573069e4b67205353fe3469dbe7bd`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, PDA/CFL theorem-family boundary,
source-statement crosswalk, outside-Stage1 neighbor boundary, open task DAG, JSON/scoped invariants,
and a narrow pinned Lean interface probe. It does not validate a canonical source proposition or
proof because the exact direction, machine model, transition and acceptance semantics, binders,
and boundary cases have not been frozen.

The automation-provided canonical `.lake` symlink was present before editing and used read-only.
No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The pre-existing untracked symlink and owned untracked dossier make this nonrelease worker evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; its package worktree was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- `IntakeProbe.lean` SHA-256:
  `0cdd279090b7275c088ed26d837c48a1b7516d1989d21041b43a2d70a6f6203b`.

## Commands and results

All commands ran from the worker clone root unless a `cwd` is shown.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0764` | exit 0; rank 1350, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD`; `git rev-parse 'HEAD^{tree}'` | pre-edit exit 0; only the automation-provided `Formalizations/Lean/.lake` symlink existed; base revision/tree recorded above |
| inspect the target manifest and execution node, repository source, Stage0 projection, `THM-C-0141`, and pinned CFG/stack-machine sources | exit 0; identified the exact scheduled target, a recognizable but under-specified theorem family, the outside-Stage1 equivalence neighbor, and directly relevant interfaces without transferring statement or proof credit |
| Crossref query for DOI `10.1016/S0019-9958(63)90306-1` and DBLP record query for `Schutzenberger63` | exit 0; confirmed Schuetzenberger, title, journal, volume/issue, September 1963, pages 246-264, DOI, and a Chomsky 1962 reference title; bibliographic discovery only, no source text or H0 credit |
| attempted DuckDuckGo HTML search for Chomsky's 1962 source | curl exit 28; connection timed out, so no source text, statement locator, or source hash was accepted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; pinned Lean and Lake versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision/tree recorded above; empty package status |
| `sha256sum` on pinned `Language.lean`, `ContextFreeGrammar.lean`, and `StackTuringMachine.lean` | exit 0; respectively `f4c3964d5713b752c02906354e5366a8367b94804b4dcdac9b07964c36bb8d2e`, `d0e893c76496af0851a6f669fe5881a106f2158e042d953c15f21f9c836c3f19`, and `c78f9028503580f9dfd42700be75577e18357c496c76b08c2adc7045e85f3246` |
| bounded case-insensitive exact-topic search over repo-local and pinned mathlib Lean sources | exit 1 as expected for no match; no explicitly named pushdown-automaton/PDA or CFG/PDA-equivalence declaration found; intake discovery only, not a global absence or anchor-audit claim |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0764/IntakeProbe.lean)` | exit 0; 16 pinned language, CFG, and general stack-machine interfaces elaborated; no theorem or proof body declared; stdout SHA-256 `feb811e8006470d9309ba96c4f4753b9b2f10b2fcf2954f906d6cf072d62971a` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each; all finalized structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0764-pycache python3 -m py_compile Stage1_Instances/THM-M-0764/check_intake.py` | exit 0; scoped validator compiles without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0764/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; authority identity, source and pin hashes, null target, H1/M3/R4 boundary, neighbor boundary, exact inventory, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0764/check_intake.py` | exit 0; public replay mode passes without the scheduler-only root packet |
| simulated public replay after changing only this intake node to `[_]` in temporary copies of the generated blueprint and authoritative DAG | exit 0; the validator accepts integration-lane projection/state updates while binding the worker evidence to the recorded base snapshot; authoritative files were restored byte-for-byte |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0764` | exit 1 as expected for no match; no prohibited declaration or proof escape |
| `git diff --check -- Stage1_Instances/THM-M-0764 .stage1-worker-selftest.json` plus per-file `git diff --no-index --check /dev/null <new-file>` | exit 0 for the tracked check; every no-index command reported only the expected new-file difference and no whitespace diagnostic |

## Known open gates

- An immutable exact primary or approved authoritative source proposition, incorporated definitions,
  assumptions, conclusion, proof boundary, translation, correction and errata disposition, and
  independent source review remain open.
- Terminal and stack alphabets, grammar and PDA encodings, control-state and transition semantics,
  nondeterminism and epsilon moves, theorem direction, acceptance convention, ordered binders,
  hypotheses, transports, and boundary cases remain open.
- The separate `THM-C-0141` record has no accepted alias or evidence-ownership mapping to this
  target. Its explicit equivalence gloss cannot be copied into this instance.
- The pinned CFG interfaces justify only M3 definition/interface debt; the general deterministic
  multi-stack TM2 model is not a source-matched PDA, and no root conversion or proof is credited.
- Canonical Lean target, minimal imports, elaborated expression and environment fingerprints,
  checked alternate encodings and statement mutations, exhaustive anchor/provenance audit,
  discovery protocol, obligation registry, typed graphs, proof, composition, trust closure,
  readable reconstruction, hermetic replay, deterministic bundle, independent verification, and
  master acceptance remain open.

These failures prevent statement, H0, root-proof, audit-completion, and theorem-completion claims.
They do not invalidate a truthful self-tested `planned` intake.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0764-INTAKE` only. It supports a planned
dossier proposal, not an accepted receipt. No canonical proposition, accepted source, exact Lean
statement, proof body, audit completion, theorem completion, or master acceptance is claimed.
