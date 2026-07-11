import Init

/-!
# THM-M-0392 anchor-audit probe

This dependency-minimal probe re-elaborates the audited root expression. The
audited mathlib checkout has useful elliptic-curve object APIs, but no terminal
integral-points finiteness theorem to import here.
-/

namespace Stage1Instances.THMM0392.AnchorAudit

def IsFinite (α : Type) : Prop :=
  ∃ n : Nat, ∃ encode : α → Fin n, Function.Injective encode

def AuditedRootExpression : Prop :=
  ∀ k : Int, k ≠ 0 →
    IsFinite {p : Int × Int // p.2 ^ 2 = p.1 ^ 3 + k}

#check AuditedRootExpression

end Stage1Instances.THMM0392.AnchorAudit
