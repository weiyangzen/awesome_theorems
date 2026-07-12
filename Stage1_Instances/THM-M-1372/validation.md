# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, source-family and duplicate discrimination, JSON and scoped invariants, a narrow pinned
Lean substrate probe, bounded repository/mathlib discovery, prohibited-construct hygiene, and
whitespace. It does not validate a canonical Nekhoroshev statement or proof because the catalog
does not select one binder-complete variant.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease. The remote source inspections were discovery work, not hermetic replay or an
accepted source packet.

## Source discovery boundary

The English translation of Nekhoroshev's 1977 paper was obtained from its MathNet record and
inspected at Sections 1.4, 4.1, 4.3, Theorem 4.4, and Remark 4.5. The PDF had 4,420,441 bytes and
SHA-256 `0bfe624cf108096badd7e27fc40ca800e2948b68dce2bf8b9c653e0eaec4def6`. The main theorem's
Part II proof dependency, the approximate nature of introductory Theorem 1.4, and the materially
different modern analytic and finite-regularity variants are recorded in the crosswalk. The
inspected arXiv variant PDFs had SHA-256
`90f0f6b3b3b183b8898f4e961f0127b3a143453f76645d960d3095fda5b9b818` and
`2c1d5fdcb35662a67cd1f1f4098df0aa2f5168a70fb56f640175a177b1fda768`.

No remote input was added to the repository. No catalog source selection, immutable admission,
complete two-part premise/proof/errata map, correction or translation audit, or independent H0
review is claimed.

## Environment

- Linux `7.0.0-27-generic`, `x86_64`; timezone `Asia/Shanghai`.
- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1372` | 0 | rank 982; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 9999,10004 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| MathNet acquisition and bounded PDF inspection of the 1977 English translation | 0 | 65 pages; digest above; located the exact Theorem 4.4 contract, approximate introductory statement, and two-part proof boundary |
| bounded inspection of arXiv `1004.1014v2` and `1002.1804v2` | 0 | confirmed materially different analytic quasi-convex and finitely differentiable contracts; digests above |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above; no dependency-mutating operation run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; status empty |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1372/IntakeProbe.lean)` | 0 | five generic analytic, integral-curve, flow, real-power, and exponential APIs elaborated; complete output SHA-256 `eaa5a19a23fe7d1a5ab1d305b0692aa635d17edb13c93b39c6d4b095c2639128` |
| `rg -n -i --glob '*.lean' 'Nekhoroshev\|near.?integrab\|quasi.?integrab\|steepness' ...` | 0 only for two unrelated uses of `integrable` | no target-specific Nekhoroshev or perturbative-Hamiltonian declaration; bounded intake discovery only, not an exhaustive external audit |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-1372/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1372/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, source pins, null target, H1/M4/R4 boundary, duplicate boundary, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1372/check_intake.py` | 0 | public replay mode passed without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 per new file means only that content differs from `/dev/null` |
| `git diff --check -- Stage1_Instances/THM-M-1372 .stage1-worker-selftest.json` | 0 | no tracked-diff diagnostics; the preceding no-index checks cover untracked files |

## Known downstream failures

- The catalog does not select the original Theorem 4.4 or any other exact variant and supplies no
  cited proposition, complete assumptions, proof boundary, corrections, or independent review.
- The original root depends on a Part II proof boundary not yet mapped; the introductory statement
  is explicitly approximate; modern steep, quasi-convex, analytic, Gevrey, and finite-regularity
  variants are not interchangeable.
- The non-covered `THM-P-0775` semantic duplicate has no accepted identity or ownership decision.
- The Hamiltonian model, dimensions, domains, regularity, nondegeneracy, perturbation norm,
  trajectory convention, constants, drift radius, time scale, conclusion, and boundary cases remain
  open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity and
open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
