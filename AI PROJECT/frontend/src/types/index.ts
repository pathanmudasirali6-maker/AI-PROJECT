export interface ComparisonFeature {
  feature_name: string;
  option_a_detail: string;
  option_b_detail: string;
  winner?: string;
}

export interface DecisionOutcome {
  summary: string;
  comparison_table: ComparisonFeature[];
  confidence_score: number;
  sources_cited: string[];
  recommendation: string;
}
