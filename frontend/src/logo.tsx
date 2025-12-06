export default function Logo({ size = 32 }: { size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <linearGradient id="wwai" x1="0" y1="0" x2="100" y2="100">
          <stop offset="0%" stopColor="#ff7a3d" />
          <stop offset="100%" stopColor="#ff955f" />
        </linearGradient>
      </defs>
      <circle cx="50" cy="50" r="46" stroke="url(#wwai)" strokeWidth="6" />
      <path
        d="M28 35 L45 65 L60 50 L75 70"
        stroke="url(#wwai)"
        strokeWidth="6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
