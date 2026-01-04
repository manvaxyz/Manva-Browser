MANVA Design System — tokens, components, and interaction patterns

Design language
- Futuristic but minimal. Use soft glass materials, subtle depth, and motion for affordances.
- Three modes: Light, Dark, Auto (follows OS). Provide high-contrast accessibility mode.

Core tokens
- Color palette: primary / accent / background / surface / error / success
- Typography scale: H1..H4, Body, Caption. Provide dynamic scaling based on user setting.
- Spacing scale: 4/8/12/16/24/32
- Motion: durations (fast/medium/slow) and easing curves; respect `prefers-reduced-motion`.

Components
- Unified Command Bar
  - Single input for commands and search
  - Modes: text, voice, file search
  - Keyboard access: `Ctrl+Space` or `Cmd+Space`
  - Accessibility: role="searchbox", aria-autocomplete

- Tab Card
  - Compact card with favicon, title, origin trust badge, summary button
  - Actions: close, pin, group

- AI Assistant Pane
  - Collapsible, shows provenance, confidence, and action buttons

- File Previewer
  - Inline preview with in-place editing where possible

Interaction patterns
- One-hand mode (mobile): move primary controls to bottom; enlarge touch targets; use edge swipes for nav
- Adaptive layout: use CSS grid/flex with breakpoint logic and component reflow rules
- Content summarization: single-tap overlay with read-mode toggle

Accessibility checklist
- All interactive controls have ARIA roles and labels
- High-contrast theme and large-text mode
- Focus outlines and keyboard tab order

Motion & performance
- Lazy-load heavy components (PDF editor, video tools) and show skeletons
- Keep first meaningful paint < 1s on modern desktop and < 2s on mid-range mobile

Platform-specific notes
- Android: prefer Jetpack Compose for dynamic layouts and NNAPI for on-device acceleration
- Desktop: Rust + wgpu for GPU acceleration; provide native keyboard and window integrations
