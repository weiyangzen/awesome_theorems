# Proof outline

For the readability ledger, each fragment digest is SHA-256 of the exact UTF-8 bytes strictly
between its matching `BEGIN` and `END` marker lines, including the terminating newline.

<!-- BEGIN F1 -->
## 1. Witness at thirteen

With no hypotheses, choose `A = {3, 6, 11, 12, 13}`. A closed finite decision verifies interval
membership, cardinality five, and injectivity of all 32 subset sums. This outputs existence at
thirteen for node N1 and is consumed by N4. Its formal anchor is
`AwesomeTheorems.Stage5.S5_CLM_00003549.audit_witness_at_thirteen`; there are no exceptional
cases, and the trust boundary is kernel-checked finite reduction.
<!-- END F1 -->

<!-- BEGIN F2 -->
## 2. Finite exclusion through twelve

With no hypotheses, enumerate the powerset of `Icc 1 12`, filter for cardinality five and
injective subset sums, and decide that the result is empty. This outputs nonexistence at twelve
for node N2 and is consumed by N3. Its formal anchor is
`AwesomeTheorems.Stage5.S5_CLM_00003549.audit_no_witness_at_twelve`; there are no exceptional
cases, and the trust boundary is kernel-checked finite reduction under explicit resource limits.
<!-- END F2 -->

<!-- BEGIN F3 -->
## 3. Monotonic lower bound

Assume a candidate at `N` and enter the exceptional contradiction branch `N ≤ 12`. Every member
of its ambient interval then also lies in `Icc 1 12`, while subset-sum injectivity and cardinality
are unchanged. N2 yields a contradiction, so `13 ≤ N`. This is node N3, consumed by N4, with
formal anchor `AwesomeTheorems.Stage5.S5_CLM_00003549.audit_lower_bound_thirteen`; its trust
boundary is ordinary kernel theorem composition.
<!-- END F3 -->

<!-- BEGIN F4 -->
## 4. Exact-root composition

With the N1 existence output and N3 lower-bound output, apply the two fields of `IsLeast`. This
produces the frozen target proposition as node N4. Its formal anchor is
`AwesomeTheorems.Stage5.S5_CLM_00003549.machine_root`, its downstream use is the exact-type
witness and terminal axiom query in `Audit.lean`, it has no exceptional cases, and its trust
boundary is the independently reconstructed claim-owned root.
<!-- END F4 -->
