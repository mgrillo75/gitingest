from utils.clone import clone_repo, delete_repo
from ingest import ingest_from_query


async def process_query(query: dict) -> tuple:
    try:
        await clone_repo(query)
        result = ingest_from_query(query)
        txt_dump = result[1] + "\n" + result[2]
        
        with open(f"{query['local_path']}.txt", "w", encoding='utf-8') as f:
            f.write(txt_dump)
            
        return result
    finally:
        # Always try to clean up, even if there was an error
        try:
            delete_repo(query['local_path'])
        except:
            pass
