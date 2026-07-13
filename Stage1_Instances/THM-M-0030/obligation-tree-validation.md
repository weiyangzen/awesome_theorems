# THM-M-0030 obligation-tree validation

Item: `S56-M-0030-OBLIGATION_TREE`. Base revision:
`a16584a808446057f9ca2f2f26e76230cf45b84f`; base tree:
`af0da30f285b30a34f3ead4689f614670d8bef98`.

Validation ran in the worker clone on 2026-07-13. It reused the existing pinned Lean and mathlib
closure read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard structure and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, execution ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0030` | 0 | rank 1075, planned, L0/rework-required, theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only the automation-provided untracked `.lake` link; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `python3 -B Stage1_Instances/THM-M-0030/build_obligation_artifacts.py` | 0 | generated 28 obligations and 70 typed edges; denominator `2c8a39...1c6a45`; full registry digest `c34cd6...01c27` |
| `python3 -B Stage1_Instances/THM-M-0030/check_obligation_tree.py` | 0 | deterministic regeneration, predecessor and registry hashes, denominators, all node fields and ledgers, seven graph types, reciprocal proof edges, pinned bodies, exact internal conditional Lean replay, receipt, status boundary, and ownership passed; seven composition declarations reported only `propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx` |
| `python3 -m json.tool` on all changed structured JSON | 0 | every structured artifact parsed |
| Python syntax compilation with `PYTHONPYCACHEPREFIX` outside the repository | 0 | builder and checker compiled without repository bytecode |
| scoped `rg` scan of `ObligationTree.lean` and pinned body lines 392-435 | 1 (expected no match) | no placeholder, axiom declaration, unsafe/oracle/backend, opaque, or external-code marker |
| `git diff --check -- Stage1_Instances/THM-M-0030 .stage1-worker-selftest.json` plus no-index checks for new files | 0 | no whitespace diagnostics |

The structural validator treats the exact mathlib theorem as the one deduplicated terminal body.
Distinct imported finite-module, Jacobson, unit, fixed-point, stability, and Nakayama declarations
have separate proof-body identities; local containment and power induction remain separately owned
semantic obligations without fabricated body identities. Only interfaces with explicit
conditional Lean terms have
`proof_requires`/`composes` edges; visible source internals without local terms remain open
`logical_decomposition` edges.

## Status boundary

The registry and typed architecture are self-tested. Accepted proof state and accepted receipt IDs
remain empty, and the root stays `[H1, M3, R3]`. H0, E1/M0 acceptance, R0, complete provenance and
trust, proof integration, hermetic and independent validation, release, `AUDIT-Z`, and theorem
completion remain open.

The provisional receipt is deliberately `content_addressed=false`; it is a worker handoff and
cannot satisfy master acceptance or release evidence requirements by itself.
