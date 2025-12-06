export default function LoaderDots() {
  return (
    <div className="typing-loader">
      <style>{`
        .typing-loader {
          width: 60px;
          height: 20px;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .typing-loader div {
          width: 10px;
          height: 10px;
          background: var(--accent);
          border-radius: 50%;
          animation: blink 1.4s infinite both;
        }
        .typing-loader div:nth-child(2) {
          animation-delay: 0.2s;
        }
        .typing-loader div:nth-child(3) {
          animation-delay: 0.4s;
        }
        @keyframes blink {
          0% { opacity: .2; }
          20% { opacity: 1; }
          100% { opacity: .2; }
        }
      `}</style>
      <div></div><div></div><div></div>
    </div>
  );
}
