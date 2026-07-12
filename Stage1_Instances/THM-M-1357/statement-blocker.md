# Exact-statement gate: blocked

Item: `S56-M-1357-STATEMENT`

Theorem: `THM-M-1357`

Base revision: `0d26adeae663d55eb536120f7d93ede975fe8f49` (tree
`6b5ab44050900e9a4a181b4fc56b1e965183f2c9`)

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only `Nyquist稳定性判据` (Nyquist stability criterion), Harry Nyquist, 1932,
and the gloss `反馈系统的稳定性` (stability of a feedback system). It provides no cited
truth-valued proposition, definitions, ordered binders, hypotheses, conclusion, or boundary cases.
Stage0 explicitly leaves the formal system, exact definitions and premises, proof route,
equivalent statements, axioms, machine status, and artifact links open. The catalog value `已验证`
is untrusted metadata under rev-5.6.

The wording identifies a theorem family rather than one proposition. A source-selected criterion
must still choose the feedback topology and sign, continuous- or discrete-time semantics, scalar
SISO or matrix MIMO scope, transfer-function or state-space model, admissible analytic class,
stability predicate and region, Nyquist contour and orientation, and the signs and meanings of the
pole, zero, and encirclement counts. It must also settle boundary-axis poles and zeros, a plot that
passes through the critical point, cancellations and minimality, multiplicity, well-posedness, and
all degenerate cases.

Those choices materially change the claim. An argument-principle identity such as `N = Z - P`, a
necessary-and-sufficient closed-loop stability criterion, a determinant-based MIMO theorem, and a
discrete-time unit-circle theorem are not interchangeable targets. Selecting one from memory would
invent missing mathematics. Encoding the desired count or stability conclusion as a structure
field would instead assume it. Both substitutions are prohibited.

The intake therefore correctly leaves the canonical human statement, Lean module and expression,
minimal imports, and expression/environment fingerprints null. Without one canonical target, there
is no meaningful alternate-form transport or removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutation suite. No `Statement.lean`, axiom, placeholder,
weakened special case, or broadened interface was added.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated against the pinned environment. Its three direct
imports expose meromorphic divisors and orders, logarithmic derivatives, and a complex-circle
parameterization. All six checked interfaces elaborate. They are adjacent complex-analysis APIs
only: the probe defines no feedback system or winding convention and states no Nyquist theorem.
Its imports cannot be certified minimal for an unknown target, and the successful check receives
no statement, anchor, or proof credit.

A bounded name search over `Formalizations/Lean/AwesomeTheorems` and pinned Mathlib found no
declaration matching the recorded Nyquist, feedback-control, transfer-function, encirclement,
winding-number/index, or argument-principle regex. This is a local feasibility boundary, not the
later immutable anchor audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned Mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the
`lake-manifest.json` SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`; and the probe SHA-256 is
`b944885886f1898335c1c21c8add5d4aa648870d5b6aa2e08684ae7db9748dcb`.

The automation-provided `Formalizations/Lean/.lake` link to canonical pinned artifacts was used
read-only. No update, build, dependency clone, fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Commands ran from the repository
root unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1357` | 0 | rank 967, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake match the pinned environment fingerprint above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision and tree match the fingerprint above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; the pinned package worktree is clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-1357/IntakeProbe.lean` | 0 | all three hashes match the structured blocker |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1357/IntakeProbe.lean)` | 0 | six adjacent divisor, order, logarithmic-derivative, and circle interfaces elaborated; no target theorem was checked |
| bounded `rg` search for Nyquist, feedback-control, transfer-function, encirclement, winding-number/index, and argument-principle patterns in `Formalizations/Lean/AwesomeTheorems` and pinned Mathlib | 1 | expected no-match result; no target-specific declaration was located under the recorded regex |
| `python3 -B Stage1_Instances/THM-M-1357/check_intake.py` | 1 | historical intake replay expects its intake node to remain `[ ]`; current authoritative projection is `[_]`, so the intake-only checker is stale and was not rewritten by this phase |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-1357` | 1 | expected no-match result; the API-only probe contains no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1357/statement-blocker.json` | 0 | the finalized structured blocker parsed as valid JSON |
| scoped statement-blocker invariant assertions | 0 | IDs, rank, blocked verdict, null target and fingerprints, unchanged `[H5, M4, R4]`, false completion flags, exact changed paths, and absent worker packet agree |
| per-file `git diff --no-index --check /dev/null` for both new blocker artifacts | 1 per file | expected new-file difference status with no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | the worker packet is absent because the statement completion gate did not pass |

The intake prerequisite itself is only worker-provisional `[_]`, its receipt is not accepted, and
its historical checker freezes pre-integration authority and file inventory. This statement phase
does not rewrite or refresh separately owned intake evidence. That freshness/dependency issue
independently prevents statement-node acceptance.

## Retry condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash an immutable primary or authoritative source, select and transcribe one exact
truth-valued Nyquist theorem and every incorporated definition with pinpoint locators, audit
corrections and errata, and independently approve the source crosswalk. The source must fix the
exact model, sign, domain, analytic class, stability, contour, orientation, count, cancellation,
multiplicity, conclusion, and all applicable boundary assumptions and exclusions listed above.

A later statement worker can then encode that same claim using real Lean definitions, minimize its
pinned imports, freeze faithful ordered binders, universes, and typeclass context, serialize and
hash the elaborated expression and environment, explicitly scope nonapplicable cases, check every
credited transport, and execute all four required mutation classes.

This is the first failed gate, not completion of the statement node or a downstream node. The root
remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted and no statement-node or master-acceptance receipt is
claimed.
