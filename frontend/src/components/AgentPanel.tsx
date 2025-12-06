import { useState } from "react";
import ReactMarkdown from "react-markdown";

export default function AgentPanel({
  title,
  content,
}: {
  title: string;
  content: string;
}) {
  const [open, setOpen] = useState(true);

  return (
    <div
      style={{
        background: "var(--bg-card)",
        marginBottom: "16px",
        borderRadius: "16px",
        padding: "16px",
        border: "1px solid var(--border-glass)",
        backdropFilter: "var(--glass-blur)",
        boxShadow: "0 4px 20px rgba(0,0,0,0.4)",
        transition: "0.2s",
      }}
    >
      <div
        onClick={() => setOpen(!open)}
        style={{
          cursor: "pointer",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontSize: "18px",
          fontWeight: "600",
          color: "var(--accent)",
        }}
      >
        {title}
        <span>{open ? "▼" : "▲"}</span>
      </div>

      {open && (
        <div style={{ marginTop: "12px", color: "var(--text-secondary)" }}>
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}
