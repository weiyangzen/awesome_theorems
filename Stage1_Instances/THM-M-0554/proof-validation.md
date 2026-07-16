# THM-M-0554 proof-phase worker validation

This proof-phase attempt re-audits the exact v2 dependency context at repository
revision `1cc6aa61bb055a5c032297ee457905c849af7608`. The direct-parent and
transitive-ancestor closure is empty, so the required parent inspection order is
the empty list. The one nonblocking shared-module group was inspected through
`THM-M-0540`; its pinned singular-homology artifacts contain no compatible AHSS
terminal body, and the refreshed ledger records `not_applicable` rather than
transferring proof or acceptance credit.

`Proof.lean` contains three genuine placeholder-free declarations. They recompose
four explicit branch packages into the literal `AtiyahHirzebruchData` output and
then package that output as the frozen statement. A trust-zero replay observes
only `propext`, `Classical.choice`, and `Quot.sound`. This is conditional
composition, not an AHSS construction: all branch packages remain premises, all
32 frozen obligations remain open, and no composition certificate is credited.

The first failed gate is
`P04-KERNEL/S56-5.1-EXACT-TARGET-CONSISTENCY/M0554-S-DATA`. The frozen interface
omits reducedness and permits its coefficient, convergence, and naturality
meanings to be selected by the output. A literal zero-container witness would
therefore be a fake result and is not retained or credited. Retrying the same
root cannot close the phase. The predecessor statement and obligation registry
must first be replaced by source-faithful, exact elaborated branch contracts, or
an immutable exact compatible AHSS implementation must enter the pinned closure.

The sole HEAD proof validator is `check_proof.py`. It validates the receipt and
worker packet byte bindings, the empty hard-parent closure, shared-group audit,
frozen denominator and closure boundary, pinned toolchain and mathlib revisions,
source hygiene, and trust-zero Lean replay. Its stdout is exactly one
`stage1-validator-semantic-result/1.0` JSON object. A successful validator exit
means that this blocker packet is truthful; its semantic result remains
`status=blocked`, `phase_accepted=false`, `audit_complete=false`, and
`theorem_complete=false`.
