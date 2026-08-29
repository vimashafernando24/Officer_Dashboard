type IconProps = { className?: string };

const base = {
  viewBox: "0 0 20 20",
  fill: "none" as const,
  stroke: "currentColor",
  strokeWidth: 1.6,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
};

export function UserIcon({ className }: IconProps) {
  return (
    <svg className={className} {...base} aria-hidden="true">
      <circle cx="10" cy="6.5" r="3.2" />
      <path d="M3.5 17c1-3.4 3.9-5.2 6.5-5.2s5.5 1.8 6.5 5.2" />
    </svg>
  );
}

export function BuildingIcon({ className }: IconProps) {
  return (
    <svg className={className} {...base} aria-hidden="true">
      <rect x="3.5" y="4" width="8" height="13" rx="1" />
      <path d="M11.5 8h5v9h-5" />
      <path d="M6 7.2h1.2M6 10h1.2M6 12.8h1.2" />
    </svg>
  );
}

export function TargetIcon({ className }: IconProps) {
  return (
    <svg className={className} {...base} aria-hidden="true">
      <circle cx="10" cy="10" r="6.5" />
      <circle cx="10" cy="10" r="3.2" />
      <circle cx="10" cy="10" r="0.6" fill="currentColor" stroke="none" />
    </svg>
  );
}

export function MessageIcon({ className }: IconProps) {
  return (
    <svg className={className} {...base} aria-hidden="true">
      <path d="M3.5 5.5h13v8.2H8.6L5 17v-3.3H3.5z" />
    </svg>
  );
}

export function CalendarIcon({ className }: IconProps) {
  return (
    <svg className={className} {...base} aria-hidden="true">
      <rect x="3.2" y="4.3" width="13.6" height="12" rx="1.4" />
      <path d="M3.2 8.2h13.6M6.6 2.8v3M13.4 2.8v3" />
    </svg>
  );
}

export function GlobeIcon({ className }: IconProps) {
  return (
    <svg className={className} {...base} aria-hidden="true">
      <circle cx="10" cy="10" r="6.8" />
      <path d="M3.2 10h13.6M10 3.2c2.4 2 2.4 11.6 0 13.6M10 3.2c-2.4 2-2.4 11.6 0 13.6" />
    </svg>
  );
}

export function FileIcon({ className }: IconProps) {
  return (
    <svg className={className} {...base} aria-hidden="true">
      <path d="M5.5 2.8h6l3 3v11.4h-9z" />
      <path d="M11.5 2.8v3h3M7.3 10h5.4M7.3 12.6h5.4" />
    </svg>
  );
}

export function LightbulbIcon({ className }: IconProps) {
  return (
    <svg className={className} {...base} aria-hidden="true">
      <path d="M6.3 8.5a3.7 3.7 0 1 1 7.4 0c0 1.7-1 2.4-1.6 3.3-.5.7-.6 1.2-.6 1.9H8.5c0-.7-.1-1.2-.6-1.9-.6-.9-1.6-1.6-1.6-3.3z" />
      <path d="M8.4 16.2h3.2M8.9 17.7h2.2" />
    </svg>
  );
}

export function PeopleIcon({ className }: IconProps) {
  return (
    <svg className={className} {...base} aria-hidden="true">
      <circle cx="7" cy="6.8" r="2.6" />
      <circle cx="14" cy="7.8" r="2.1" />
      <path d="M2.5 17c.8-3.1 2.7-4.6 4.5-4.6s3.7 1.5 4.5 4.6M12 12.9c1.9-.4 3.9.9 4.6 3.6" />
    </svg>
  );
}

export function BookIcon({ className }: IconProps) {
  return (
    <svg className={className} {...base} aria-hidden="true">
      <path d="M10 5.2c-1.3-1-3.4-1.4-6-1.4v10.8c2.6 0 4.7.4 6 1.4 1.3-1 3.4-1.4 6-1.4V3.8c-2.6 0-4.7.4-6 1.4z" />
      <path d="M10 5.2v10.8" />
    </svg>
  );
}

export function ShieldIcon({ className }: IconProps) {
  return (
    <svg className={className} {...base} aria-hidden="true">
      <path d="M10 2.5l6 2.2v4.7c0 4-2.6 6.7-6 8.1-3.4-1.4-6-4.1-6-8.1V4.7z" />
      <path d="M7.3 9.8l1.9 1.9 3.5-3.9" />
    </svg>
  );
}

export function ChevronDownIcon({ className }: IconProps) {
  return (
    <svg className={className} {...base} aria-hidden="true">
      <path d="M4.5 7.2l5.5 5.6 5.5-5.6" />
    </svg>
  );
}

export function ArrowLeftIcon({ className }: IconProps) {
  return (
    <svg className={className} {...base} aria-hidden="true">
      <path d="M12.5 4.3L6.2 10l6.3 5.7M6.5 10h11" />
    </svg>
  );
}

export function CheckIcon({ className }: IconProps) {
  return (
    <svg className={className} {...base} aria-hidden="true">
      <path d="M4 10.3l3.8 3.8 8.2-8.7" />
    </svg>
  );
}

export function ClockIcon({ className }: IconProps) {
  return (
    <svg className={className} {...base} aria-hidden="true">
      <circle cx="10" cy="10.3" r="6.8" />
      <path d="M10 6.4v4.1l2.9 1.8" />
    </svg>
  );
}

export function HelpCircleIcon({ className }: IconProps) {
  return (
    <svg className={className} {...base} aria-hidden="true">
      <circle cx="10" cy="10" r="6.8" />
      <path d="M7.7 7.9a2.3 2.3 0 1 1 3.5 2c-.8.6-1.2 1-1.2 1.9" />
      <circle cx="10" cy="14.4" r="0.5" fill="currentColor" stroke="none" />
    </svg>
  );
}

export function LeafIcon({ className }: IconProps) {
  return (
    <svg className={className} {...base} aria-hidden="true">
      <path d="M4 16c-.6-6.6 3.6-11.4 11.8-11.8.6 7.7-3.8 11.6-11.8 11.8z" />
      <path d="M4.6 15.4c2.6-3.4 5.6-5.8 9.9-8.6" />
    </svg>
  );
}
