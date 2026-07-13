# THM-M-0741 Anchor-Audit Validation

Item: `S56-M-0741-ANCHOR_AUDIT`

Base revision: `561d83df037004ceb2259292d7c63be930b40391`

Base tree: `6eb02475bf5a70139d60615c924b31c930efc2bb`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`ComputablePred.halting_problem n` proves that no computable predicate decides whether an
arbitrary partial-recursive code halts at the fixed input `n`. This is not definitionally the
frozen pair predicate. `AnchorAudit.lean` therefore checks an exact target-owned adapter: an
alleged decider on `Code x Nat` is composed with the computable section `code |-> (code, 0)`,
contradicting the pinned theorem at zero.

The offline checker also concatenates the frozen statement and audit probe in a temporary Lean
module. It proves the canonical declaration and audit copy definitionally equivalent by `Iff.rfl`,
then checks the audit candidate directly at the canonical declaration's type. This binds the
adapter to the statement itself rather than relying on a normalized prose comparison.

Lean prints the terminal body. It is a direct application of `ComputablePred.rice`, using the
terminating `Nat.Partrec.zero` and divergent `Nat.Partrec.none` witnesses. Machine axiom reports
for the terminal theorem and exact adapter are both exactly `propext`, `Classical.choice`, and
`Quot.sound`. The pinned source body and target-owned adapter have no proof placeholder, bodyless
declaration, unsafe or opaque body, oracle, external code, or generated certificate.

The repo-local THM-M-0707 duplicate supplied an adapter discovery lead only. Its declaration,
receipt, and target state were not imported or credited. The wrapper was reimplemented and checked
inside THM-M-0741 ownership. Adjacent mathlib semidecidability, complement, and Rice declarations
are deduplicated support rather than additional exact proof bodies.

Bounded public search also found `FormalizedFormalLogic/Foundation` at immutable commit
`c28942b...`. Its halting-named theorem is a commented first-incompleteness application, not the
pair target; the surrounding commented bridge sketches contain `sorry`. The immutable archive is
recorded and the candidate is excluded as statement-mismatched and inactive. Historical mathlib3
is provenance rather than Lean 4 completion. Anonymous GitHub code search and grep.app were
unavailable, so discovery saturation is not claimed.

The exact route is `M0-W`-shaped, but it is not a legal current `M0-W` status because this worker
packet is deliberately below release-grade `E1`: full content-addressed transitive declaration,
compiled-artifact, executable, foundation, and TCB closure belongs to later validation and master
acceptance. The accepted root therefore remains `[H1, M3, R4]`. Neither `AUDIT-Z` nor theorem
completion is claimed.

## Commands And Results

All local validation ran in this worker clone against the automation-provided canonical `.lake`
symlink read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard structure and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0741` | 0 | rank 1329; planned; L0/rework-required; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | exact revision `8a1783...ea95`, tree `bdc39a...5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; dependency worktree clean |
| scoped repo-local, pinned mathlib, and pinned flt-regular `rg` queries from `anchor-audit.json` | 0 | duplicate-family wrapper lead and unique pinned mathlib terminal located; no flt-regular match |
| bounded Sourcegraph searches recorded in `anchor-audit.json` | 0 | 13 `halting_problem` matches in mathlib4, Foundation, and historical mathlib3; two alternate queries returned zero; response hashes recorded |
| anonymous GitHub repository and code queries recorded in `anchor-audit.json` | 0 / HTTP 403 | repository metadata returned a complete zero result; code search was rate-limited and receives no negative-search credit |
| grep.app queries recorded in `anchor-audit.json` | HTTP 429 | Vercel checkpoint; response hashes recorded as access failures only |
| HTTPS codeload inspection of `FormalizedFormalLogic/Foundation@c28942b...` | 0 | archive SHA-256 `477e6268...5975`; source, toolchain, manifest, license, commented boundary, placeholders, and target mismatch classified |
| `lake env lean ../../Stage1_Instances/THM-M-0741/Statement.lean` from `Formalizations/Lean` | 0 | prerequisite exact target, five expected `#check_failure` mismatch diagnostics, boundaries, statement transport axiom report, and explicit expression re-elaborated on the current pinned closure |
| `lake env lean ../../Stage1_Instances/THM-M-0741/AnchorAudit.lean` from `Formalizations/Lean` | 0 | terminal type/body, adjacent types, exact adapter, explicit target, and two axiom reports checked; stdout SHA-256 `fab3027f...ba5` |
| `python3 -B Stage1_Instances/THM-M-0741/check_anchor_audit.py` | 0 | authority metadata, exact target, pins, clean dependency, blobs, hashes, body markers, candidate ledger, receipt, optional worker packet, definitional statement identity, canonical candidate closure, trust boundary, and narrow Lean replay passed |
| `python3 -m json.tool` on anchor ledger, receipt, and root worker packet | 0 | all structured artifacts parsed |
| scoped prohibited-construct scan over `AnchorAudit.lean` and the pinned terminal region | 1 (expected no match) | no proof gap, axiom declaration, unsafe or opaque body, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0741 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Status Boundary

This phase supplies provisional, self-tested anchor evidence pending dependency-ordered master
acceptance. The obligation registry, proof-phase integration, full provenance/trust and TCB
closure, primary-source and readable reconstruction review, hermetic and independent validation,
deterministic release bundle, `AUDIT-Z`, and theorem completion remain open.
