# THM-M-0912 anchor-audit validation

Item: `S56-M-0912-ANCHOR_AUDIT`

Base revision: `72e9e8092182121a6794921f61fcc9cae22f726d`; tree
`0d6c1fdf06d1573c256af331c6b198e5a787af43`. Validation date: 2026-07-13
(`Asia/Shanghai`).

## Result

The exact constrained target has a route through pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The closest terminal theorem is
`Nat.choose_eq_choose_pred_add` in `Mathlib.Data.Nat.Choose.Basic`: its positive row and column
premises follow from `1 <= n <= m`, and commuting the summands yields the target literally.
`AnchorAudit.lean` checks this adapter and a second reindexing adapter through the
definitionally proved `Nat.choose_succ_succ'`. The checker compares fully explicit elaborated
expressions, so neither the broader all-natural recurrence nor a different binomial identity is
substituted for the frozen proposition.

The terminal definition and recurrence family live in
`Mathlib/Data/Nat/Choose/Basic.lean:45-82`, pinned by commit, tree, Git blob, file hash, and source
slice hashes. Lean reports no axioms for `Nat.choose_succ_succ` or its prime form. The positive
predecessor lemmas and both exact adapters report only `propext`; all seven inspected declarations
are machine-reported sorry-free. The actual bodies are transparent: the successor forms are
`rfl`, while the closest predecessor theorem reindexes a positive column and invokes
`Nat.choose_succ_right`. A comment-aware supplemental scan finds no prohibited proof escape,
unsafe declaration, external code, or oracle marker in the adapter or direct source module.

This establishes only a provisional `M0-W` route candidate. It is not release-grade accepted `E1`,
has not been adopted by the proof phase, and cannot change the accepted root from `[H1, M3, R4]`.
Full transitive declaration, compiled-artifact, TCB, supply-chain, obligation-composition, hermetic,
and independent-verification closure remains downstream.

## Discovery

The discovery protocol was frozen before external queries. Repository-local and all ten
materialized non-mathlib manifest packages contain no independent selected declaration. Other
mathlib matches are uses, adjacent recurrences, derived identities, or a different ring-valued
object. An inline exact-formula step in `KruskalKatona.lean` calls the same recurrence and is not a
separate named terminal body.

Sourcegraph found `choose_eq_choose_pred_add` only in indexed mathlib4. A broader
`choose_succ_succ` query found mathlib plus public downstream users; sampled Lean 4 repositories
call the mathlib theorem rather than supply an independent Pascal-identity body. Exact English-name
queries returned zero within that index. Two GitHub repository-metadata queries returned complete
zero-result responses before anonymous rate exhaustion. Later GitHub repository/code queries were
rate-limited, and grep.app returned a Vercel security checkpoint. Those are access failures, not
negative evidence. Search responses are dated discovery records only; the selected candidate is
bound to the local manifest pin, not Sourcegraph's newer indexed mathlib commit. Saturation is not
claimed.

## Commands and exact outcomes

Commands ran from the repository root unless a `cwd` is shown. Existing canonical Lake artifacts
were used read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was
performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets in ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0912` | 0 | rank 1454, planned, no legacy slot, legacy evidence unaccepted, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386...ea95`; tree `bdc39a31...5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned mathlib worktree clean |
| manifest-package revision/status loop | 0 | all eleven materialized packages matched their manifest revisions and were clean at final validation |
| bounded `rg` inventory over repo-local and materialized manifest-package sources | 0 aggregate | only the pinned mathlib terminal family plus duplicate uses/adjacent results; no independent local body |
| `LC_ALL=C LANG=C NO_COLOR=1 lake env lean ../../Stage1_Instances/THM-M-0912/AnchorAudit.lean` (`cwd=Formalizations/Lean`) | 0 | two exact adapters elaborated; two axiom-free terminal reports, five `propext` reports, seven sorry-free reports; stdout SHA-256 `0eb74a20...d862` |
| GitHub repository/code REST queries recorded in `anchor-audit.json` | mixed | two complete repository zero-results; subsequent queries HTTP 403 rate-limit failures |
| Sourcegraph streaming queries recorded in `anchor-audit.json` | 0 | exact predecessor name only in mathlib; broad recurrence matches classified; English exact-name queries zero with `skipped=[]` |
| grep.app API queries recorded in `anchor-audit.json` | HTTP 429 | Vercel checkpoint; explicit access failure, no negative claim |
| `python3 -B Stage1_Instances/THM-M-0912/check_anchor_audit.py --worker-packet .stage1-worker-selftest.json` | 0 | authority identity, exact expression match, immutable pins/source hashes, five candidate groups, trust boundary, receipt, and worker packet agree |
| `python3 -B Stage1_Instances/THM-M-0912/check_intake.py --worker-packet .stage1-worker-selftest.json` | 1 | historical predecessor checker rejects the intentionally expanded owned-file inventory; its immutable intake receipt was not rewritten, while the anchor checker independently validates current authority and statement inputs |
| `python3 -B ../../Stage1_Instances/THM-M-0912/check_statement.py --measure-only` (`cwd=Formalizations/Lean`) | 0 | statement expression, mutation, import-deletion, and toolchain measurements still execute against the unchanged statement source |
| `python3 -m json.tool` on the protocol, audit, receipt, and worker packet | 0 | all structured artifacts parse |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0912-anchor-pycache python3 -m py_compile Stage1_Instances/THM-M-0912/check_anchor_audit.py` | 0 | scoped validator compiles without owned-path cache output |
| scoped prohibited-construct scans and `git diff --check -- Stage1_Instances/THM-M-0912 .stage1-worker-selftest.json` | expected no-match / 0 | no prohibited construct in new Lean/source body; no whitespace diagnostics |

## Boundary

This self-tests only the bounded anchor-audit node. Intake and statement proposals plus this audit
still require dependency-ordered master acceptance. The obligation registry, proof-phase adoption
and composition, primary-source `H0`, readable `R0`, complete provenance/trust and release-grade
`E1`, hermetic replay, independent verification, deterministic release bundle, `AUDIT-Z`, and
theorem completion remain open.

The earlier intake checker freezes the statement-phase file inventory and therefore reports an
inventory assertion after these new anchor artifacts appear. That predecessor receipt is immutable
historical evidence, so this phase does not rewrite it. The current anchor checker instead binds the
unchanged statement source and expression hashes and validates current target/DAG identity directly.
