# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, the overlapping-target boundary, JSON and scoped invariants, a narrow pinned Lean
substrate probe, a bounded exact-topic search, prohibited-construct hygiene, and whitespace. It
does not validate a canonical theorem statement or proof. The catalog supplies a recognizable
classical theorem gloss, but no independently reviewed exact source or formal presentation.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source and duplicate boundary

The catalog record was traced to its uncited introduction commit. Official metadata identifies
Washington's Chapter 14, "The Kronecker-Weber Theorem," pages 321-331, and supports the broad
containment wording; Marcus remains a secondary comparison lead. No immutable full source edition
or exact theorem and proof passage within the chapter was admitted, and no H0 assumption, proof,
errata, or node review was performed.

`THM-M-0419` remains a separate authoritative target. Its historical statement-shape module was
read but not changed, imported, or credited. The complete claim in `THM-M-0014` and the shorter
gloss in `THM-M-0419` were not merged by the repository's exact-record deduplication. Reconciliation
is therefore a governance and source-review task, not an intake inference.

## Environment fingerprint

- Platform: Linux 7.0.0-27-generic, x86_64, Asia/Shanghai.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0014` | 0 | rank 1064; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 121,126 -- Docs/researches/math_theorems.md` | 0 | all six uncited source-record lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0014/IntakeProbe.lean)` | 0 | seven adjacent APIs elaborated; complete output SHA-256 `8bbad9b0aa382865b712243cbdc30156139c4a86f2880422962ad0ea2c7fc028`; this probe states no target theorem |
| `rg -n -i --glob '*.lean' 'kronecker.?weber\|kroneckerweber' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 0 | matches only the explicitly nonterminal repo-local sibling module; no pinned-mathlib terminal occurrence in this bounded discovery search |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0014/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0014/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | planned H1/M4/R3 boundary, null formal target, duplicate boundary, exact inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0014/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0014 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- No catalog-cited immutable primary or authoritative proof source, exact theorem/page, complete
  assumptions, proof boundary, errata audit, node mapping, or independent source review exists.
- The separate `THM-M-0419` record overlaps this theorem family but is not an authorized alias;
  its statement shape and evidence cannot be transferred.
- Literal subfield inclusion, abstract algebra embedding, intermediate-field equivalence,
  finiteness and abelian-Galois packaging, cyclotomic algebra structure, index and conductor
  conventions, quantifier order, exact conclusion, and boundary cases remain open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen for this target.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable proof reconstruction, hermetic replay, deterministic bundle, independent
  release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to preserve the source scope,
ownership boundary, and open work. Only the integration lane may accept the provisional receipt.
