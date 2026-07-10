import Lake
open Lake DSL

package «AwesomeTheorems» where
  -- Keep the shared Lean tree lightweight in git by pinning mathlib through Lake.

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "8a178386ffc0f5fef0b77738bb5449d50efeea95"

require «flt-regular» from git
  "https://github.com/leanprover-community/flt-regular.git" @ "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"

@[default_target]
lean_lib AwesomeTheorems where
  roots := #[`AwesomeTheorems]
