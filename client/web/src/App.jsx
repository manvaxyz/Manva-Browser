import React, { useState, useEffect } from "react";
import CommandBar from "./components/CommandBar";
import axios from "axios";

export default function App() {
  const [tabs, setTabs] = useState([
    { id: 1, title: "New Tab", url: "about:blank" },
  ]);
  const [activeTab, setActiveTab] = useState(1);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    // keyboard shortcut to focus command bar
    const handler = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.code === "Space") {
        const el = document.getElementById("cmd-input");
        if (el) el.focus();
        e.preventDefault();
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  const runIntent = async (text) => {
    try {
      const res = await axios.post(
        "http://127.0.0.1:8080/intent",
        { text },
        { timeout: 5000 }
      );
      if (res.data && res.data.result) {
        const intent = res.data.result.intent;
        if (intent === "search") {
          openTab(`https://duckduckgo.com/?q=${encodeURIComponent(res.data.result.query)}`, `Search: ${res.data.result.query}`);
        } else if (intent === "open") {
          const target = res.data.result.target || res.data.result.url;
          openTab(target, target);
        } else if (intent === "summarize") {
          // call summarize action
          const s = await axios.post("http://127.0.0.1:8080/action/summarize", { url: tabs.find(t => t.id === activeTab)?.url });
          alert("Summary:\n\n" + (s.data.summary || "No summary available"));
        } else {
          alert("Unknown intent: " + intent);
        }
        setHistory(h => [{ text, res: res.data.result, at: Date.now() }, ...h]);
      } else {
        alert("No response from agent.");
      }
    } catch (err) {
      alert("Error contacting AI agent: " + (err.message || err));
    }
  };

  const openTab = (url, title) => {
    const id = Math.max(...tabs.map(t => t.id)) + 1;
    const newTab = { id, title: title || url, url: url.startsWith("http") ? url : `https://${url}` };
    setTabs((t) => [...t, newTab]);
    setActiveTab(id);
  };

  const closeTab = (id) => {
    setTabs((t) => t.filter(x => x.id !== id));
    if (activeTab === id && tabs.length > 1) setActiveTab(tabs[0].id);
  };

  return (
    <div className="app">
      <header className="topbar">
        <div className="logo">MANVA</div>
        <CommandBar onSubmit={runIntent} />
        <div className="mode-toggle" title="Mode">⚙️</div>
      </header>

      <main className="main">
        <aside className="tabstrip" aria-label="Tabs">
          {tabs.map(t => (
            <div key={t.id} className={`tab ${t.id === activeTab ? "active" : ""}`}>
              <button onClick={() => setActiveTab(t.id)} className="tab-title">{t.title}</button>
              <button onClick={() => closeTab(t.id)} className="tab-close">✕</button>
            </div>
          ))}
        </aside>

        <section className="content">
          <div className="content-frame">
            <iframe
              title="active-content"
              src={tabs.find(t => t.id === activeTab)?.url || "about:blank"}
              sandbox="allow-same-origin allow-scripts allow-forms allow-popups"
            />
          </div>
        </section>
      </main>

      <footer className="statusbar">
        {history.slice(0,3).map((h, idx) => (
          <div key={idx} className="history-item">{h.text}</div>
        ))}
      </footer>
    </div>
  );
}
