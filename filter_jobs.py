def matches_keywords(job):
    title = job.get("title", "").lower()
    desc = job.get("description", "").lower()
    
    devops_terms = ["devops", "cloud engineer", "platform engineer"]
    genai_terms = ["genai", "llm", "langchain", "ai", "artificial intelligence", "large language model"]
    
    has_devops = any(term in title for term in devops_terms)
    has_genai = any(term in desc or term in title for term in genai_terms)
    
    return has_devops and has_genai
