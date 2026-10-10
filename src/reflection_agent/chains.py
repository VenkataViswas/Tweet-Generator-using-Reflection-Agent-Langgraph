"""
This file implements a tweet generation and reflection system using LangChain and Google Gemini. It defines two prompt chains: a generation chain that creates engaging Twitter posts and a reflection chain that critiques tweets and provides recommendations to improve their length, style, clarity, and virality.

The prompts use ChatPromptTemplate and MessagesPlaceholder to manage system instructions and conversation messages. Both chains are connected to the Gemini model using LangChain Expression Language (LCEL) with the prompt | model syntax.

When executed, the script invokes the generation chain with a sample question and prints the generated tweet.

Key concepts: Prompt templates, message placeholders, LLM integration, LCEL, and reflection-based content improvement.
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

reflection_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a viral Twitter influencer grading a tweet. "
        "Generate critique and recommendations for the user's tweet. "
        "Always provide detailed recommendations, including length, "
        "virality, and style."
    ),
    MessagesPlaceholder(variable_name="messages"),
])

generation_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a Twitter tech influencer assistant tasked with writing "
        "excellent Twitter posts. Generate the best Twitter post possible. "
        "If the user provides critique, revise your previous attempt."
    ),
    MessagesPlaceholder(variable_name="messages"),
])

model = ChatGoogleGenerativeAI(model="gemini-3.7-flash")

generation_chain = generation_prompt | model
reflection_chain = reflection_prompt | model

# for testing this file does not require for final graph state running 

if __name__ == "__main__":
    response = generation_chain.invoke({
        "messages": [
            ("human", "Is LangChain better than ever as a framework?")
        ]
    })

    print(response.content)