# Machine-checked audit

Root: `AwesomeTheorems.Stage5.S5_CLM_00003502.zariskiCancellationDimOne`.

- Toolchain: `leanprover/lean4:v4.29.0`.
- Kernel setting: `--trust=0`.
- Replay mode: cold, offline, `LAKE_NO_CACHE=1` under the pinned Lake graph.
- Placeholder scan: no `sorry`, `admit`, local axiom, unsafe declaration, or
  opaque oracle occurs in the three claim-owned Lean artifacts.
- Source shadow scan: no local definition, abbreviation, instance, notation,
  syntax, macro, coercion, namespace alias, or substitute semantic symbol.
- Observed root axioms: empty.
- Remaining machine cut set: empty.

The frozen Formal Conjectures declaration is referenced to bind identity, not
counted as proof authority. Canonical acceptance still requires the Master to
recompute the elaborated expression and transitive environment after applying
the handoff patch.
