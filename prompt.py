def get_prompt(context):
    return f"""
    **Context:**
    - **Industry:** {context['industry']}
    - **Products/Services:** {context['products']}
    - **Location:** {context['location']}
    - **Data:** {context['data']}
    - **Timeframe:** {context['timeframe']}
    - **Type of Business:** {context['type_of_business']}
    - **Size of Business:** {context['size_of_business']}

    **Task:**
    You are an expert demand forecaster and supply chain strategist for the given industry. 
    Forecast demand and create a detailed stock list for the business operating in the specified location within the defined timeframe, considering the all the festivals during that time, weather condition and social trend.

    **Instructions:**
    1. **Stock/Resource List:**
    - Provide a detailed list with specific quantities for each primary category and its subcategories.
    - Include total numbers and breakdowns.

    2. **Festival/Seasonal/Event Analysis:**
    - Identify major festivals, seasons, or events within the timeframe.
    - Analyze their impact on demand for each category and explain which items/services surge and why.

    3. **Transportation and delivery time:**
    - Give each mode of transportation with expected delivery time.
    - Identify best mode of transportation, considering cost and time.

    4. Also add the recommendation for other than Context stock/resource management strategy.

    **Output Format:**
    - Use markdown with headings, bullet points, and tables.
    - Provide numerical data for all items.
    - Include a summary table of the final stock list.
    """

    # **Avoid**
    # - If user ask about out of knowledge, then do not give response.

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
    """


def get_prompt_with_old_data(context):
        return f"""
    **Context:**

    - **Industry:** {context['industry']}
    - **last Products/Service sales report data :** {context['old_data']}
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