def generate_insights(results):

    importance = results["importance"]

    top_attribute = importance.idxmax()
    top_value = round(importance.max(), 2)

    insight = f"""
    The most influential attribute is **{top_attribute}**
    contributing approximately **{top_value}%**
    to customer decision-making.

    Recommendation:
    Focus product optimization and marketing
    messaging around this attribute to maximize preference.
    """

    return insight