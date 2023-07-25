from fastapi import FastAPI

from fast_zero.routes import main_router

app = FastAPI(
    title='fast_zero', version='0.1.0', description='API de gestão de tarefas.'
)
app.include_router(main_router)


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}
