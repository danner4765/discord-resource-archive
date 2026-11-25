
import csv
import json
import argparse
from pathlib import Path
from urllib.parse import urlparse


DATA_DIRECTORY = Path(__file__).parent / "data"


SUBJECTS = {
    "A Level": {
        "mathematics": "Mathematics",
        "further_maths": "Further Mathematics",
        "physics": "Physics",
        "chemistry": "Chemistry",
        "biology": "Biology",
        "computer_science": "Computer Science"
    },

    "IGCSE": {
        "mathematics": "Mathematics",
        "additional_maths": "Additional Mathematics",
        "physics": "Physics",
        "chemistry": "Chemistry",
        "biology": "Biology",
        "computer_science": "Computer Science",
        "english": "English",
        "urdu": "Urdu",
        "pak_studies": "Pak Studies",
        "islamiat": "Islamiat"
    },

    "O Level": {
        "mathematics": "Mathematics",
        "additional_maths": "Additional Mathematics",
        "physics": "Physics",
        "chemistry": "Chemistry",
        "biology": "Biology",
        "computer_science": "Computer Science",
        "english": "English",
        "urdu": "Urdu",
        "pak_studies": "Pak Studies",
        "islamiat": "Islamiat"
    }
}


QUALIFICATION_FOLDERS = {
    "A Level": "a_level",
    "IGCSE": "igcse",
    "O Level": "o_level"
}


CATEGORIES = {
    "notes",
    "topicals",
    "youtubers",
    "textbooks"
}


def is_valid_url(url):

    if not url.startswith(("https://", "http://")):
        return False

    if any(character.isspace() for character in url):
        return False

    try:
        parsed = urlparse(url)
        hostname = parsed.hostname

        return (
            bool(parsed.netloc)
            and hostname is not None
            and "." in hostname
        )

    except ValueError:
        return False


def read_resources(csv_path):

    resources = []
    errors = []
    seen_resources = {}
    seen_urls = {}

    with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:

        reader = csv.DictReader(file)

        required_columns = {
            "Qualification",
            "Subject Key",
            "Subject",
            "Category",
            "Resource Name",
            "URL"
        }

        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError(
                "CSV is missing one or more required columns."
            )

        for row_number, row in enumerate(reader, start=2):

            qualification = (row["Qualification"] or "").strip()
            subject_key = (row["Subject Key"] or "").strip()
            subject_name = (row["Subject"] or "").strip()
            category = (row["Category"] or "").strip().lower()
            resource_name = (row["Resource Name"] or "").strip()
            url = (row["URL"] or "").strip()

            # Skip completely empty rows
            if not any([
                qualification,
                subject_key,
                subject_name,
                category,
                resource_name,
                url
            ]):
                continue

            # Validate qualification
            if qualification not in SUBJECTS:
                errors.append(
                    f"Row {row_number}: Invalid qualification."
                )
                continue

            # Validate subject key
            valid_subjects = SUBJECTS[qualification]

            if subject_key not in valid_subjects:
                errors.append(
                    f"Row {row_number}: Invalid subject key "
                    f"for {qualification}."
                )
                continue

            # Validate subject name
            if subject_name != valid_subjects[subject_key]:
                errors.append(
                    f"Row {row_number}: Subject name does not "
                    f"match subject key."
                )
                continue

            # Validate category
            if category not in CATEGORIES:
                errors.append(
                    f"Row {row_number}: Invalid category."
                )
                continue

            # Validate resource details
            if not resource_name or not url:
                errors.append(
                    f"Row {row_number}: Resource name or URL is missing."
                )
                continue

            # Validate URL format
            if not is_valid_url(url):
                errors.append(
                    f"Row {row_number}: Invalid URL: {url}"
                )
                continue

            location_key = (
                qualification,
                subject_key,
                category
            )

            duplicate_key = (
                *location_key,
                resource_name.casefold(),
                url.casefold()
            )

            url_key = (
                *location_key,
                url.casefold()
            )

            # Detect exact duplicates
            if duplicate_key in seen_resources:
                original_row = seen_resources[duplicate_key]

                errors.append(
                    f"Row {row_number}: Duplicate resource. "
                    f"It already appears in row {original_row}."
                )
                continue

            # Detect repeated URLs with different names
            if url_key in seen_urls:
                original_row = seen_urls[url_key]

                errors.append(
                    f"Row {row_number}: This URL is already used "
                    f"in row {original_row}."
                )
                continue

            seen_resources[duplicate_key] = row_number
            seen_urls[url_key] = row_number

            resources.append({
                "qualification": qualification,
                "subject_key": subject_key,
                "subject_name": subject_name,
                "category": category,
                "name": resource_name,
                "url": url
            })

    return resources, errors


def generate_json(resources):

    grouped = {}

    # Create an empty structure for every subject
    for qualification, subjects in SUBJECTS.items():

        folder = QUALIFICATION_FOLDERS[qualification]

        for subject_key, subject_name in subjects.items():

            grouped[(folder, subject_key)] = {
                "subject": subject_name,
                "categories": {
                    "topicals": [],
                    "notes": [],
                    "youtubers": [],
                    "textbooks": []
                }
            }

    # Organise resources
    for resource in resources:

        folder = QUALIFICATION_FOLDERS[
            resource["qualification"]
        ]

        subject_key = resource["subject_key"]
        category = resource["category"]

        grouped[(folder, subject_key)]["categories"][category].append({
            "name": resource["name"],
            "url": resource["url"]
        })

    # Write JSON files
    for (folder, subject_key), data in grouped.items():

        file_path = DATA_DIRECTORY / folder / f"{subject_key}.json"

        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

    print(f"Successfully generated {len(grouped)} JSON files.")


def show_preview(resources):

    print("\nDRY RUN — No files will be modified.\n")
    print("Validation successful!")
    print(f"\nTotal resources: {len(resources)}\n")

    for qualification in SUBJECTS:

        count = sum(
            1 for resource in resources
            if resource["qualification"] == qualification
        )

        print(f"{qualification}: {count}")

    print("\nAll checks passed.")
    print("No JSON files were changed.")


def main():

    parser = argparse.ArgumentParser(
        description="Convert the resource spreadsheet CSV into JSON files."
    )

    parser.add_argument(
        "csv_file",
        help="Path to the exported CSV file."
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and preview without modifying JSON files."
    )

    args = parser.parse_args()

    csv_path = Path(args.csv_file)

    if not csv_path.is_file():
        print(f"Error: CSV file not found: {csv_path}")
        return

    try:
        resources, errors = read_resources(csv_path)

    except (OSError, ValueError, UnicodeError) as error:
        print(f"Could not read CSV: {error}")
        return

    if errors:

        print("\nValidation failed:\n")

        for error in errors:
            print(f"- {error}")

        print("\nNo JSON files were changed.")
        return

    if not resources:
        print("No resources found in the CSV.")
        print("No JSON files were changed.")
        return

    if args.dry_run:
        show_preview(resources)
        return

    print(f"\nValidated {len(resources)} resources.")

    generate_json(resources)


if __name__ == "__main__":
    main()
