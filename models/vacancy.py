from typing import TypedDict


class Requirements(TypedDict):
    languages: str
    experience: str
    location: str


class Vacancy(TypedDict):
    name: str
    description: str
    requirements: Requirements


vacancies = {
    "frontEndDeveloper": {
        "name": "Front-end Developer",
        "description": "Vaga para programador frontend",
        "requirements": {
            "languages": "NodeJS, Vue, tailwindcss",
            "experience": "6 anos",
            "location": "Curitiba",
        },
    },
    "fullStackDeveloper": {
        "name": "Full-stack Developer",
        "description": "Vaga para programador fullstack",
        "requirements": {
            "languages": "PHP e Vue",
            "experience": "1 ano",
            "location": "Curitiba",
        },
    },
}
