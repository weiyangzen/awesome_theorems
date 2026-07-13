# Intake validation

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier and scope invariants, repository-source
provenance, a versioned human-source lead, pinned environment identity, direct candidate API
elaboration and representative axiom reports, prohibited-construct hygiene, JSON integrity, and
whitespace. It does not freeze or prove a canonical theorem. The catalog omits the scalar field,
both completeness assumptions, bounded-operator encoding, ordinary versus semilinear boundary,
and open-map definition, so `IntakeProbe.lean` authenticates candidate interfaces only.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is provisional nonrelease worker evidence.

## Environment

- Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`; Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package status was clean after the probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- `Mathlib.Analysis.Normed.Operator.Banach` source SHA-256:
  `b046e38a239014c32e2313b4a216edd89198e57351d9c6068a3de7811680bf6c`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0276` | exit 0; rank 1282, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` before edits | exit 0; only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was untracked and it was preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 1985,1990 -- Docs/researches/math_theorems.md`; same for lines 2260-2265 | exit 0; both identical uncited records originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error --max-time 30 -o /tmp/alan-fa-6aeecbd.tar.gz https://codeload.github.com/alan-sorani/functional_analysis_notes/tar.gz/6aeecbd2a7d6df63455f3d7beb273b6b4512dfbc` | exit 0 during source discovery; immutable archive SHA-256 `664a51f3cdf150ac6522702c67677bde27beb3e291e64dcbfa0b5f1a877dfa47` |
| `tar -xOf /tmp/alan-fa-6aeecbd.tar.gz functional_analysis_notes-6aeecbd2a7d6df63455f3d7beb273b6b4512dfbc/functional_analysis.tex \| sha256sum` | exit 0; TeX SHA-256 `2b1acb4cd1e680e4a0e348c48dbd1c07eee1a8847f7b373f00129afccada9bd4` |
| `tar -xOf /tmp/alan-fa-6aeecbd.tar.gz functional_analysis_notes-6aeecbd2a7d6df63455f3d7beb273b6b4512dfbc/functional_analysis.tex \| sed -n '1133,1198p' \| sha256sum` and the same pipeline without `sha256sum` | exit 0; Open Map definition, Theorem 2.2.11, and intended Baire/series route inspected; excerpt SHA-256 `826821f7a25c2c73cad62e7050bf424826dc0028ed8f9233a68ad7a23b1a9825`; printed line 1152 repeats the unit ball instead of `B(0,n)`, invalidating the Baire inference until corrected; H2 gap lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | exit 0; pinned revision/tree recorded above; empty status output |
| `rg -n 'ContinuousLinearMap.isOpenMap\|exists_preimage_norm_le\|exists_approx_preimage_norm_le\|isQuotientMap\|LinearEquiv.continuous_symm' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Normed/Operator/Banach.lean` | exit 0; direct theorem, proof ingredients, and distinct corollaries located |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0276/IntakeProbe.lean)` | exit 0; six interfaces elaborated; three representative declarations report `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `d84aba7fe0dadb887b30bb30c68f486caa6404fc9f686410fee8c78813d04774` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0276-pycache python3 -m py_compile Stage1_Instances/THM-M-0276/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0276/check_intake.py --source-archive /tmp/alan-fa-6aeecbd.tar.gz --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; source archive, TeX, lines 1133-1198 excerpt, theorem text and proof-gap boundary plus manifest/DAG identity, hashes, H2/M3/R4 boundary, null target, inventory, receipt/packet agreement, probe, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-0276` | exit 1 as expected; no prohibited declaration token; `#print axioms` is an allowed diagnostic |
| `for f in .stage1-worker-selftest.json Stage1_Instances/THM-M-0276/*; do git diff --no-index --check -- /dev/null "$f"; done` | each file returned only expected added-file difference exit 1 and no whitespace diagnostic |
| `git diff --check -- Stage1_Instances/THM-M-0276 .stage1-worker-selftest.json` | exit 0; tracked-diff check was clean but does not cover the untracked packet, which is why the preceding per-file checks are authoritative here |

## Known open gates

Catalog-to-source identity, historical primary-source mapping, the source's printed Baire-cover
typo, incorporated bounded-operator definition chain, corrections or errata disposition, complete premise/conclusion
mapping, and independent source review remain open. So do the exact scalar and completeness
boundary, canonical Lean expression and environment fingerprints, minimal imports, checked
same-field/semilinear transports, statement mutations, exhaustive anchor and terminal-body audit,
discovery and obligation freezes, typed graphs, proof and composition, accepted trust closure,
readable reconstruction, hermetic replay, deterministic bundle, independent verification, master
acceptance, audit completion, and theorem completion. These open gates do not invalidate a
truthful, self-tested `planned` intake.
