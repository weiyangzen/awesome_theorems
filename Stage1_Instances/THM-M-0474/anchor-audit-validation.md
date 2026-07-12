# THM-M-0474 anchor-audit validation

Item: `S56-M-0474-ANCHOR_AUDIT`

Base revision: `3ed74ce8b03564707b34b6e2314d2bb6d0a6206e`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact candidate
`Nat.ModEq.pow_card_sub_one_eq_one` in `Mathlib.FieldTheory.Finite.Basic`. Its natural-number
domain, prime and coprime premises, exponent, modulus, and conclusion agree with the frozen target.
`AnchorAudit.lean` independently restates that target and its adapter elaborates as
`fun p a hp ha => Nat.ModEq.pow_card_sub_one_eq_one hp ha`.

Lean's transitive `assert_no_sorry` check passes for the upstream theorem and audit wrapper;
`#print sorries` reports that the declarations are sorry-free. Both axiom probes report exactly
`propext`, `Classical.choice`, and `Quot.sound`. The visible source chain is the natural wrapper,
the integer congruence theorem, the nonzero `ZMod` theorem, the finite-field theorem, and the finite
group `pow_card_eq_one` theorem. Their pinned source hashes are recorded in `anchor-audit.json`.
Full transitive provenance, TCB, and computation closure remains a downstream gate.

The manifest-pinned `flt-regular` package only consumes the integer mathlib theorem and supplies no
independent exact root. Public discovery also classified `little4` and two student Lean 4 sources;
they use integer, `ZMod`, or all-base encodings, different or missing pins, and in two cases fail a
local compatibility replay. The older `encryptedsalad` source is Lean 3 and has no terminal Fermat
little theorem. A complete bounded Sourcegraph query returned 73 matches in 14 indexed repositories;
the remaining Lean 4 hits were mathlib itself or downstream consumers. This is bounded discovery,
not an exhaustive global-absence claim.

The exact upstream is therefore recorded as an `M0-W_candidate_pending_downstream_acceptance`.
The authoritative planned root remains `[H1, M3, R4]`: this phase does not install the proof-phase
canonical wrapper or create accepted proof state. Full audit completion and theorem completion are
both false.

## Commands and exact outcomes

All commands ran in this worker clone. Lean used the existing manifest-pinned shared Lake artifacts.
No `lake update`, build, dependency clone/fetch, or other `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0474` | 0 | rank 938, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | mathlib revision `8a1783...a95`, tree `bdc39a...c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned mathlib source worktree clean |
| `lake env lean -t 0 ../../Stage1_Instances/THM-M-0474/AnchorAudit.lean` (`cwd=Formalizations/Lean`) | 0 | exact wrapper elaborated; both declarations sorry-free; both axiom sets printed |
| `lake env lean ../../Stage1_Instances/THM-M-0474/Statement.lean` (`cwd=Formalizations/Lean`) | 0 | predecessor target, checked premise transport, expression, and four expected mutation rejections re-elaborated |
| `python3 Stage1_Instances/THM-M-0474/check_anchor_audit.py` | 0 | seven candidates, pins, hashes, exact source markers, visible body chain, and fail-closed boundary verified |
| `python3 ../../Stage1_Instances/THM-M-0474/check_statement.py` (`cwd=Formalizations/Lean`) | 0 | predecessor fingerprints, transports, minimal imports, and four mutations remain valid |
| `python3 Stage1_Instances/THM-M-0474/check_intake.py` | 0 | expanded dossier remains planned at H1/M3/R4 with six open tasks |
| `python3 -m json.tool Stage1_Instances/THM-M-0474/anchor-audit.json` | 0 | structured candidate ledger is valid JSON |
| GitHub repository metadata and immutable commit/tree/raw inspections | 0 | three dedicated repositories and one additional exact-alias project classified without cloning |
| Sourcegraph bounded code-index query recorded in `anchor-audit.json` | 0 | complete response: 73 matches in 14 indexed repositories |
| GitHub unauthenticated code search | 22 | HTTP 401 access failure recorded; no negative-result claim |
| `git diff --check -- Stage1_Instances/THM-M-0474 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Boundary

This self-test supports only the provisional anchor-audit node, pending master acceptance. The
exact candidate still requires a frozen obligation registry, proof-phase integration, accepted
terminal provenance/trust and TCB closure, source/readability work, hermetic replay, independent
verification, and release evidence. It supplies no theorem-completion receipt.
