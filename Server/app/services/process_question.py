from app.services.llm_service import send_data_to_server_LLM
from app.services.search_service import send_data_to_server_search
from app.models.prompts import system_prompt_keywords, system_prompt_search_q
from app.config import SERVER_MODEL_URL, SERVER_SEARCH_URL

def process_asking(question: str):
    keywords = send_data_to_server_LLM(SERVER_MODEL_URL, question, system_prompt_keywords)
    print(f" Keywords extracted: {keywords}")
    keywords_list = keywords.get("text", "").split(", ")
    if not keywords_list or keywords_list == [""]:
        return {"text":"No keywords were found that match your question."},keywords
    keywords_list.append(question)
    search_results = send_data_to_server_search(SERVER_SEARCH_URL, keywords_list)
    docs_text = "\n\n".join(
        [f"[{i+1}] Title:{r['title']} " for i, r in enumerate(search_results.get("results", []))]
    )
    system_prompt_search_q_filled = system_prompt_search_q.format(docs=docs_text)
    return send_data_to_server_LLM(SERVER_MODEL_URL, question, system_prompt_search_q_filled),keywords_list,search_results
