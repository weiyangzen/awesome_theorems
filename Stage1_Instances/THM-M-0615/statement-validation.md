# Statement-phase blocker and validation

Item: `S56-M-0615-STATEMENT`  
Base revision: `3ec252ff03162db067bf77973c0a74a97d4bbe0a`

## Fail-closed result

The statement gate is **blocked** at exact source identification. The repository title,
"classification of four-dimensional manifolds," is not one theorem. The intake provisionally
chooses the simply connected closed oriented topological branch associated with Freedman, but the
owned dossier contains only candidate bibliography. It has no inspected fixed edition,
theorem/page, verbatim statement, corrections, or resolution of the realization versus uniqueness
branches, parity cases, Kirby-Siebenmann qualification, and exceptional cases.

The legacy `S1_M_252.lean` module cannot repair that gap. Its `FourManifoldInvariants` accepts an
intersection form and a free proposition named `orientationData`; its
`FreedmanClassificationBridgeData` accepts the classification implication itself as a field.
Promoting either interface to the canonical root would broaden or substitute the theorem and would
violate the exact-statement gate. It receives no statement credit here.

## Narrow Lean probe

`StatementProbe.lean` uses the smallest imports found for the presently expressible fragments. It
kernel-elaborates a `C^0` four-manifold context with `T2Space`, `CompactSpace`, `ConnectedSpace`,
`SimplyConnectedSpace`, and `IsManifold`, plus the conclusion `Nonempty (M ≃ₜ N)`. This probe is
deliberately not named `Statement.lean`: it is neither the canonical target nor a credited
alternate encoding. The pinned snapshot has no repo-locally discovered Kirby-Siebenmann,
four-manifold intersection-form construction, or terminal classification API.

## Commands and results

All commands ran in this worker clone. Lean ran from `Formalizations/Lean`; no Lake dependency was
updated, fetched, built, or otherwise mutated.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0615` | 0 | rank 252, planned, L0/rework-required, theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-0615/StatementProbe.lean` | 0 | both available statement fragments elaborated and their explicit types printed |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0615/StatementProbe.lean lean-toolchain lake-manifest.json` | 0 | probe `9a2dcf...7698`; toolchain `651c8a...1d2`; manifest `321626...2d81` |
| `python3 -m json.tool Stage1_Instances/THM-M-0615/statement-blocker.json` | 0 | structured blocker is valid JSON |
| forbidden-term scan of `StatementProbe.lean` | 1 | no `sorry`, `admit`, `axiom`, or `placeholder` match; 1 is ripgrep's no-match exit |

## Retry condition

Archive or otherwise fix an inspectable primary source and applicable errata, select an exact
theorem/page and branch, and freeze every hypothesis and exception. Then encode the actual
invariants without assuming the desired classification bridge, elaborate the canonical target,
fingerprint it, and run the required removed-hypothesis, changed-domain, binder-scope, and boundary
mutations. Until then the root remains `[H2, M4, R4]`, and no worker self-test manifest is valid.
