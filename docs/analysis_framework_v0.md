This section outlines the planned analysis axes for interpreting model behavior on formal–informal intent-matched pairs.  
The framework is intended as an analysis plan rather than finalized results, and will be iteratively refined as more model outputs are collected.

### A1. Formal vs Informal Performance Gap
**Question**  
Does model performance degrade when the input is informal compared to its formal counterpart?

**Planned metrics / checks**  
- Pair-level performance difference between formal and informal variants  
- Proportion of intent pairs where the informal variant underperforms the formal variant  
- Qualitative differences in response completeness or specificity

### A2. Sensitivity to Linguistic Phenomena
**Question**  
Which types of linguistic variation (e.g., typos, abbreviations, informal lexicon, dialect words) are most likely to degrade model performance?

**Planned metrics / checks**  
- Performance grouped by phenomenon category  
- Error rates conditioned on specific phenomena types  
- Comparison of error patterns across phenomena

### A3. Error Pattern Distribution
**Question**  
Do certain error types (as defined in the error taxonomy) occur more frequently under informal or non-standard inputs?

**Planned metrics / checks**  
- Distribution of error labels (E1–E10) for formal vs informal inputs  
- Relative increase of specific error types under informal variants

> Note: This analysis framework represents a top-down plan for interpreting results and will be updated based on empirical observations from model outputs.
