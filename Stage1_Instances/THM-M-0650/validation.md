# Intake validation

Base revision: `34b51889997c961b0ad69413dae1dc249a8cf744`.

Validation date: 2026-07-12 (Asia/Shanghai). Preflight found the existing untracked
`Formalizations/Lean/.lake` artifact. It was used read-only; no `lake update`, `lake build`, clone,
fetch, or other dependency mutation was run. This is scoped, nonrelease intake evidence.

Environment fingerprint:

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0650` | exit 0; rank 696, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | exit 0; Lean and Lake versions recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib revision recorded above |
| repository and pinned-mathlib `rg` searches for Tarski-Vaught and elementary-substructure declarations | exit 0; repository source reduced to secondary metadata and exact-looking mathlib candidates located |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0650/IntakeProbe.lean` | exit 0; `IsElementary`, the substructure test, and the embedding test elaborated; the substructure theorem body was printed |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0650 .stage1-worker-selftest.json` | exit 0; no output |

The Lean probe establishes candidate availability and shape only. It is not statement acceptance:
there is no reviewed pinpoint primary source, canonical wrapper, serialized expression hash,
checked source transport, or mutation suite. The intake itself is self-tested, but all downstream
gates remain open: source review, exact implication/iff decision, statement and mutation gate,
anchor/provenance audit, obligation graphs, proof integration, hermetic validation, readable
reconstruction, and independent review. Accordingly this dossier claims neither audit completion
nor theorem completion.
