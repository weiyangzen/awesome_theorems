# THM-M-1585 intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2`; base tree:
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, umbrella-versus-neighbor discrimination, JSON and scoped invariants, a narrow pinned
Lean API probe, a bounded repo-local and mathlib search, prohibited-construct hygiene, and
whitespace. It does not validate a canonical theorem statement or proof because the catalog does
not supply one truth-valued coding-theory proposition.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source boundary

`Docs/researches/math_theorems.md:11679-11684` supplies only the title, many-mathematicians
attribution, 20th-century date, noun-phrase gloss, importance, and untrusted status. All six lines
originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Stage0 repeats them while leaving every
statement and evidence component open. The separate computer-science taxonomy enumerates many
distinct bounds and code families but no theorem named merely coding theory. No external source
was fetched or admitted, and no H0 claim is made.

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
| `python3 scripts/stage1_target.py show THM-M-1585` | 0 | rank 1207; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 11679,11684 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1585/IntakeProbe.lean)` | 0 | nine generic Hamming/source-code APIs elaborated; `hammingDist_triangle` and Kraft-McMillan report `propext`, `Classical.choice`, `Quot.sound`; `flatten_injective` reports no axioms; stdout SHA-256 `a62fc48c537ee4733a0de3d1a94b54c20fc2d9311102641b9ba966ad3a0a51a2` |
| bounded exact-topic search over pinned mathlib and repo-local Lean | 0 | 13 adjacent lexical matches in generic Hamming/source-code documentation and unrelated phrases; no general canonical coding-theory declaration; discovery only |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-1585/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1585/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H5/M4/R4 boundary, null target, source/neighbor boundaries, inventory, packet, hashes, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1585/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| `rg -n -i --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-1585` | 1 (expected no match) | no prohibited declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null FILE` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1585 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

## Known downstream failures

- The catalog is a discipline label with no primary source, theorem locator, mathematical formula,
  ordered binders, hypotheses, conclusion, or independently reviewed correction.
- Selecting or conjoining Hamming, Singleton, Gilbert-Varshamov, linear/cyclic/algebraic codes,
  Kraft-McMillan, decoder correctness, or Shannon coding would substitute neighboring scope.
- No canonical Lean expression, exact minimal imports, expression/environment fingerprint, checked
  alternate encoding, or mutation suite is frozen.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity and
open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
