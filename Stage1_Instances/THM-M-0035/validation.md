# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation ran on 2026-07-13 in the
isolated worker clone.

Validation is limited to target-set consistency, planned-dossier structure, scope and
non-substitution invariants, repository and bibliographic provenance, pinned environment identity,
a narrow Lean candidate-API and axiom probe, bounded exact-topic discovery, proof-escape hygiene,
JSON integrity, and whitespace. Because no exact primary theorem passage and source-to-Lean
transport are accepted, no canonical target, expression hash, statement mutation, source closure,
or root proof is claimed.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

## Environment fingerprint

- Platform: Linux x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0035` | 0 | rank 1018, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git blame -L 270,275 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalogue lines originate at commit `bcf3f9fa...b74f` |
| Crossref lookup for DOI `10.1090/S0002-9947-1945-0011680-8` | 0 | metadata identifies N. Jacobson, title, Trans. AMS 57(2), 1945, pages 228-245; payload SHA-256 `5d7f2b7b...d4ae`; full theorem text not inspected |
| AMS/JSTOR full-text retrieval attempts | nonzero | rate-limited or access-blocked; correctly recorded as an open source gate, with no moving artifact added to the repository |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package worktree clean |
| pinned source and history inspection of `Mathlib/RingTheory/SimpleModule/Basic.lean:562-594` | 0 | `jacobson_density` and its finite surjectivity corollary entered at commit `2396a857...1638`; comment cites Lorenz 2008, Chapter 28, F20 |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0035/IntakeProbe.lean)` | 0 | eight relevant APIs elaborated; both formal candidates report axioms `[propext, Classical.choice, Quot.sound]`; no canonical-root or proof-credit claim |
| bounded exact-topic `rg` over repository and pinned mathlib sources | 0 | only the two pinned candidate declarations and documentation mapping were found; no primitive-ring predicate or repo-local THM-M-0035 artifact; intake discovery only |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| Python `ast.parse` and isolated `py_compile` on `check_intake.py` | 0 | validator parses and compiles without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0035/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, planned H1/M3/R4 state, null target, source and pin hashes, candidate boundary, exact artifact inventory, receipt packet, and six open tasks agree |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0035 .stage1-worker-selftest.json` plus scoped new-file checks | 0 | no whitespace diagnostics in changed files |

## Known downstream failures

- No lawful immutable copy of a primary theorem passage or the cited Lorenz F20 passage has been
  accepted and independently reviewed with definitions, assumptions, conclusion, proof boundary,
  translation, and errata.
- Primitive-ring and module handedness, unitality, faithfulness, endomorphism/op convention,
  independent-family quantifiers, finite topology, boundary cases, and the canonical root form are
  unresolved.
- The pinned semisimple-module theorem and finite surjectivity corollary are strong candidates, but
  no exact source transport, serialized expression/environment fingerprint, checked alternate
  encoding, or four-class statement mutation exists.
- Exhaustive anchor and terminal-body provenance audits, discovery protocol, obligation registry,
  typed graphs, composition, readable reconstruction, hermetic replay, deterministic bundle,
  independent release verification, and master acceptance are open.

These failures prevent statement, source-fidelity, proof, audit-completion, and theorem-completion
claims. They do not invalidate a truthful, self-tested `planned` intake whose purpose is to freeze
the ambiguity and candidate boundaries and open the downstream DAG. Only the integration lane may
accept the provisional worker receipt.
