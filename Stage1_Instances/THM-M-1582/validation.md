# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2`; base tree:
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, 1963/1965 source discrimination, JSON and scoped invariants, a narrow pinned Lean
substrate probe, a bounded repo-local and mathlib search, prohibited-construct hygiene, and
whitespace. It does not validate a canonical theorem statement or proof because the catalog gives
a minimum-description concept rather than one truth-valued proposition.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The MathNet.Ru record and full Russian scan of A. N. Kolmogorov's 1965 paper *Three Approaches to
the Definition of the Concept "Quantity of Information"* were inspected. The record gives volume
1, issue 1, pages 3-11, Russian language, and receipt date 9 January 1965. The 986,818-byte,
nine-page scan has SHA-256
`77a10807916f52dd48d5eac07e26fd471738f47b6307f3259c3b1787052abab8`; extracted text has SHA-256
`7835a81c189ad7c591a1903ca6a58e725186bbf73480e5d32e42eb723d1149f9`.

Section 3 and its main theorem were inspected. They distinguish the minimum-program definition,
existence of an asymptotically optimal partial recursive description method, and the resulting
additive invariance. The paper cites the 1963 random-table article as an incomplete precursor.
This supports source-family discrimination only. The catalog cites neither paper and does not
select the 1965 theorem; no accepted translation comparison, correction and errata audit,
complete premise mapping, target correction, or independent `H0` review is claimed.

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

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1582` | 0 | rank 1204; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 11658,11663 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| retrieval of MathNet.Ru metadata and full text to temporary worker storage | 0 | 23,998-byte metadata response and 986,818-byte, nine-page Russian PDF; neither added to the repository |
| `pdftotext -layout <temporary-1965-scan> <temporary-extract>` | 0 | extracted 37,809 bytes; Section 3 main theorem and proof inspected; digests recorded above |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1582/IntakeProbe.lean)` | 0 | nine encoding, partial-recursive-code, evaluator, universality, and Turing APIs elaborated; complete output SHA-256 `e43d09fc44386892c23f6db5bd140eb7f84df8ba348dafcf72d6a3695714f4ed` |
| bounded exact-topic search over pinned mathlib and repo-local Lean | 1 (expected no match) | no Kolmogorov-complexity, algorithmic-complexity, description-length, or shortest-program declaration matched; discovery only |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-1582/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1582/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H5/M4/R4 boundary, null target, source/neighbor boundaries, inventory, hashes, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1582/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| scoped prohibited-construct scan over `Stage1_Instances/THM-M-1582/*.lean` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1582 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- The catalog supplies a definition-like gloss, not a truth-valued proposition, and does not select
  optimal-description existence, invariance, noncomputability, incompressibility, or another root.
- Its 1963 date refers naturally to the random-table precursor, while the inspected mature
  shortest-program definition and optimality theorem are from 1965; no target correction is
  accepted.
- The Russian source scan is not an independently approved `H0` packet; complete translation,
  incorporated-definition, premise, proof-boundary, correction, and errata mapping remain open.
- Computation model, object/program domains, encodings, complexity convention, universality,
  additive-constant dependency, binder order, conclusion, and boundary cases remain open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked model
  transport, or statement mutation is frozen.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

These failures block ordinary statement and theorem execution. They do not invalidate a truthful,
self-tested `planned` intake whose purpose is to freeze the source defect, scope choices, and open
DAG. Only the integration lane may accept the provisional worker receipt.
