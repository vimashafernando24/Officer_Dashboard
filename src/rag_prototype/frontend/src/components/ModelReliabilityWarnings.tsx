import { EnglishOriginal } from "../i18n/LanguageControls";
import { useLocalizer } from "../i18n/languageContext";
import { translateMessage } from "../i18n/localize";
import type { AssignedProfile, ClusterCatalogueEntry } from "../types";

interface Props {
  assignedProfiles: AssignedProfile[];
  catalogue: ClusterCatalogueEntry[];
}

export function ModelReliabilityWarnings({ assignedProfiles, catalogue }: Props) {
  const localizer = useLocalizer();
  const warnings = assignedProfiles.filter((profile) => profile.needs_review_model);
  if (!warnings.length) return null;

  return (
    <div className="model-reliability-warnings" aria-label={localizer.t("reliability.groupLabel")}>
      {warnings.map((profile) => {
        const dimension = catalogue.find((entry) => entry.model_id === profile.model_id)?.dimension
          ?? profile.model_id.replace(/_/g, " ");
        // Same formatted figure in both languages; the English warning is kept
        // beside the Sinhala because it is the authoritative wording.
        const accuracy = (profile.model_published_accuracy * 100).toFixed(1);
        return (
          <section className="model-reliability-warning" role="alert" key={profile.model_id}>
            <div className="model-reliability-warning-heading">
              <strong>{localizer.t("reliability.heading", { dimension: localizer.modelLabel(profile.model_id, dimension) })}</strong>
              <span>{localizer.modelJudgment(profile.model_judgment)}</span>
            </div>
            <p>
              {localizer.t("reliability.body", { accuracy })}
              <EnglishOriginal text={translateMessage("en", "reliability.body", { accuracy })} />
            </p>
          </section>
        );
      })}
    </div>
  );
}
