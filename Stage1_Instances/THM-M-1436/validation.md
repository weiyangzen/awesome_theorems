# Intake validation

Base revision: `d1bb69e506d568ec4852bd68cc5bda1d61702852` (tree
`d9681ef41935162296b57b0170641d66404a53a9`). Validation ran on 2026-07-12 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, source
provenance, two bibliographic metadata leads, pinned environment identity, a narrow Lean API probe,
a bounded local name search, proof-escape hygiene, and whitespace. The source wording is not a
proposition, so elaborating a purported canonical Lean target would invent missing mathematics.
`IntakeProbe.lean` therefore checks only possible substrate; it introduces no theorem and supplies
no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

## Environment fingerprint

- Platform: Linux x86_64; worker timezone `Asia/Shanghai`.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1436` | 0 | rank 934, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git blame -L 10488,10493 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '10488,10493p' Docs/researches/math_theorems.md \| sha256sum` | 0 | exact catalog block SHA-256 `0bb268ed333f3f26043f5c53e0a31dc8b2a071b25236f4a1871d96f905463d5b` |
| Crossref API query for DOI `10.1007/BF01020332` with a compact `jq` projection | 0 | Feigenbaum, title, Journal of Statistical Physics 19(1), pp. 25-52, 1978; bibliographic ambiguity evidence only |
| Crossref title/author query for *Complex Dynamics and Renormalization* with a compact `jq` projection | 0 | McMullen book metadata and DOI `10.1515/9781400882557`; a distinct bibliographic lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1436/IntakeProbe.lean)` | 0 | thirteen generic pinned iteration, semiconjugacy, fixed/periodic-point, homeomorphism, and continuous-map APIs elaborated; no target declaration |
| bounded renormalization/Feigenbaum/unimodal/quadratic-like target-name search over repo-local and pinned-mathlib `*.lean` | 0 | only three unrelated peak-function renormalization text matches; no dynamical target match; intake discovery only, not an exhaustive anchor audit |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | instance, open task DAG, provisional receipt, and worker handoff are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1436-pycache python3 -m py_compile Stage1_Instances/THM-M-1436/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-1436/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/item identity, pinned inputs, planned H5/M4/R4 boundary, null target, artifact hashes, handoff, and six open tasks agree |
| prohibited Lean proof-escape scan over `Stage1_Instances/THM-M-1436` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped `git diff --check` plus no-index checks for every untracked changed file | 0 | no whitespace diagnostics |

## Known downstream failures

- The catalog wording is not a stable proposition. No approved correction selects the dynamical
  category, map class, return construction, rescaling, normalization, combinatorics, operator
  space, hypotheses, conclusion, or boundary cases.
- No independently reviewed immutable primary theorem, complete definition/assumption/proof/errata
  crosswalk, catalog-identity justification, or theorem locator is accepted. The two bibliographic
  leads demonstrate distinct readings and receive no source credit.
- No canonical Lean expression, expression/environment hash, exact imports, checked alternate
  encoding, or statement mutation test exists.
- Discovery protocol, anchor audit, obligation registry and typed graphs, proof, composition and
  trust checks, readable reconstruction, hermetic replay, deterministic evidence bundle, and
  independent release verification are open.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose purpose is to freeze the honest ambiguity boundary and
open DAG. Only the integration lane may accept the provisional worker receipt.
