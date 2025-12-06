import ReactMarkdown from "react-markdown";

export default function ChatWindow({ messages }: { messages: any[] }) {
  return (
    <div
      style={{
        flexGrow: 1,
        overflowY: "auto",
        padding: "24px",
      }}
    >
      {messages.map((msg, i) => (
        <div key={i} style={{ marginBottom: "20px" }}>
          <div
            style={{
              background: msg.role === "user" ? "var(--accent)" : "var(--bg-card)",
              padding: "14px",
              borderRadius: "16px",
              maxWidth: "80%",
              color: msg.role === "user" ? "#000" : "var(--text-primary)",
              boxShadow:
                msg.role === "user"
                  ? "0 0 14px var(--accent-glow)"
                  : "0 0 12px rgba(255,255,255,0.05)",
            }}
          >
            <ReactMarkdown>{msg.text}</ReactMarkdown>
          </div>
        </div>
      ))}
    </div>
  );
}
