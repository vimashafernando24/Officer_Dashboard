import "./ChoiceGrid.css";
import type { Option } from "../types";

export function ChoiceGrid({
  name,
  options,
  value,
  onChange,
  optionImages,
  tiles,
}: {
  name: string;
  options: Option[];
  value: string | null;
  onChange: (code: string) => void;
  optionImages?: Record<string, string>;
  tiles?: boolean;
}) {
  return (
    <div
      className={`choice-grid${tiles ? " choice-grid-tiles" : ""}`}
      role="radiogroup"
      aria-label={name}
    >
      {options.map((o) => (
        <label
          key={o.code}
          className={`choice-option${value === o.code ? " selected" : ""}`}
        >
          <input
            type="radio"
            name={name}
            checked={value === o.code}
            onChange={() => onChange(o.code)}
          />
          {optionImages?.[o.code] && (
            <img className="choice-mascot" src={optionImages[o.code]} alt="" aria-hidden="true" />
          )}
          <span className="choice-label">{o.label}</span>
        </label>
      ))}
    </div>
  );
}

export function MultiChoiceGrid({
  name,
  options,
  value,
  onChange,
  maxSelected,
  exclusiveOptionCodes = [],
}: {
  name: string;
  options: Option[];
  value: string[];
  onChange: (values: string[]) => void;
  maxSelected?: number;
  exclusiveOptionCodes?: string[];
}) {
  const selected = new Set(value);
  const exclusiveOptions = new Set(exclusiveOptionCodes);
  const selectedNonExclusive = value.filter((code) => !exclusiveOptions.has(code));
  const atLimit = maxSelected !== undefined && selectedNonExclusive.length >= maxSelected;
  return (
    <div className="choice-grid" role="group" aria-label={name}>
      {options.map((option) => {
        const checked = selected.has(option.code);
        const isExclusive = exclusiveOptions.has(option.code);
        const disabled = !checked && atLimit && !isExclusive;
        return (
          <label
            key={option.code}
            className={`choice-option${checked ? " selected" : ""}${disabled ? " is-disabled" : ""}`}
          >
            <input
              type="checkbox"
              name={name}
              checked={checked}
              disabled={disabled}
              onChange={() => {
                if (checked) {
                  onChange(value.filter((code) => code !== option.code));
                } else if (isExclusive) {
                  onChange([option.code]);
                } else {
                  onChange([
                    ...value.filter((code) => !exclusiveOptions.has(code)),
                    option.code,
                  ]);
                }
              }}
            />
            <span className="choice-label">{option.label}</span>
          </label>
        );
      })}
      {maxSelected !== undefined ? (
        <div className="choice-limit" aria-live="polite">
          {value.length} of {maxSelected} selected
        </div>
      ) : null}
    </div>
  );
}
