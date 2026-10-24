# Design outline

Use the sections that help another developer make the change. Match an existing
project format when present; this outline is not a readiness schema.

- **Problem and intended behavior:** concrete caller/user example; scope and
  constraints established by the request.
- **Current implementation:** inspected files and reusable patterns; facts
  distinguished from assumptions.
- **Decision:** chosen approach, alternatives considered, and important tradeoffs.
- **Contracts:** public interface, data flow, validation and failure behavior;
  compatibility or migration only where affected.
- **Acceptance criteria:** observable outcomes and how each will be checked.
- **Open questions and authorization:** unresolved choices; proposed versus
  accepted decisions; whether implementation has been requested.

Include technical sources when they support a decision. Avoid speculative code
listings, mandatory phase counts, or sections unrelated to the change.
