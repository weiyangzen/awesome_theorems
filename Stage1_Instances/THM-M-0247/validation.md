# THM-M-0247 intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, catalog and primary-source crosswalk, source/formal and
non-substitution boundaries, six-node open task DAG, structured intake invariants, and a narrow
pinned Lean API probe. It does not validate an exact Lean statement or proof. The
automation-provided canonical `.lake` symlink existed before intake and was used read-only; no
dependency update, build, clone, fetch, or other `.lake` mutation was performed. The downloaded
source bytes were inspected from `/tmp` and were not added to the repository. This dirty worker run
is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e` on Linux x86_64.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean before and after the
  probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0247` | exit 0; rank 1257, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree match this record |
| `git blame -L 1780,1785 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| DOI resolution and publisher landing-page inspection for `10.4064/fm-7-1-24-29` | exit 0; A. Kolmogoroff, title, 1925, volume 7, pages 24-29, DOI, and official PDF URL confirmed; the dynamic landing page is a locator, not hashed evidence |
| Official publisher PDF retrieval to `/tmp` and visual inspection | exit 0; six pages, 273743 bytes, SHA-256 `b0567754c1c50a5549f664effcc2e29163b4409de1e4fcc228895e19e803a73b`; printed pages 24-25 fix the conjugate boundary context, principal-value formula, Theorem I, binders, and estimate; source lead only |
| `sha256sum` over authority inputs, catalog/Stage0 excerpts, toolchain/lockfile, three pinned mathlib modules, and the observed source scan | exit 0; exact hashes are recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean version and target recorded above |
| `(cd Formalizations/Lean && lake --version)` | exit 0; Lake version recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0 before and after probe; empty output |
| bounded case-insensitive search for Hilbert/conjugate transforms, Kolmogorov conjugate-function names, and weak-type/weak-(1,1) patterns in repo-local Lean and pinned mathlib | completed; no target terminal theorem appeared; intake discovery only, not a global absence proof |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0247/IntakeProbe.lean)` | exit 0; nine adjacent pinned APIs elaborated; stdout SHA-256 `42a46aaf78698bc3e7d85646b810fd7a9b33c3b1fbd630c22846e84199de0f11`; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0247-pycache python3 -m py_compile Stage1_Instances/THM-M-0247/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0247/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; authority/DAG identity, source and dependency hashes, null Lean target, H1/M4/R4 boundary, exact artifact inventory, receipt/packet, and six open tasks agree |
| `rg -n -e '\bsorry\b' -e '\badmit\b' -e '\bsorryAx\b' -e '^[[:space:]]*axiom\b' -e '^[[:space:]]*constant\b' -e '^[[:space:]]*opaque\b' -e '^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0247 --glob '*.lean'` | exit 1 as expected; no prohibited declaration in the discovery-only probe |
| `git diff --check`, plus `git diff --no-index --check /dev/null <file>` for every untracked changed file | exit 0 for whitespace diagnostics; every changed file passed |

The generic Chebyshev-Markov declarations are adjacent distribution-function infrastructure only.
They assume the measured function already has the relevant finite `Lp` norm and do not construct
the conjugate function or prove Kolmogorov's endpoint map. They receive no target statement or
proof credit.

## Known open gates

Independent review of the source scan, exact translation, incorporated Privaloff boundary theorem
and proof premises, corrections/errata, and source-to-node mapping remain open. So do measure
normalization, scalar and representative policy, conjugate construction and additive normalization,
threshold and strictness conventions, ordered binders, canonical Lean target and minimal imports,
expression/environment fingerprints, checked transports, four statement mutation classes,
exhaustive anchor audit, discovery protocol, obligation registry, typed graphs, proof and
composition, source/provenance/trust closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These open gates do not invalidate a truthful self-tested `planned` intake.
