from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model.rag_chain import rag_chain
from fastapi.middleware.cors import CORSMiddleware


class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    context: list

app = FastAPI()

# Set CORS policy
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        results = rag_chain.invoke({"input": request.query})
        return QueryResponse(answer=results["answer"], context=[doc.page_content for doc in results["context"]])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
