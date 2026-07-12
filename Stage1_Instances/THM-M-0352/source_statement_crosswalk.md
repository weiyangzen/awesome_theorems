# Source-statement crosswalk

| Claim component | Repository source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Name | `Docs/researches/math_theorems.md`: "Calderon-Zygmund theory" | none | Identifies a theory, not a unique theorem |
| Attribution and date | Alberto Calderon / Antoni Zygmund; 1952 | none | Metadata only; no publication or pinpoint result is identified |
| Source wording | "the theory of singular integral operators" | none | Does not specify binders, hypotheses, or conclusion |
| Singular operator | No kernel, truncation, cancellation, or boundedness assumptions given | none | An operator interface cannot be frozen truthfully |
| Domain and range | No dimension, measure space, scalar field, or function spaces given | none | Ordered domains and universes remain unknown |
| Conclusion | No exact estimate or mapping property given | none | Weak type, strong type, endpoint, and weighted results cannot be treated as interchangeable |
| Formal status | Manifest field `source_status_untrusted` is `已验证` | none | The label is intake metadata, not source or kernel evidence |

The same short wording appears in `Docs/Stage0_Blueprint.md`, where its precise definitions,
assumptions, source, equivalent formulations, and machine-checked status are all recorded as needing
further work. It therefore supplies no additional statement detail.

Two nearby records show why silent normalization would be unsafe:

- `THM-M-0298` separately names the Calderon-Zygmund decomposition.
- `THM-M-1171` separately names a Calderon-Zygmund estimate and has chosen a Hessian-by-Laplacian
  formulation for that target.

Neither is evidence that this target means the same proposition. A valid source selection must bind
an immutable primary source to an edition or file hash, theorem/page, every operator and kernel
condition, the exact endpoint range and conclusion, and an errata review. Only then can a later
phase populate quantifiers and hypotheses, select a Lean expression, and test related formal
candidates. No `H0` or machine-closure claim is made.
