def get_prompt(context):
    return f"""
    **Context:**

    - **Industry:** {context['industry']}
    - **Products/Services:** {context['products']}
    - **Location:** {context['location']}
    - **Data:** {context['data']}
    - **Timeframe:** {context['timeframe']}

    **Task:**

    Act as an expert demand forecaster and supply chain strategist for the given industry. Create a detailed stock/resource list for the business operating in the specified location within the defined timeframe, considering the constraints of available data.

    **Instructions:**

    1. **Stock/Resource List:**
    - Provide a detailed list with specific quantities for each primary category and its subcategories.
    - Include total numbers and breakdowns.
    - Also add the recommendation for other than Context stock/resource management strategy.

    2. **Festival/Seasonal/Event Analysis:**
    - Identify major festivals, seasons, or events within the timeframe.
    - Analyze their impact on demand for each category and explain which items/services surge and why.

    **Output Format:**

    - Use markdown with headings, bullet points, and tables.
    - Provide numerical data for all items.
    - Include a summary table of the final stock/resource list.
    """

def get_prompt_update(context, user_input):
    return f"""

**Context:**

    - **Industry:** {context['industry']}
    - **Products/Services:** {context['products']}
    - **Location:** {context['location']}
    - **Data:** {context['data']}
    - **Timeframe:** {context['timeframe']}

    **Task:**

    Act as an expert demand forecaster and supply chain strategist for the given industry. Update a detailed stock/resource list for the business operating in the specified location within the defined timeframe, considering the constraints of available data.

    **Instructions:**

    1. **Stock/Resource List:**
    - Provide a detailed list with specific quantities for each primary category and its subcategories.
    - Include total numbers and breakdowns.
    - Also add the recommendation for other than Context stock/resource management strategy.

    2. **Festival/Seasonal/Event Analysis:**
    - Identify major festivals, seasons, or events within the timeframe.
    - Analyze their impact on demand for each category and explain which items/services surge and why.

    **Output Format:**

    - Use markdown with headings, bullet points, and tables.
    - Provide numerical data for all items.
    - Include a summary table of the final stock/resource list.

    **Instructions:**

    Please modify only the following sections based on the new requirements:

    - {user_input}
    