# Intake validation

Base revision: `300a2745fe5f7351353cca57a5fdb8ad2325458c`; base tree:
`f28a7c551a8f3600b3a402791362affb691ab478`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, source-family discrimination, JSON and scoped invariants, a narrow pinned Lean substrate
probe, a bounded repo-local and mathlib search, prohibited-construct hygiene, and whitespace. It
does not validate a canonical theorem statement or proof because the catalog supplies no stable
truth-valued proposition.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The strongest historical lead is Jacobi's 1837 Crelle article, DOI
`10.1515/crll.1837.17.97`. The inspected 67-page GDZ scan had SHA-256
`181ce79c830b5ca538509733f7128eef99009f3f88326de69688879bcd69fdef`; printed page 114 discusses
a complete parameterized solution of a first-order PDE and integration of the associated equations
of motion. An Encyclopedia of Mathematics revision and the abstract of Samelson's 2001 article
converge on the complete-integral-to-Hamiltonian-trajectories family. Tong's *Dynamics*, Section
4.7, was inspected for the adjacent chain-rule and autonomous-solution boundaries; its PDF had
SHA-256 `b65ba2b0399df6b02ca3850e5c69ee0255c3011a35664e80766349f521e43e80`.
These temporary discovery inputs were not added to the repository. No exact theorem/proof
transcription, complete correction/errata audit, immutable source admission, or independent `H0`
review is claimed.

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
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1380` | 0 | rank 990; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 10055,10060 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git rev-parse bcf3f9fa79ab8c2b6610c9875668c2589b35b74f:Docs/researches/math_theorems.md` | 0 | source-record blob `5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf` |
| bounded inspection of the Jacobi 1837 GDZ scan, Encyclopedia of Mathematics revision, Samelson abstract, and Tong notes | 0 | source-family discrimination only; observed digests and boundaries are recorded above and in the crosswalk |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1380/IntakeProbe.lean)` | 0 | seven adjacent smoothness, Frechet-derivative, product-map, and integral-curve APIs elaborated; output SHA-256 `b319d6c1b42bc96e54cd518d90f2b5d5f1092c00d251b24508662f42806bf247` |
| bounded case-insensitive exact-topic search over pinned mathlib and repo-local Lean | 0 | only unrelated commutative-algebra uses of `completeIntegralClosure`; no Hamilton-Jacobi occurrence; intake discovery only, not an exhaustive anchor audit or global absence claim |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-1380/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1380/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H5/M4/R4 boundary, null formal target, exact inventory, worker packet, source hashes, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1380/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1380 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- The title and gloss do not select one stable proposition. No repository-selected primary source,
  exact theorem, incorporated definitions, assumptions, proof boundary, correction decision, or
  independent source review exists.
- Complete integral, phase/configuration/parameter spaces, regularity, time dependence,
  independence condition, locality, canonical-transformation or trajectory conclusion, sign
  conventions, quantifier order, and boundary cases remain open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity and
open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
