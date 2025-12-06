import { useEffect, useState } from "react";
import "./index.css";

type Role = "user" | "assistant";

interface Message {
  id: number;
  role: Role;
  content: string;
}

interface Conversation {
  id: string;
  title: string;
  messages: Message[];
}

export default function App() {
  const [theme, setTheme] = useState<"dark" | "light">("dark");
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeId, setActiveId] = useState<string | null>(null);
  const [input, setInput] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // apply theme to <html> so CSS can switch
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  const activeConversation =
    conversations.find((c) => c.id === activeId) ?? null;

  // helper to append a message to a conversation list
  const appendMessage = (
    convId: string,
    message: Message,
    convs: Conversation[]
  ) =>
    convs.map((c) =>
      c.id === convId
        ? { ...c, messages: [...c.messages, message] }
        : c
    );

  const handleSend = async () => {
    const text = input.trim();
    if (!text || isLoading) return;

    setIsLoading(true);

    let convId = activeId;
    let updatedConvs = conversations;

    // create a new conversation if none is active
    if (!convId) {
      convId = String(Date.now());
      const newConv: Conversation = {
        id: convId,
        title: text.slice(0, 50) || "New draft",
        messages: [],
      };
      updatedConvs = [newConv, ...conversations];
    }

    // add user message locally
    const userMsg: Message = {
      id: Date.now(),
      role: "user",
      content: text,
    };

    updatedConvs = appendMessage(convId, userMsg, updatedConvs);
    setConversations(updatedConvs);
    setActiveId(convId);
    setInput("");

    try {
      // ✅ payload that matches your GenerateRequest schema
      const payload = {
        topic: text,
        format_type: "blog_article", // must be one of backend enum values
        length: "medium",            // 'short' | 'medium' | 'long'
        num_pieces: 1,
        language: "English",
      };

      const resp = await fetch("http://127.0.0.1:8000/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(apiKey ? { "X-API-Key": apiKey } : {}),
        },
        body: JSON.stringify(payload),
      });

      if (!resp.ok) {
        const errText = await resp.text();
        throw new Error(`Backend error ${resp.status}: ${errText}`);
      }

      const data = await resp.json();

      // assuming GenerateResponse has "output"
      const assistantContent =
        data.output ?? data.result ?? JSON.stringify(data);

      const aiMsg: Message = {
        id: Date.now() + 1,
        role: "assistant",
        content: assistantContent,
      };

      setConversations((prev) => appendMessage(convId!, aiMsg, prev));
    } catch (err: any) {
      const errorMsg: Message = {
        id: Date.now() + 2,
        role: "assistant",
        content:
          "⚠️ There was a problem talking to the backend:\n" +
          (err?.message || String(err)),
      };
      setConversations((prev) => appendMessage(convId!, errorMsg, prev));
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    setActiveId(null);
    setInput("");
  };

  const handleClearHistory = () => {
    setConversations([]);
    setActiveId(null);
    setInput("");
  };

  const handleSelectConversation = (id: string) => {
    setActiveId(id);
  };

  const toggleTheme = () => {
    setTheme((t) => (t === "dark" ? "light" : "dark"));
  };

  return (
    <div className="ww-app">
      {/* Sidebar */}
      <aside className="ww-sidebar">
        <div className="ww-sidebar-header">
          <h1 className="ww-app-title">WriteWiseAI</h1>
          <p className="ww-app-subtitle">
            An open content writing Multi-Agentic AI
          </p>
        </div>

        <button className="ww-sidebar-button primary" onClick={handleNewChat}>
          + New
        </button>

        <button
          className="ww-sidebar-button subtle"
          onClick={handleClearHistory}
        >
          🗑 Clear history
        </button>

        <div className="ww-sidebar-section">
          <div className="ww-sidebar-section-title">DRAFT HISTORY</div>
          <div className="ww-sidebar-list">
            {conversations.length === 0 && (
              <div className="ww-sidebar-empty">No drafts yet.</div>
            )}
            {conversations.map((conv) => (
              <button
                key={conv.id}
                className={
                  "ww-sidebar-item" +
                  (conv.id === activeId ? " ww-sidebar-item-active" : "")
                }
                onClick={() => handleSelectConversation(conv.id)}
              >
                {conv.title}
              </button>
            ))}
          </div>
        </div>

        <div className="ww-sidebar-footer">
          <label className="ww-api-label">API Key (optional)</label>
          <input
            className="ww-api-input"
            placeholder="Paste key here..."
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
          />
        </div>
      </aside>

      {/* Main area */}
      <main className="ww-main">
        <header className="ww-main-header">
          <h2 className="ww-main-title">Create, write anything</h2>
          <button className="ww-theme-toggle" onClick={toggleTheme}>
            {theme === "dark" ? "☀️ Light" : "🌙 Dark"}
          </button>
        </header>

        <section className="ww-chat-shell">
          {activeConversation && activeConversation.messages.length > 0 ? (
            <div className="ww-messages">
              {activeConversation.messages.map((m) => {
                const isUser = m.role === "user";
                return (
                  <div
                    key={m.id}
                    className={
                      "ww-message-row " +
                      (isUser
                        ? "ww-message-row-user"
                        : "ww-message-row-assistant")
                    }
                  >
                    {/* AI avatar on left */}
                    {!isUser && (
                      <div className="ww-avatar ww-avatar-ai">AI</div>
                    )}

                    {/* Message bubble */}
                    <div
                      className={
                        "ww-message " +
                        (isUser
                          ? "ww-message-user"
                          : "ww-message-assistant")
                      }
                    >
                      <div className="ww-message-content">{m.content}</div>
                    </div>

                    {/* User avatar on right */}
                    {isUser && (
                      <div className="ww-avatar ww-avatar-user">You</div>
                    )}
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="ww-empty-state">
              Start by telling WriteWiseAI what you want to create: blog,
              LinkedIn post, script, email…
            </div>
          )}
        </section>

        <footer className="ww-input-bar">
          <input
            className="ww-input"
            placeholder="Create, write anything..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
          />
          <button
            className="ww-send-button"
            onClick={handleSend}
            disabled={isLoading}
          >
            {isLoading ? "Thinking..." : "Send"}
          </button>
        </footer>
      </main>
    </div>
  );
}
