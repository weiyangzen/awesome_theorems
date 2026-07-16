# Statement gate blocker

Item: `S56-M-0445-STATEMENT`<br>
Theorem: `THM-M-0445`<br>
Worker verdict: `blocked`<br>
Phase accepted: `false`

## First failed gate

`S02-EXACT-TARGET.exact_source_statement_identity_and_theorem_variant_selection`

The exact Lean 4 target cannot be selected from the admitted repository source. The complete human
statement attached to this target is `椭圆曲线的BSD` (BSD for elliptic curves), while the target
name is Rubin-Kolyvagin theorem. The source gives no theorem citation, curve hypotheses,
analytic-rank restriction, CM/Iwasawa or Heegner-point assumptions, or precise conclusion. In
particular, it does not decide between:

- equality of analytic and Mordell-Weil ranks plus finiteness of the Tate-Shafarevich group in an
  analytic-rank-at-most-one setting; and
- the stronger full BSD leading-term formula.

Selecting either candidate would add unstated hypotheses and choose an unstated conclusion. This is
the exact-statement hard blocker described by section 5 of `Docs/Stage1_Blueprint_rev-5.6.md`.
Consequently no canonical expression hash, canonical-target minimal-import claim, checked alternate
transport, or semantic mutation suite can be produced in this phase.

The historical module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_091.lean` elaborates, but its
own documentation identifies `StatementShape` and `FullBSDStatementShape` as abstract, competing
discovery boundaries. Their proposition-valued fields stand in for the missing elliptic-curve
L-function, Mordell-Weil rank, Tate-Shafarevich group, and Euler/Kolyvagin-system APIs. Elaboration
of that module is environment evidence only, not elaboration of the exact target.

## Dependency and reuse audit

The authoritative v2 rank is `315`; the phase layer is `1`; the item ID is
`S56-M-0445-STATEMENT`. The complete direct and transitive hard-parent inspection order is empty.
The direct-parent, transitive-ancestor, hard-edge, reuse-hint, and shared-group lists are all empty.
`dependency-reuse-ledger.json` records that exact audited closure against graph digest
`e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b` and dependency-context
digest `068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`. No body was inspected,
copied, transported, or credited, and no provider acceptance is inherited.

## Lean boundary

`Statement.lean` checks only pinned adjacent vocabulary for elliptic-curve rational points, generic
L-series, and a Dedekind-domain Selmer group. It deliberately declares no canonical target,
theorem, proposition alias, proof body, or credited transport. A successful elaboration of that
probe proves only that the vocabulary is available; it cannot satisfy the exact-target gate.

The validator candidate is new in this worker delta. The HEAD contract requires a validator to
exist at the worker base with the identical HEAD blob before it can be selected for authority
replay. Therefore this run can only bootstrap the validator and blocker artifacts for a later
fresh-base replay; its local exit code is not acceptance evidence.

## Retry condition

Admit and independently review one exact primary or approved-authoritative Rubin or Kolyvagin
theorem passage with a stable edition, theorem/page locator, incorporated definitions, ordered
hypotheses, precise conclusion, correction, and errata disposition. Statement work can then encode
only that claim, minimize imports, fingerprint the elaborated expression and environment, check
every credited transport, and execute the four required mutation classes.

This target-owned blocker advances no proof, phase acceptance, audit completion, theorem
completion, or master acceptance.
