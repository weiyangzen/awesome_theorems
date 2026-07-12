# THM-M-0012 Anchor-Audit Validation

Item: `S56-M-0012-ANCHOR_AUDIT`

Base revision: `02cc55f883d5b5d091ead6851bffe89199eb8391`

Base tree: `035212d041a1e61553b3d2f465964c9bbb35e47d`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Complex.exists_root` has the exact positive-degree complex-polynomial root conclusion adjacent to
the frozen target. A local audit adapter converts exclusion of every `Polynomial.C c` to positive
degree and elaborates the exact binder and conclusion shape. Lean prints a direct Liouville proof
body and reports only `propext`, `Classical.choice`, and `Quot.sound` for both the terminal theorem
and adapter.

`Complex.isAlgClosed` and the generic `IsAlgClosed.exists_root` route are not independent: the
complex instance is constructed from `Complex.exists_root`. They are deduplicated support. The
immutable `madvorak/read-lean` candidate only quotes the mathlib proof in its README and declares no
FTA theorem. No additional proof dependency needs integration; public discovery remains bounded
because authenticated GitHub code search and grep.app were unavailable.

The exact mathlib route is an `M0-W` candidate with local `E2` checking. The accepted root remains
`H1/M3/R4` until downstream proof, composition, provenance/trust, and master-acceptance gates provide
accepted `E1` evidence. Neither `AUDIT-Z` nor theorem completion is claimed.

## Commands And Results

All local validation ran in this worker clone against the automation-provided canonical `.lake`
symlink read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard structure and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0012` | 0 | rank 1062; planned; L0/rework-required; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | exact revision `8a1783...ea95`, tree `bdc39a...5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; dependency worktree clean |
| read-only HTTPS inspection of `madvorak/read-lean` README, Lean source, toolchain, and manifest at commit `ad424b95...57acb` | 0 | README/source SHA-256 `de11b90a...e1` / `81b3580c...44`; no independent FTA declaration; Lean 4.12.0-rc1 and mathlib `d389f3...648` recorded |
| `lake env lean ../../Stage1_Instances/THM-M-0012/AnchorAudit.lean` from `Formalizations/Lean` | 0 | direct, packaged, and generic types printed; direct/package bodies printed; exact adapter elaborated; four axiom reports matched; stdout SHA-256 `3bf558a6...148` |
| `python3 -B Stage1_Instances/THM-M-0012/check_anchor_audit.py` | 0 | local pins, blobs, hashes, body markers, immutable external ledger values, classification, packet, and narrow Lean replay matched offline |
| `python3 -m json.tool` on the three anchor JSON artifacts and root packet | 0 | all structured artifacts parsed |
| scoped prohibited-construct scan over `AnchorAudit.lean` | 1 (expected no match) | no proof gap, axiom declaration, unsafe/opaque body, TODO, FIXME, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0012 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## External Search Boundary

Anonymous GitHub repository metadata search returned zero repositories for the quoted theorem and
Lean query. GitHub code search returned HTTP 401, while grep.app returned HTTP 429. Each response is
hashed in `anchor-audit.json`. These are bounded query results and access failures, not evidence of
global absence or discovery saturation.

## Status Boundary

This phase supplies provisional self-tested anchor evidence pending master acceptance. The
obligation registry, canonical proof-phase wrapper, full transitive trust/TCB closure, primary-source
and readable reconstruction review, hermetic and independent validation, deterministic release
bundle, `AUDIT-Z`, and theorem completion remain open.
