from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from pinecone import Pinecone, ServerlessSpec
from utils.DLAIUtils import Utils
from sentence_transformers import SentenceTransformer

# Initialize the app
app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Add CORS middleware (optional, if you want to allow cross-origin requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to a specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize utilities and model
Utils = Utils()
pinecone_api_key = Utils.get_pinecone_api_key()
pinecone = Pinecone(api_key=pinecone_api_key)

model = SentenceTransformer('all-MiniLM-L6-v2')

#INDEX_NAME = Utils.create_dlai_index_name(pinecone, 'quora-index')
index = pinecone.Index('quora-index')
print(f"index status: {index.describe_index_stats()}")

@app.get("/", response_class=HTMLResponse)
async def read_root(request:Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process", response_class=HTMLResponse)
async def process_input(request:Request, user_input:str = Form(...)):
    #processed_data = f'You have entered: {user_input}'
    query_vector = model.encode(user_input).tolist()
    #print(query_vector[:5])
    # query pinecone
    results = index.query(vector=query_vector,top_k=2, include_metadata=True, include_vector=False)
    processed_data = '<br>'.join([f"{result['score']}: {result['metadata']['text']}" for result in results['matches']])
    return templates.TemplateResponse("result.html", {"request": request, "result": processed_data})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    