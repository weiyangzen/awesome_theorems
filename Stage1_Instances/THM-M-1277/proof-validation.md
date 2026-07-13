# THM-M-1277 proof execution

Item: `S56-M-1277-PROOF`
Date: `2026-07-14` (`Asia/Shanghai`)
Base revision: `bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`

## Verdict

`blocked`. The exact frozen Lean proposition is false. `Proof.lean` gives a
kernel-checked, placeholder-free proof of
`Stage1Rev56.THMM1277.not_statement : Not Statement`.

The first failed gate is exact canonical statement correctness. In
`SmoothCompactIn`, `ContDiff Real ⊤` elaborates at the top of
`WithTop ℕ∞`, which mathlib calls order `omega`: real analyticity. It is not
the smooth order `infinity`, represented by the coerced top of `ℕ∞`.
Analytic uniqueness makes every compactly supported approximant identically
zero. Therefore every scalar field admitted by `ZeroBoundarySobolev` is zero
almost everywhere, and its exponential integral over `Omega` is exactly
`volume Omega` for every exponent. On the bounded nonempty open unit ball,
the sharpness conjunct asks for an admissible integral strictly larger than
that same finite volume, a contradiction.

This is a refutation of the frozen formal target, not a proof of the intended
Moser-Trudinger theorem. No obligation or theorem-completion credit is
claimed. The registry and typed graphs still describe the now-invalid planned
proof route and require correction by the owning earlier phases and master
lane. `.stage1-worker-selftest.json` is deliberately absent because the
assigned proof deliverable cannot pass for a false target.

The recorded provisional dossier root remains `[H1, M3, R3]`; this worker does
not mutate authoritative debt state. The countertheorem warrants proposed root machine
classification `M5` for statement mismatch. The classical human theorem is
not refuted, so the human/source axis remains `H1` pending the source owner's
correction of the formal encoding rather than being reclassified here as
`H5`.

`Proof.lean` also proves useful local facts found during diagnosis: the zero
field is admissible, bounded domains have finite volume, every frozen analytic
compact-support approximant is zero, the completion collapses almost
everywhere, every admissible exponential integral equals the domain volume,
and every nonempty open domain contains a positive-radius closed ball. These
are blocker evidence, not closure of the frozen positive proof architecture.

## Narrow validation evidence

All commands ran in this worker clone and reused the existing pinned Lake
artifacts through the worker's untracked `.lake` symlink. No update, build,
dependency clone/fetch, or `.lake` mutation was performed. This is dirty,
nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1277` | 0 | rank 328, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-1277/check_obligation_tree.py` | 0 | existing 24-obligation, 48-edge architecture is structurally valid but still reports the stale pre-refutation root as open `M3` |
| `TMP=/tmp/thm-m-1277-proof-final; rm -rf "$TMP"; mkdir -p "$TMP"; BASE=$(lake env printenv LEAN_PATH); lake env lean --root=../.. -o "$TMP/Statement.olean" ../../Stage1_Instances/THM-M-1277/Statement.lean && LEAN_PATH="$TMP:$BASE" lake env lean --root=../.. ../../Stage1_Instances/THM-M-1277/Proof.lean; result=$?; rm -rf "$TMP"; exit "$result"` (from `Formalizations/Lean`) | 0 | the fresh temporary `Statement.olean` and final imported proof both elaborated; `not_statement : Not Statement`; every listed axiom report exactly `propext`, `Classical.choice`, `Quot.sound`; temporary output removed |
| `lake env lean --root=../.. ../../Stage1_Instances/THM-M-1277/Statement.lean` (from `Formalizations/Lean`) | 0 | frozen target still elaborated as `Stage1Rev56.THMM1277.Statement : Prop` |
| `lake env lean --root=../.. ../../Stage1_Instances/THM-M-1277/ObligationTree.lean` (from `Formalizations/Lean`) | 0 | conditional composition elaborated with the same three axioms; it does not supply its false sharpness premise |
| independent review: repeat the fresh temporary-olean proof recipe above | 0 | a separate reviewer confirmed the exact refutation chain, exact target type, and axiom report; no proof issue found |
| `lake env lean --version` (from `Formalizations/Lean`) | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 -m json.tool Stage1_Instances/THM-M-1277/proof-blocker.json >/dev/null` | 0 | structured blocker record is valid JSON |
| `rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|unsafe)\b' Stage1_Instances/THM-M-1277 --glob '*.lean'` | 1, expected | no prohibited proof placeholder, declared axiom, or unsafe declaration |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1277/Proof.lean` | 1 | expected for an added file; no whitespace diagnostic was printed |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1277/proof-validation.md` | 1 | expected for an added file; no whitespace diagnostic was printed |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1277/proof-blocker.json` | 1 | expected for an added file; no whitespace diagnostic was printed |

The temporary output directory was outside the repository and was removed
after validation. Nothing was written into `.lake`.

## Structured handoff

- Intent: `prove` for item `S56-M-1277-PROOF`, root obligation `M1277-ROOT`.
- Lifecycle: `planned -> planned`; audit complete: `false`; theorem complete:
  `false`.
- Root vector: recorded provisional `[H1, M3, R3] -> [H1, M3, R3]`;
  proposed diagnosis `[H1, M5, R3]`, pending integration-lane review and a
  corrected statement.
- Accepted receipt IDs: none.
- First failed gate: exact canonical statement correctness.
- Remaining root cut set: `S56-M-1277-STATEMENT`.
- Status boundary: blocker/refutation evidence only; no proof-node receipt or
  state transition is requested.

## Retry condition

Return to the statement phase and replace analytic order `⊤` with the intended
smooth order, written unambiguously as
`((⊤ : ℕ∞) : WithTop ℕ∞)` (scoped notation `∞`), then rerun statement
identity, source mapping, mutation, obligation-registry, and typed-graph gates
before any new proof attempt. That corrected proposition is a new statement
fingerprint and cannot inherit proof credit from this refuted target.
