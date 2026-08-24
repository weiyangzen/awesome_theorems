# Machine-checked audit

The three claim-owned Lean files were elaborated separately with the pinned repository toolchain and `lean --trust=0`. Each file has an exact provider-authority marker, contains no `sorry`, `admit`, claim-specific axiom, unsafe declaration, opaque oracle, local semantic definition, parser extension, coercion, or namespace alias, and exposes only theorem declarations.

The source theorem's own `sorryAx` is excluded from the machine root: the source is a statement provider, while the target declarations check transparent proposition transport and typed composition. The recorded target axiom census is empty. A cold replay disables the Lake cache and re-elaborates each claim-owned file from source.

Machine level is `M0-L`; trust is zero and the remaining machine cut set is empty. Master must independently reconstruct the expression and declaration census after integration.
