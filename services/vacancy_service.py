import re
import json
import google.generativeai as genai
from config.settings import settings
from models.vacancy import Vacancy

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


def generate_prompt(resume: str, vacancy: Vacancy) -> str:
    requirements = "\n".join(
        f"- {key}: {value}" for key, value in vacancy["requirements"].items()
    )

    return f"""
    Você é um avaliador especializado em triagem de currículos. Analise cuidadosamente o currículo e a vaga abaixo.

    **Vaga**:
    Nome: {vacancy['name']}
    Descrição: {vacancy['description']}
    Requisitos:
    {requirements}

    **Currículo do candidato**:
    {resume}

    ## Sua tarefa:

    ### Parte 1: Avaliação
    - Verifique estritamente se o candidato atende a **todos os requisitos obrigatórios/eliminatórios** descritos na vaga.
    - Se o candidato NÃO atender a qualquer requisito obrigatório, ele deve ser automaticamente **Reprovado**.
    - Justifique detalhadamente o motivo da aprovação ou reprovação, mencionando explicitamente cada requisito e se foi atendido ou não.
    - Não assuma ou interprete informações vagas ou implícitas no currículo como válidas. Só considere informações que estão claramente especificadas.

    ### Parte 2: Extração de Dados
    Extraia do currículo, se disponível:
    - Nome completo
    - E-mail
    - Telefone

    ## Formato de resposta:

    Responda **somente** no seguinte formato JSON, sem nenhum texto ou explicação fora dele:

    {{
        "result": "Aprovado ou Reprovado",
        "reason": "Motivo detalhado, mencionando cada requisito e se foi atendido ou não",
        "contact": {{
            "name": "Nome do candidato ou 'Não encontrado'",
            "email": "Email do candidato ou 'Não encontrado'",
            "phone": "Telefone do candidato ou 'Não encontrado'"
        }}
    }}
    """


def evaluate_resume(resume: str, vacancy: Vacancy) -> dict:
    try:
        prompt = generate_prompt(resume, vacancy)
        response = model.generate_content(prompt)

        match = re.search(r"\{.*\}", response.text, re.DOTALL)
        if not match:
            raise ValueError("Nenhum JSON encontrado na resposta")

        json_text = match.group(0)
        return json.loads(json_text)

    except Exception as e:
        print(f"Erro ao avaliar currículo: {e}")
        raise
