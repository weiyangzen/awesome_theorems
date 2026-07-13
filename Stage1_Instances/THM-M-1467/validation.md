# THM-M-1467 intake validation

Base revision: `521bd42e5ab5e30513a3c2b7377ea4a1516c0d16` (tree
`6f3d9fcf297fe5251a1dc839c1e67930001a86fc`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target identity, the planned dossier, source-statement and non-substitution
boundaries, the open task DAG, structured intake invariants, and a narrow pinned Lean API probe. It
does not validate a canonical spectral-element proposition or proof because the catalog supplies no
source-selected root. The automation-provided canonical `.lake` symlink was pre-existing and used
read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was
performed. This dirty worker run is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e` on Linux `7.0.0-27-generic` x86_64.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source boundary

Crossref metadata for DOI `10.1016/0021-9991(84)90128-1` identifies Anthony T. Patera, the title
“A spectral element method for fluid dynamics: Laminar flow in a channel expansion,” *Journal of
Computational Physics* 54(3), June 1984, pages 468-488. The inspected record had no abstract. The
article body, exact theorem or formula, assumptions, proof, corrections, catalog-root selection,
immutable capture, and independent review were not admitted. The observed response is mutable
bibliographic metadata and does not support `H0`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1467` | exit 0; rank 1144, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 10707,10712 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error 'https://api.crossref.org/works/10.1016%2F0021-9991(84)90128-1' \| sha256sum` | exit 0; bibliographic fields above independently inspected; exact response SHA-256 `f5525819bfa0f7a374a4fdea0b1c65f1c3b02ae6e9f13cef0f4917d4d09f448a`; metadata only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | exit 0; pinned revision and tree recorded above; mathlib worktree clean |
| `rg -n -i --glob '*.lean' 'spectral[ -]element\|pseudospectral\|spectral numerical method' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | exit 1 as expected; no exact-topic declaration; intake discovery only |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1467/IntakeProbe.lean)` | exit 0; eight adjacent APIs elaborated; representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; output SHA-256 `ffb52430462d2a45217887343544d376d5209ea87ff526291ccf00b144b4ab94`; no target theorem |
| `python3 -m json.tool` on the three owned JSON files and root worker packet | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1467-pycache python3 -m py_compile Stage1_Instances/THM-M-1467/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1467/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, null target, H5/M4/R4 boundary, pins, inventory, receipt/packet, and six open tasks agree |
| `rg -n -e '\bsorry\b' -e '\badmit\b' -e '\bsorryAx\b' -e '\baxiom\b' -e '\bconstant\b' -e '\bopaque\b' -e '\bunsafe\b' Stage1_Instances/THM-M-1467 --glob '*.lean'` | exit 1 as expected; no prohibited declaration in the API-only probe |
| `for f in Stage1_Instances/THM-M-1467/* .stage1-worker-selftest.json; do output=$(git diff --no-index --check /dev/null "$f" 2>&1); code=$?; if [ "$code" -gt 1 ]; then printf '%s\\n' "$output"; exit "$code"; fi; done` and `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

The method label must be redirected to an independently reviewed, immutable, exact proposition.
The problem or PDE, domain, mesh, element maps, polynomial spaces, nodes, quadrature, discrete
formulation, analytic premises, norms, constants, exact conclusion, quantifier order, arithmetic
model, neighbor boundaries, and degenerate cases remain open. So do the primary theorem/proof
crosswalk, canonical Lean expression and environment fingerprint, checked transports, statement
mutations, exhaustive anchor audit, discovery protocol, obligation registry, typed graphs, proof
and composition, trust/provenance closure, readable reconstruction, hermetic replay, deterministic
bundle, independent verification, master acceptance, audit completion, and theorem completion.
These open gates do not invalidate a truthful, self-tested `planned` intake.
