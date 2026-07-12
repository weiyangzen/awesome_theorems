# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation ran on 2026-07-13 in
an isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants,
repository and source-lead provenance, pinned environment identity, a narrow Lean API probe,
proof-escape hygiene, and whitespace. The catalog wording omits assumptions needed for one exact
proposition, so elaborating a purported canonical target at intake would infer missing
mathematics. `IntakeProbe.lean` therefore checks adjacent infrastructure only; it introduces no
theorem and supplies no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The external Lean candidate was inspected as downloaded source outside the repository; it was not
installed, built, or added to `.lake`. This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1512` | 0 | rank 1026, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree above |
| `git blame -L 11043,11048 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref lookup for DOI `10.1073/pnas.36.1.48` | 0 | confirmed Nash title, author, PNAS, January 1950, volume 36, issue 1, pages 48-49; response SHA-256 `59eeb4f06cfb8b6a905049948188ac9e587e80e79b6c558073ef8d5a2f56a9f6` |
| Unpaywall lookup for DOI `10.1073/pnas.36.1.48` | 0 | located the PMC scan; response SHA-256 `e8af5122ff05c534843922fa8094b90372433cd424b3805d77cdd5afc02cb227` |
| `file`, `wc -c`, `sha256sum`, `pdfinfo`, and `pdftotext -layout` on the external Nash scan | 0 | PDF 1.3, 2 pages, 206125 bytes; source SHA-256 `5bf21fdad1ab15779fb1d816298ba338b6d30d854938c15e4f41df1b6659ed85`; definitions, countering relation, Kakutani route, and existence conclusion inspected |
| bounded external source search and static inspection of `math-xmum/Brouwer` at commit `c02205edf347ad45f0d62db85497598ba2c4291e` | 0 | located Lean 4.31 `Gametheory/Nash.lean` and `ExistsNashEq`; source SHA-256 `734911160e5fec94607d343c36228b0064de083d6a9b412b9dbe8b66bd962c4b`; not built, axiom-audited, statement-mapped, or integrated |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1512/IntakeProbe.lean)` | 0 | eight pinned simplex, compactness, convexity, PMF, hemicontinuity, and fixed-point APIs elaborated; output SHA-256 `88a971b84acef12822305b629861799ebcd1a3037aa7489484ac273656e69965` |
| bounded Nash/game/Kakutani name search over repo-local and pinned mathlib `*.lean` | 0 | no matching Nash-equilibrium/game-theory or Kakutani terminal declaration in that bounded closure; unrelated payoff/combinatorial-game/Riesz-Markov-Kakutani results rejected |
| four separate `python3 -m json.tool <file>` invocations for the three owned JSON files and `.stage1-worker-selftest.json` | 0 | instance, open task DAG, provisional intake receipt, and worker handoff are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1512-pycache python3 -m py_compile Stage1_Instances/THM-M-1512/check_intake.py` | 0 | scoped intake validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-1512/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/item identity, planned H1/M4/R4 boundary, null target, exact artifact inventory, handoff, source hashes, and six open tasks agree |
| prohibited Lean proof-escape scan over `Stage1_Instances/THM-M-1512` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-1512 .stage1-worker-selftest.json`, per-file new-file checks, and scoped byte-level hygiene assertions | 0; expected no-index new-file differences; 0 | no whitespace diagnostics; all ten changed files have final LF newlines, no CR/NUL bytes, and no trailing spaces or tabs |

## Known downstream failures

- The catalog does not select an exact source proposition. Player and action nonemptiness,
  finiteness encodings, payoff field, mixed-strategy representation, expected payoff, deviation,
  best response, equilibrium, and boundary conventions remain open.
- The inspected 1950 primary lead has no accepted edition/definition/assumption/errata/translation
  crosswalk or independent source review, so it does not establish `H0`.
- No canonical Lean expression, expression or environment hash, exact minimal imports, checked
  alternate encoding, or statement mutation certificate exists.
- The external `ExistsNashEq` source candidate uses Lean 4.31 and another mathlib revision. It has
  no local build, axiom/trust/provenance audit, exact statement transport, pin/import decision, or
  repo-local wrapper and does not upgrade the root from `M4` at intake.
- Discovery protocol, complete anchor audit, obligation registry and typed graphs, proof,
  composition and trust checks, readable reconstruction, hermetic replay, deterministic evidence
  bundle, and independent release verification remain open.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose purpose is to freeze the source-family and ambiguity
boundary and open the downstream DAG. Only the integration lane may accept the provisional worker
receipt.
