from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from atlas import Atlas
app=FastAPI(title="Atlas")
@app.get('/',response_class=HTMLResponse)
async def home(): return Path('static/index.html').read_text()
atlas=Atlas()
class Project(BaseModel): name:str
class Alias(BaseModel): value:str
@app.get('/healthz')
async def healthz(): return {'ok':True,'service':'atlas'}
@app.post('/demo/setup')
async def setup():
 try: await atlas.ingest_fixture(); return {'ok':True}
 except Exception as e: raise HTTPException(502,str(e))
@app.post('/answer/project')
async def answer(q:Project):
 try: return await atlas.resolve(q.name)
 except Exception as e: raise HTTPException(502,str(e))
@app.post('/answer/alias')
async def alias(q:Alias):
 try: return await atlas.aliases(q.value)
 except Exception as e: raise HTTPException(502,str(e))
