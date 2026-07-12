# Intake validation

Base revision: `02cc55f883d5b5d091ead6851bffe89199eb8391` (tree
`035212d041a1e61553b3d2f465964c9bbb35e47d`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source and neighbor-scope boundary, open task DAG,
structured invariants, and a narrow pinned Lean API probe. It does not validate a canonical
Sturm-Liouville statement or proof because the catalog does not identify one. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only. No dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker evidence is
not release evidence.

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

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1384` | exit 0; rank 994, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short` | preflight exit 0; only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was present |
| `git blame -L 10083,10088 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded retrieval and inspection of NUMDAM record `JMPA_1836_1_1__106_0` and its linked errata | exit 0; primary family lead and corrections inspected; source SHA-256 `dac79254915e753884f6dd68865ef5c7165043599ac611558c6c4d6045feac96`, errata SHA-256 `ed7f4db1783207a385546e47c43f8c952352ebedda823e62e0e611918a962cd7`; no canonical selection or H0 credit |
| bounded retrieval and inspection of NIST DLMF Section 1.13(viii) and Encyclopedia of Mathematics immutable revision 55171 | exit 0; regular/singular, finite/infinite, boundary, spectral, and transform distinctions inspected; no canonical selection or H0 credit |
| bounded retrieval and inspection of Teschl Sections 5.3-5.6 and official errata | exit 0; equation, operator, boundary, spectral, oscillation, and periodic scopes distinguished; no canonical selection or H0 credit |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | exit 0; Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` and package `git status --short` | exit 0; pinned revision/tree above and clean package source |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1384/IntakeProbe.lean` | exit 0; thirteen adjacent derivative, ODE, eigenvalue, compact/symmetric spectral, and Rayleigh APIs elaborated; stdout SHA-256 `ac028e1169b8e992d0aac97fb938547024be09f08fea05ac3f1bbe994c2e0008` |
| `rg -n -i --glob '*.lean' 'sturm[ _-]?liouville\|liouville[ _-]?sturm' Formalizations/Lean/AwesomeTheorems` | exit 0 with one nonterminal planning-string hit in `S1_M_207.lean`; no target declaration located; bounded intake discovery only |
| the same exact `rg` command with `Formalizations/Lean/.lake/packages/mathlib/Mathlib` as its final path | exit 1; expected no match; bounded pinned-mathlib discovery only, not an exhaustive external audit |
| `python3 -m json.tool Stage1_Instances/THM-M-1384/instance.json` | exit 0; the same command separately passed for `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` |
| `python3 -c "import ast,pathlib; ast.parse(pathlib.Path('Stage1_Instances/THM-M-1384/check_intake.py').read_text())"` | exit 0; scoped validator parsed without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1384/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; target and authoritative-DAG identity, pins, H5/M4/R4 boundary, null target, artifact inventory, receipt, packet, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1384` | exit 1; expected no match; no prohibited declaration in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-1384 .stage1-worker-selftest.json` plus `git diff --no-index --check /dev/null <each-new-file>` | no whitespace diagnostics; the tracked-diff command exits 0, while each clean new-file comparison exits 1 only because content differs from `/dev/null` |

## Known open gates

The H5 theory label must first receive an integration-approved correction to one stable proposition
or be redirected to another rev-5.6-permitted target form; ordinary theorem execution is prohibited
until then. An accepted immutable source, exact definitions, binders, assumptions, conclusion and proof boundary,
historical attribution, translation and errata crosswalk, regular-versus-singular, boundary and
neighbor-scope decisions, and independent review remain open. So do the canonical Lean expression
and environment fingerprints, transports and mutations, anchor audit, discovery protocol,
obligation registry, typed graphs, proof and composition, trust and provenance closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These gates do not invalidate a truthful,
self-tested `planned` intake.
