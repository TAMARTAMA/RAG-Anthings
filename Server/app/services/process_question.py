import torch
from app.services.llm_service import send_data_to_server_LLM
from app.services.search_service import send_data_to_server_search
from app.models.prompts import system_prompt_keywords, system_prompt_search_q
from app.config import SERVER_MODEL_URL
from sentence_transformers import CrossEncoder

reranker_model = CrossEncoder(
    "jinaai/jina-reranker-v2-base-multilingual",
    trust_remote_code=True,
    device="cuda:0" )

def process_asking(question: str ,index_name:str):
    keywords = send_data_to_server_LLM(SERVER_MODEL_URL, question, system_prompt_keywords)
    print(f" Keywords extracted: {keywords}")
    keywords_list = keywords.get("text", "").split(", ")
    if not keywords_list or keywords_list == [""]:
        return {"text":"No keywords were found that match your question."},keywords,[]
    keywords_list.append(question)
    search_results = send_data_to_server_search(keywords_list,index_name)
    results = search_results.get("results", [])
    for r in results:
        passages = r['text'].split('.')
        with torch.no_grad():  
            ranks = reranker_model.rank(question, passages)
        txts = []
        for rank in ranks[:3]:
            txts.append(passages[rank['corpus_id']])
        r['text'] = ".".join(txts) 

    docs_text = "\n\n".join(
    [
        f"[{i+1}] Title: {r.get('title', 'No Title')}\nText: {r.get('text', '')}"
        for i, r in enumerate(search_results.get("results", []))
    ]
    )
    print(docs_text)
    system_prompt_search_q_filled = system_prompt_search_q.format(docs=docs_text)
    print("_____________________________________")
    answer = send_data_to_server_LLM(SERVER_MODEL_URL, question, system_prompt_search_q_filled)
    torch.cuda.empty_cache()
    return answer,keywords_list,search_results
