# Intake validation

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, scope and source crosswalk, historical-source boundary,
THM-M-0310 non-substitution boundary, open task DAG, structured invariants, and pinned Lean
candidate probe. It does not validate a canonical Holder proposition or proof because the exact
source, measure, function representation, carrier, product, integral, exponent, hypothesis, binder,
and boundary choices remain open. The automation-provided canonical `.lake` symlink was pre-existing
and used read-only. No update, build, clone, fetch, or dependency mutation was performed. Dirty
worker evidence is nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean after the probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0279` | exit 0; rank 1285, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'`; `git blame -L 2006,2011 -- Docs/researches/math_theorems.md` | exit 0; base revision/tree recorded above; all six source-record lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error 'https://encyclopediaofmath.org/index.php?title=H%C3%B6lder_inequality&oldid=28956' -o /tmp/thm-m-0279-eom.html`; bounded `rg` inspection | exit 0; revision 28956 distinguishes sum, integral, endpoint, multi-function, and generalized forms and cites Holder 1889, pages 38-47; secondary lead only |
| `mkdir -p /tmp/thm-m-0279-source && curl -L --fail --silent --show-error 'https://gdz.sub.uni-goettingen.de/mets/PPN252457072_1889.xml' -o /tmp/thm-m-0279-source/mets.xml && curl -L --fail --silent --show-error 'https://manifests.sub.uni-goettingen.de/iiif/presentation/PPN252457072_1889/manifest' -o /tmp/thm-m-0279-source/manifest.json && for n in $(seq 44 53); do printf -v image_id '%08d' "$n"; curl -L --fail --silent --show-error "https://images.sub.uni-goettingen.de/iiif/image/gdz:PPN252457072_1889:${image_id}/full/1600,/0/default.jpg" -o "/tmp/thm-m-0279-source/${image_id}.jpg"; done` | exit 0; institutional metadata and all ten article images (printed pages 38-47) fetched outside the workspace; METS SHA-256 `e703a40a23af66af3a4860fb83a13cbf9cdb5d0bdf7a96316db5c71733eb7d40`, manifest SHA-256 `626b3b66009bfb3296df4587743447b8c0b9de9edf6e8cbd3796808701edbcb8`; inspected scan contains finite weighted mean/power-sum results, not a verbatim modern measure-integral statement, so no H0 claim |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | exit 0; pinned revision/tree recorded above; empty status output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0279/IntakeProbe.lean)` | exit 0; seven exact-topic theorem/consequence interfaces and two exponent predicates elaborated; five theorem candidates each reported `[propext, Classical.choice, Quot.sound]`; complete output SHA-256 `6e3f1c1285d6f24fe06fb8f17da19cfe6962df54efbf2a04609071a5b717b20d` |
| bounded `rg` search in pinned mathlib and repo-local Lean | completed; exact-topic `(E)NNReal` lintegral, Bochner norm/nonnegative-real, generalized `eLpNorm`, and `MemLp.mul` interfaces were located; no source-identical canonical root or repo-local THM-M-0279 wrapper was inferred |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 after finalization; all structured artifacts parse |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0279-pycache python3 -m py_compile Stage1_Instances/THM-M-0279/check_intake.py` | exit 0; checker compiled without writing generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0279/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; authorities, source/dependency hashes, historical and neighbor boundaries, H1/M3/R4 planned state, null target, exact inventory, receipt/packet, Lean probe, and six open tasks agree |
| token-anchored prohibited Lean declaration scan over the owned path | exit 1 as expected; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` remains permitted |
| scoped new-file whitespace checks and `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

An exact modern source proposition or a complete reviewed derivation from the historical scan,
incorporated definitions, ordered premise/conclusion/proof crosswalk, Rogers priority resolution,
translation, corrections or errata, and independent review remain open. So do the measure space,
raw-function versus `Lp` representation, scalar carrier, product/absolute/norm convention, integral,
finite versus endpoint exponent regime, hypotheses, binders, conclusion normalization, and boundary
cases. The canonical Lean expression and environment fingerprints, checked alternate encodings,
statement mutations, exhaustive anchor/provenance audit, discovery and obligation freezes, typed
graphs, proof and composition, accepted trust closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion remain open. These gates do not invalidate a truthful self-tested `planned` intake.
