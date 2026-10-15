import type { AssignedProfile, ClusterCatalogueEntry } from "../types";

interface Props {
  assignedProfiles: AssignedProfile[];
  catalogue: ClusterCatalogueEntry[];
}

export function ModelReliabilityWarnings({ assignedProfiles, catalogue }: Props) {
  const warnings = assignedProfiles.filter((profile) => profile.needs_review_model);
  if (!warnings.length) return null;

  return (
    <div className="model-reliability-warnings" aria-label="Model reliability warnings">
      {warnings.map((profile) => {
        const dimension = catalogue.find((entry) => entry.model_id === profile.model_id)?.dimension
          ?? profile.model_id.replace(/_/g, " ");
        return (
          <section className="model-reliability-warning" role="alert" key={profile.model_id}>
            <div className="model-reliability-warning-heading">
              <strong>{dimension} model</strong>
              <span>{profile.model_judgment}</span>
            </div>
            <p>
              This model did not meet the predefined reliability thresholds for assigning new members
              ({(profile.model_published_accuracy * 100).toFixed(1)}% validation accuracy). Treat this
              cluster assignment as provisional and review it alongside the member’s own answers.
            </p>
          </section>
        );
      })}
    </div>
  );
}
