# THM-M-0025 intake validation

Base revision: `d750776142c633e42858cebfc67c5c2664d419d7`; base tree:
`7e62c62f1939b5cb668e56590b709f71f6e676b5`. Validation date: 2026-07-13
(Asia/Shanghai); exact timestamps are recorded in the provisional receipt.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, the modern commutative one-variable scope selection, JSON/scoped invariants, a narrow
pinned Lean API probe, prohibited-construct hygiene, and whitespace. It does not pass the formal
statement gate, source gate, anchor audit, or proof gate.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned files and worker packet make this nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source boundary

Crossref bibliographic metadata confirmed Hilbert's 1890 article and DOI recorded in the
crosswalk. No historical primary text was admitted or inspected, so no exact theorem/page,
definition transport, assumption map, proof boundary, translation, errata result, or independent
review is claimed. Stacks Project tag `00FN` was inspected as an authoritative modern secondary
cross-check; its exact polynomial specialization agrees with the intake-selected claim but cannot
establish historical source fidelity.

## Commands and results

All commands ran at the repository root unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0025` | 0 | rank 1070; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 200,205 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref metadata request for DOI `10.1007/BF01208503` | 0 | historical bibliographic lead confirmed; no primary source admitted and no H0 credited |
| Stacks Project tags `00FM` and `00FN` inspection | 0 | modern definition and polynomial specialization cross-checked; secondary evidence only |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above; package status clean |
| `sha256sum` on authoritative manifests, source records, toolchain, lock, and three probed mathlib modules | 0 | hashes recorded in `instance.json` and replay-checked by `check_intake.py` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0025/IntakeProbe.lean)` | 0 | seven Noetherian-ring and polynomial APIs elaborated, including the exact candidate type; no target declaration or proof credit |
| `python3 -m json.tool` on all structured owned files and the root packet | 0 | valid JSON after finalization |
| `python3 -c` with `ast.parse` on `check_intake.py` | 0 | scoped checker parsed without bytecode output |
| `python3 -B Stage1_Instances/THM-M-0025/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, source/dependency hashes, H1/M3/R3 boundary, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0025/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for each owned file and worker packet | 0 aggregate | no whitespace diagnostics; exit 1 from each no-index invocation was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0025 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; per-file checks cover untracked files |

## Known open gates

Pinpoint primary-source admission and statement/proof mapping, modern-to-historical terminology
transport, corrections/errata audit, and independent source review remain open. So do canonical
Lean elaboration and fingerprints, checked transports, four statement mutation classes,
exhaustive anchor and proof-body audit, discovery protocol, obligation registry and typed graphs,
proof/composition/source/provenance/trust closure, readable proof reconstruction, hermetic replay,
deterministic release evidence, independent verification, master acceptance, audit completion, and
theorem completion.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0025-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No H0, M0, R0, proof, audit completion, theorem completion,
or master acceptance is claimed.
