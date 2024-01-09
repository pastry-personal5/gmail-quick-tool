"""
This moudle renames Gmail labels according to defined find-and-replace patterns.
The source code is based on a Gmail Python quickstart provided by Google. For details, visit
https://developers.google.com/gmail/api/quickstart/python?hl=en
"""
import copy
import os.path
import pprint
import re
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.labels"]


def do_login(renew_token):
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if not renew_token:
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w", encoding="utf-8") as token:
      token.write(creds.to_json())
  return creds


def convert_month_string_to_month_number_string(abbr_month):
  abbr_months_array = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
  for i in range(0, 12):
    if abbr_month == abbr_months_array[i]:
      return f"{i + 1:02}"
  return None


def build_new_label_name(prefix, location, abbr_month, year):
  month = convert_month_string_to_month_number_string(abbr_month)
  if not month:
    print("[ERROR] Abbreviated month string is not found: ", abbr_month)
    return None
  new_label_name = f"{prefix}{year}-{month}-{location}"
  return new_label_name


def get_new_label_if_possible(old_label):
  """
  It returns a new label; None, if it fails.
  The argument `label` is a dict like below:
  {'color': {'backgroundColor': '#ac2b16', 'textColor': '#f6c5be'},
   'id': 'Label_866226624395716597',
   'labelListVisibility': 'labelShow',
   'messageListVisibility': 'show',
   'name': '지난여행/43. SFO-DEC-1959',
   'type': 'user'}
  """
  pattern = re.compile('(지난여행/[0-9]+. )([^-]+)-([^-]+)-([0-9]+)')
  result = pattern.match(old_label["name"])
  if not result:
    return None
  new_label = copy.deepcopy(old_label)
  new_label_name = build_new_label_name(result.group(1), result.group(2), result.group(3), result.group(4))
  if new_label_name:
    new_label["name"] = new_label_name
    return new_label
  return None


def print_rename_info(new_label):
  pprint.pprint(new_label)
  sys.stdout.flush()


def rename_label_using_google_api(service, new_label):
  service.users().labels().update(userId="me", id=new_label["id"], body=new_label).execute()


def rename_labels(creds):
  """It renames Gmail labels according to defined find-and-replace patterns.
  """

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])

    if not labels:
      print("[ERROR] No labels found.")
      return
    for label in labels:
      print(f"[INFO] Processing {label['name']}...")
      sys.stdout.flush()
      new_label = get_new_label_if_possible(label)
      if new_label:
        print_rename_info(new_label)
        rename_label_using_google_api(service, new_label)

  except HttpError as error:
    print(f"[ERROR] An error occurred: {error}")


def main():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """

  creds = do_login(renew_token=False)
  rename_labels(creds)


if __name__ == "__main__":
  main()
