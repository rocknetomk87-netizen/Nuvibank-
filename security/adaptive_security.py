def requires_extra_verification(risk_score):

    if risk_score >= 70:
        return True

    return False
