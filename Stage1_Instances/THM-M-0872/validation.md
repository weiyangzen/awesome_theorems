# THM-M-0872 intake validation

Base revision: `748243faadc15828fb087059337fd05b7be9fdeb` (tree
`e46d642646f80980838b6f016f5d69b817bd464d`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, scope and source-statement
boundaries, the six-node open downstream DAG, structured intake invariants, and a narrow pinned
Lean API probe. It does not validate a canonical Bodlaender proposition or proof: the catalog gives
an unspecified approximation gloss while the year-matched source family states a fixed-parameter
exact decision-and-construction result. The automation-provided canonical `.lake` symlink was
pre-existing and used read-only; no dependency update, build, clone, fetch, or other `.lake`
mutation was performed. This dirty worker run is nonrelease evidence.

## Source boundary

Crossref and DBLP confirm Hans L. Bodlaender, *A Linear-Time Algorithm for Finding
Tree-Decompositions of Small Treewidth*, SIAM Journal on Computing 25(6), December 1996, pages
1305-1317, DOI `10.1137/S0097539793251219`. The Crossref response SHA-256 is
`3fe295385af09485316242a2397556f7fc8ddc28ce43c789bf3367548b466a58`; the DBLP BibTeX SHA-256 is
`a5f9dc7583c07ed6fdad15f4d1b5cc5c6b0fdea979398bcb1feb319671bee49c`.
The publisher endpoint returned HTTP 403, so no journal theorem passage or proof was admitted.

Utrecht repository metadata for the 1992 report precursor was inspected. The item metadata digest
is `ef0a72b6da4a14d766b4c6ea94b8a49c588180fd6b70d75d8060697c94c6c44c`; its bitstream metadata
digest is `ab3fa5839e4389fda0e1db6e4f8c2174041b408c0f931a2c042be22002cc9266` and reports an original
size of 863740 bytes with MD5 `5a693dd987524c9e28fd34ba8b424e6a`. The content endpoint emitted
changing 881920-byte wrapper PDFs whose extracted text contained only repository cover metadata;
those wrappers were not admitted as immutable source text. OpenAIRE's observed summary confirms
the exact fixed-`k` source family, but source selection, exact theorem and proof mapping,
corrections, and independent review remain open. No H0 is claimed.

## Environment

- Platform: Linux `7.0.0-27-generic`, x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root unless a different `cwd` is shown.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0872` | exit 0; rank 1426, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 6390,6395 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl` Crossref DOI metadata and `https://dblp.org/rec/journals/siamcomp/Bodlaender96.bib`, followed by `sha256sum` and bounded field inspection | exit 0; title, author, December 1996, journal, volume 25, issue 6, pages 1305-1317, and DOI matched; observed digests recorded above |
| `curl -L --fail --silent --show-error https://doi.org/10.1137/S0097539793251219` | exit 22; publisher endpoint returned HTTP 403, so no journal body or proof was admitted |
| `curl` Utrecht DSpace item and bitstream APIs for handle `1874/16670`, followed by bounded JSON inspection | exit 0; report identity, open-access record, bitstream name, size, and repository-reported MD5 recorded; current generated wrapper was excluded from source credit |
| `curl -L --fail --silent --show-error 'https://api.openaire.eu/search/publications?doi=10.1137/S0097539793251219&format=json'` | exit 0; observed response SHA-256 `d8163df72893b6222d8a932e70d2728e67e612738f6278e97bac229ad3fe101e`; source-family summary says fixed-`k` exact recognition plus positive decomposition output |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision/tree above; mathlib source worktree clean |
| `rg -n -i 'Bodlaender\|tree.?width\|tree.?decomposition' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | exit 0 only for an unrelated phrase `theorem-tree decomposition`; no treewidth, tree decomposition, or Bodlaender declaration found; bounded intake search only |
| initial `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0872/IntakeProbe.lean)` on the draft probe | exit 1; the graph APIs elaborated, but three draft names under `Turing.TM2` were unknown; the probe was corrected to the actual `Turing` namespace before evidence was recorded |
| `(cd Formalizations/Lean && env -i HOME="$HOME" LANG=C.UTF-8 LC_ALL=C.UTF-8 PATH="$PATH" lake env lean ../../Stage1_Instances/THM-M-0872/IntakeProbe.lean)` | exit 0; nine adjacent graph/tree and machine-time APIs elaborated; tree-path theorem axiom report contained only `propext`, `Classical.choice`, and `Quot.sound`; stdout SHA-256 `dc19fff3438303c84d7e254101197d0b335ba6544faf1e4c1025e7361502c927` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0872/check_intake.py` | exit 0; scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0872/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; authority identity, null target, H5/M4/R4 boundary, pins, exact inventory, receipt/packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0872/check_intake.py` | exit 0; public replay mode passes without the scheduler-only packet |
| `rg -n -e '\bsorry\b' -e '\badmit\b' -e '\bsorryAx\b' -e '^[[:space:]]*axiom\b' -e '^[[:space:]]*constant\b' -e '^[[:space:]]*opaque\b' -e '^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0872 --glob '*.lean'` | expected no-match exit 1; no prohibited declaration in the discovery-only probe |
| per-new-file `git diff --no-index --check /dev/null FILE` with expected diff exit handled, then scoped `git diff --check` | no whitespace diagnostics for target artifacts or worker packet |

## Known open gates

- Master acceptance of this intake is pending.
- A reviewer must resolve the catalog approximation wording against the 1996 exact fixed-parameter
  theorem, select an edition and exact proposition, crosswalk all definitions, assumptions,
  quantifiers, conclusions, proof, corrections, and boundary cases, and approve neighboring-target
  ownership.
- Canonical Lean target, minimal imports, expression and environment fingerprints, checked
  transports, boundary witnesses, and all four required statement mutation classes remain open.
- Exhaustive formal anchor and proof-body provenance audit, discovery protocol, obligation
  registry, typed graphs, proof, composition, trust closure, readable reconstruction, hermetic
  replay, deterministic bundle, independent verification, audit completion, and theorem completion
  remain open.

These failures block statement and theorem execution but do not invalidate a truthful, self-tested
`planned` intake. Only the integration lane may accept the provisional worker receipt.
