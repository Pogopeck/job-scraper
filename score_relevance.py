import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

prompt = ChatPromptTemplate.from_template(
    """You are an expert DevOps and GenAI hiring assistant.
    Score how well the following job matches a candidate with:
    - 5+ years in DevOps (AWS, Terraform, Kubernetes)
    - Experience building GenAI tools using LangChain, RAG, and LLMs
    - Strong Python and cloud automation skills

    Job Title: {title}
    Job Description: {description}

    Respond ONLY with a number from 1 to 10 (1 = irrelevant, 10 = perfect fit).
    """
)

def score_job(job):
    try:
        chain = prompt | llm
        response = chain.invoke({
            "title": job["title"],
            "description": job["description"]
        })
        score_text = response.content.strip()
        # Extract number
        score = int(re.search(r'\d+', score_text).group())
        return min(max(score, 1), 10)
    except Exception as e:
        print(f"Scoring error: {e}")
        return 0
