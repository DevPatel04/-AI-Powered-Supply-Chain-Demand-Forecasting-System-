def get_prompt(context):
    """This function returns prompt for user's first input"""
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
    Forecast demand and create a detailed stock list for the business operating in the specified location within the defined timeframe, considering all the festivals during that time, weather conditions, and social trends.

    **Instructions:**
    1. **Stock/Resource List:**
    - Provide a detailed list with specific quantities for each primary category and its subcategories.
    - Include total numbers and breakdowns.

    2. **Festival/Seasonal/Event Analysis:**
    - Identify major festivals, seasons, or events within the timeframe.
    - Analyze their impact on demand for each category and explain which items/services surge and why.

    3. **Transportation and Delivery Time:**
    - Give each mode of transportation with expected delivery time.
    - Identify the best mode of transportation, considering cost and time.

    4. Also add the recommendation for other than Context stock/resource management strategy.

    **Output Format:**
    - Use markdown with headings, bullet points, and tables.
    - Provide numerical data for all items.
    - Include a summary table of the final stock list.
    """


def get_prompt_update(context, user_input):
    """This function returns prompt for user's second time input."""
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
    - {{ {user_input} }}
    """


def get_prompt_with_old_data(context):
    """This function returns prompt when user upload previous sales data file"""
    return f"""
    **Context:**
    - **Industry:** {context['industry']}
    - **Last Products/Service Sales Report Data:** {context['old_data']}
    - **Location:** {context['location']}
    - **Data:** {context['data']}
    - **Timeframe:** {context['timeframe']}
    - **Type of Business:** {context['type_of_business']}
    - **Size of Business:** {context['size_of_business']}

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