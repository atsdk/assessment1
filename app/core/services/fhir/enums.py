from enum import Enum


class AllergyIntoleranceCriticality(Enum):
    """Estimate of the potential clinical harm, or seriousness,
    of a reaction to an identified substance.
    """
    low = "Low Risk"
    high = "High Risk"
    unable_to_assess = "Unable to Assess"
