import pathlib
import pandas as pd
import json
from common.json_serializer import json_serializer
from common.config import Config
from common.hashers import get_md5_of_string
app_config = Config()
data_dir = pathlib.Path(app_config.BASE_DIR).joinpath(".data")
email_path = data_dir.joinpath("emails")

email_path.mkdir(exist_ok=True, parents=True)

emails_path = data_dir.joinpath("emails.csv")
emails = pd.read_csv(emails_path)


def clean_column_names(s: str):
    return s.strip().lower() \
        .replace(' ', '_') \
        .replace(':', '') \
        .replace('(', '') \
        .replace(')', '')


emails.columns = emails.columns.map(clean_column_names)

email_dict = emails.to_dict(orient='records')

for email in email_dict:
    subject = email.pop('subject')
    body = email.pop('body')
    email_id = get_md5_of_string(body)
    new_email = {
        "email_id": email_id
    }
    for k, v in email.items():
        new_email[k] = v

    new_email['subject'] = subject
    new_email['body'] = body

    email_path.joinpath(f"{email_id}.json").write_text(
        json.dumps(
            new_email,
            indent=4,
            default=json_serializer)
    )





