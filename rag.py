from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
    StorageContext,
    load_index_from_storage,
)
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
import logging
import sys
import os.path
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import FunctionCallingAgentWorker

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
Settings.llm = Ollama(model="mistral", request_timeout=360.0)


PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    print("Creating index")
    documents = SimpleDirectoryReader(input_files=["Medicine_Details.csv"]).load_data()
    print(f"Loaded {len(documents)} documents")
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
    chat_engine = index.as_chat_engine(chat_mode="context", verbose=True)
    chat_engine.chat_repl()

#     query_engine_tool = QueryEngineTool(
#     query_engine=query_engine.as_query_engine(similarity_top_k=3),
#     metadata=ToolMetadata(
#         name="Medicine Details",
#         description=(
#             "Provides information about medicines and their uses and side effects."
#         ),
#     ),
# )
#     agent_worker = FunctionCallingAgentWorker.from_tools(
#     [query_engine_tool], verbose=True
# )
# agent = agent_worker.as_agent()

