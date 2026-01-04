import React, { useState } from "react";

export default function CommandBar({ onSubmit }) {
  const [text, setText] = useState("");

  const submit = async (e) => {
    e?.preventDefault();
    if (!text.trim()) return;
    await onSubmit(text.trim());
    setText("");
  };

  return (
    <form className="cmdbar" onSubmit={submit} role="search" aria-label="Unified Command Bar">
      <input
        id="cmd-input"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Try: 'search rust guides', 'open example.com', 'summarize'"
        aria-label="Unified Command Bar"
        autoComplete="off"
      />
      <button type="submit" aria-label="Run command">⏎</button>
    </form>
  );
}
