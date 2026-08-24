# Machine-checked audit

The claim-owned machine certificate is M0-P with trust level zero, an empty observed-axiom list, an empty machine cut set, and a cold-from-source replay obligation. The root declaration and declaration census are content-addressed in `machine-closure.json`; the canonical Master recomputes the elaborated root expression and all transitive non-foundation bindings.

No `sorry`, `admit`, unsafe declaration, opaque oracle, or claim-specific axiom is present in the Lean surfaces. The provider's `sorryAx` is explicitly excluded from proof authority.
