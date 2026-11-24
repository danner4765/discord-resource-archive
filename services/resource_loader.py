import json
from pathlib import Path


DATA_DIRECTORY = Path(__file__).parent.parent / "data"


def load_subject(qualification, subject):

    file_path = (
        DATA_DIRECTORY
        / qualification
        / f"{subject}.json"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_category(qualification, subject, category):

    data = load_subject(qualification, subject)

    return data["categories"].get(category, [])
