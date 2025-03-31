import os
from config.settings import settings
from helpers.format_phone_number import format_phone_number
from models.vacancy import vacancies
from services.file_service import load_or_create_workbook, move_files
from services.vacancy_service import evaluate_resume
from helpers.file_converter import extract_text_from_pdf
from services.whatsapp_service import (
    invite_whatsapp_url,
    approve_whatsapp_url,
    reject_whatsapp_url,
)


def main(vacancy_name: str):

    work_dir = os.path.join(settings.RESUME_PATH, vacancy_name)
    approval_path = os.path.join(work_dir, settings.APPROVED_PATH)
    rejection_path = os.path.join(work_dir, settings.REJECTED_PATH)
    excel_path = os.path.join(work_dir, f"./{vacancy_name}.xlsx")

    os.makedirs(approval_path, exist_ok=True)
    os.makedirs(rejection_path, exist_ok=True)

    wb, ws = load_or_create_workbook(excel_path)
    vacancy = vacancies[vacancy_name]

    for file_name in os.listdir(settings.RESUME_PATH):
        if file_name.endswith(".pdf"):
            pdf_file = os.path.join(settings.RESUME_PATH, file_name)

            try:
                resume = extract_text_from_pdf(pdf_file)
                result_data = evaluate_resume(resume, vacancy)

                phone_number = format_phone_number(result_data["contact"]["phone"])

                invite_message = invite_whatsapp_url(
                    vacancy["name"], result_data["contact"]["name"], phone_number
                )

                if result_data["result"].lower() == "aprovado":
                    message = approve_whatsapp_url(
                        vacancy["name"],
                        result_data["contact"]["name"],
                        phone_number,
                    )
                else:
                    invite_message = ""
                    message = reject_whatsapp_url(
                        vacancy["name"],
                        result_data["contact"]["name"],
                        phone_number,
                    )

                ws.append(
                    [
                        vacancy["name"],
                        result_data["contact"]["name"],
                        result_data["contact"]["email"],
                        phone_number,
                        "",
                        result_data["result"],
                        result_data["reason"],
                        invite_message,
                        message,
                    ]
                )

                wb.save(excel_path)

                move_files(file_name, result_data, approval_path, rejection_path)

            except Exception as e:
                print(f"Erro ao processar {file_name}: {e}")
                exit()

    print("Processamento finalizado. Planilha atualizada em:", excel_path)


if __name__ == "__main__":

    main("fullStackDeveloper")
