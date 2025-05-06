from langchain_tavily import TavilySearch

tool = TavilySearch(
    max_results=5,
    topic="general",
    # include_answer=False,
    # include_raw_content=False,
    # include_images=False,
    # include_image_descriptions=False,
    # search_depth="basic",
    # time_range="day",
    include_domains=["https://libretexts.org", "https://openstax.org/"],
    # exclude_domains=None
)

print(tool.invoke({"query": "What is thermodynamics"}))