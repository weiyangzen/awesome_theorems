# Intake validation

Base revision: `f294137feee7840fd105a4d3f6073d5cf45508ea` (tree
`234b8f273d252c2c42ce6860315ed973049c871a`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, literal catalog and duplicate
boundaries, source-statement crosswalk, open downstream task DAG, structured intake invariants, and
a narrow pinned Lean API probe. It does not validate source fidelity, a canonical proposition, a
proof, or theorem completion. The automation-provided canonical `.lake` symlink was pre-existing
and used read-only; no dependency update, build, clone, fetch, or other `.lake` mutation was run.
This dirty worker execution is nonrelease evidence.

## Environment

- Linux 7.0.0-27-generic, x86_64.
- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0294` | 0 | rank 1298, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink existed; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 2111,2116 -- Docs/researches/math_theorems.md` | 0 | all six uncited THM-M-0294 catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git blame -L 2493,2498 -- Docs/researches/math_theorems.md` | 0 | all six separate THM-M-0342 duplicate-candidate lines originate at the same catalog commit |
| `curl -L --fail --max-time 45 -sS 'https://api.crossref.org/works/10.1007%2Fbf03014877' -o /tmp/thm-m-0294-source/crossref.json` | 0 | Plancherel, 1910, Rendiconti 30, pages 289-335 confirmed as a metadata lead; payload SHA-256 `956922b769c5aad3016ecfdef88298598c492572b024141e4091bad1a30b16ce` |
| `curl -L --fail --max-time 45 -sS 'https://link.springer.com/content/pdf/10.1007/BF03014877.pdf' -o /tmp/thm-m-0294-source/plancherel.pdf` | 0 | returned a 229355-byte HTML access page, not article text; SHA-256 `3dd71d12ce2899b12461baae873aca9fdc8c1891e5cb18f11ebeba97622d2ca7`; no theorem text or H0 credit |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package worktree clean |
| `rg -n -i --glob '*.lean' 'Plancherel\|norm_fourier_eq\|fourierTransformₗᵢ' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems Stage1_Instances/THM-M-0342` | 0 | direct L2 isometry, norm, and inner-product APIs plus two repo-local candidate surfaces found; discovery only, not an exhaustive anchor audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0294/IntakeProbe.lean)` | 0 | three pinned Plancherel interfaces and the scalar Euclidean specialization elaborated; stdout SHA-256 `7281909edded52829aec9eab57d00f09018134be03e7942ad90228ffa52f9862`; no canonical target or proof declared |
| `python3 -m json.tool` separately on all owned JSON and `.stage1-worker-selftest.json` | 0 | planned instance, open task DAG, provisional receipt, and worker handoff parsed |
| `python3 -c` AST parse of `check_intake.py` | 0 | scoped checker parsed without adding generated files |
| `python3 -B Stage1_Instances/THM-M-0294/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, pins, planned H1/M3/R4 null-target boundary, duplicate boundary, exact inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0294/check_intake.py` | 0 | public replay mode passed |
| prohibited Lean construct scan over `IntakeProbe.lean` | 1 | expected no-match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped `git diff --check` plus per-new-file no-index checks | 0 | no whitespace diagnostics |

## Known open gates

- An immutable primary or authoritative edition, exact theorem and definition locators, complete
  assumption/proof/normalization crosswalk, corrections and errata audit, translation decision, and
  independent source review remain open.
- The integration lane must adjudicate whether `THM-M-0294` and `THM-M-0342` are duplicate roots and
  which target owns any shared source and formal evidence.
- Spatial domain and dual, scalar/value space, Fourier character and sign, `2 * pi` and measure
  normalization, `L^2` carrier, extension route, ordered binders, conclusion, and boundary cases are
  not selected by the catalog.
- No canonical Lean target, minimal-import claim, elaborated expression/environment fingerprint,
  checked alternate transport, or required statement mutation exists.
- The exhaustive anchor audit, discovery protocol, obligation registry, typed graphs, proof,
  composition, transitive trust and provenance closure, readable reconstruction, hermetic replay,
  deterministic bundle, independent verifier, master acceptance, audit completion, and theorem
  completion remain open.

These failures block every downstream claim, but they do not invalidate a truthful, self-tested
`planned` intake that freezes the ambiguity and non-substitution boundary. Only the integration lane
may accept this provisional worker receipt.

The `--worker-packet` command is worker-only: it binds the unintegrated `[ ]` base and root handoff.
The receipt's public structured recipe omits that flag because the integration lane does not merge
`.stage1-worker-selftest.json` and may advance the authoritative intake state independently.
