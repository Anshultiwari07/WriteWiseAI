import { useState } from "react";

export default function InputBar({ onSend }: { onSend: (msg: string) => void }) {
  const [text, setText] = useState("");

  const send = () => {
    if (!text.trim()) return;
    onSend(text.trim());
    setText("");
  };

  return (
    <div
      style={{
        padding: "16px",
        background: "rgba(0,0,0,0.5)",
        backdropFilter: "blur(10px)",
        display: "flex",
        gap: "12px",
        borderTop: "1px solid var(--border-glass)",
      }}
    >
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && send()}
        placeholder="Create,Write anything..."
        style={{
          flexGrow: 1,
          padding: "14px",
          borderRadius: "12px",
          border: "1px solid var(--border-glass)",
          background: "var(--bg-card)",
          color: "var(--text-primary)",
          fontSize: "16px",
        }}
      />

      <button
        onClick={send}
        style={{
          background: "var(--accent)",
          border: "none",
          padding: "0 22px",
          borderRadius: "12px",
          cursor: "pointer",
          color: "#000",
          fontWeight: "600",
          transition: "0.2s",
          boxShadow: "0 0 12px var(--accent-glow)",
        }}
      >
        Send
      </button>
    </div>
  );
}
