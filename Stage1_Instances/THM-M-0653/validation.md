# Statement validation

Base revision: `8a4de324e430348fba945ccc31633dc565330377`.

Validation date: 2026-07-12 (Asia/Shanghai). This validation covers the exact statement declaration
and dossier consistency against existing pinned artifacts. It establishes statement elaboration,
not proof closure or theorem completion.

The preflight worktree contains the existing untracked `Formalizations/Lean/.lake` link/artifact.
It is used read-only. No `lake update`, `lake build`, clone, fetch, or other dependency mutation is
part of this intake.

Environment fingerprint:

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0653` | exit 0; rank 698, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | exit 0; versions recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib revision recorded above |
| scoped repository and pinned-mathlib `rg` searches for Beth and implicit/explicit definability | exit 0; only the repository gloss and generic definability API were found; no Beth root declaration located |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0653/Statement.lean` | exit 0; printed `BethDefinabilityTarget.{u, v, w} (L : Language) (n : Nat) (T : (Expanded L n).Theory) : Prop` |
| `sha256sum Stage1_Instances/THM-M-0653/Statement.lean` | exit 0; `99f75b5c940f45b295576c150f9cdd3dccec590c749d792ab672ab57ed0cb1eb` |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | exit 0; both valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0653 .stage1-worker-selftest.json` | exit 0; no output |

## Status boundary

Primary-source inspection and review, checked alternate transports, formal-candidate audit,
obligation registry, proof, hermetic replay, readable reconstruction, and independent verification
all remain open. They prevent audit and theorem completion but do not invalidate this self-tested
statement phase.
