from openai import OpenAI

# Instantiate the OpenAI client

# Define the prompt
messages = [
    {"role": "system", "content": "You are an assistant that generates valid target groups and categories for events."},
    {"role": "user", "content": """
    The following event has missing information. Please suggest appropriate target groups and categories based on the event details:
    
    Title: Startup Workshop
    Summary: Learn the basics of starting a business.
    Description: This workshop covers business planning, funding, and networking.
    
    Only use the following valid values:
    - Target Groups: CORPORATES, FOUNDERS, FOUNDERS_TO_BE, INNOVATION_HUBS, INVESTORS, MENTORS, PUBLIC_INSTITUTIONS, SMALL_AND_MEDIUM_BUSINESSES, STUDENTS
    - Categories: COFOUNDER_MATCHING, CONFERENCE, DEMO_DAY, FUNDRAISING, JOB_FAIR, NETWORKING, PITCH, WORKSHOP_LEARNING
    
    Provide a JSON object with two fields:
    - target_groups: a list of valid target groups
    - categories: a list of valid categories
    """}
]

# Call the OpenAI API
response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    max_tokens=300
)

# Print the response content
print(response.choices[0].message.content)