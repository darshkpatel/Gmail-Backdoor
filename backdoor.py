from __future__ import print_function
import httplib2
import os
import oauth2client
import base64
import email
import os
import webbrowser
import mimetypes
import time
from apiclient import discovery
from apiclient import errors


try:
    import argparse

except ImportError:
    flags = None

SCOPES = ["https://mail.google.com"]
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'
user_select = raw_input("Enter username: ")
user_select = str(user_select) + ".json"


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    credential_path = os.path.join(credential_dir,
                                   user_select)

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def DeleteMessage(service, user_id, msg_id):
  """Delete a Message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: ID of Message to delete.
  """
  try:
    service.users().messages().delete(userId=user_id, id=msg_id).execute()
    print ('Message with id: %s deleted successfully.' % msg_id)
  except errors.HttpError, error:
    print ('An error occurred: %s' % error)

def GetMimeMessage(service, user_id, msg_id):
  """Get a Message and use it to create a MIME Message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A MIME Message, consisting of data from Message.
  """
  try:
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    message = service.users().messages().get(userId=user_id, id=msg_id,
                                             format='full').execute()
    print (message)
    #print ('Message snippet: %s' % message['snippet'])
    
    #msg_str = base64.urlsafe_b64decode(message['payload']['parts'][1]["body"]["data"].encode('ASCII'))

    #print(msg_str)
    #mime_msg = email.message_from_string(msg_str)

    #print (mime_msg)
    #return mime_msg
  except errors.HttpError, error:
    print ('An error occurred: %s' % error)

def ListMessagesMatchingQuery(service, user_id, query=''):
  """List all Messages of the user's mailbox matching the query.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

  Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
  """
  try:
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    response = service.users().messages().list(userId=user_id,
                                               q=query,
                                               includeSpamTrash=True).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])
#Searches All Pages
    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query,
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])
    msg_count = 0
    for message in messages:
        #print(message['id'] + " - ")
        #GetMimeMessage('Gmail API Python Quickstart', 'me', message['id'])
        msg_count = msg_count + 1

    dec = raw_input(str(msg_count) + " messages found, Display them all ? [y/n] ")
    dec = str(dec)

    if dec=="y" or dec== "Y":
      for message in messages:
        GetMessage('Gmail API Python Quickstart','me',message['id'])
      main()


    elif dec == "n" or dec == "N":
      num_messages = input(" Enter Number Of messages to be displayed : ")
      num_messages = int(num_messages)
      msg_count = 0
      for message in messages:
        #print(message['id'] + " - ")
        GetMessage('Gmail API Python Quickstart','me',message['id'])
        
        #GetMimeMessage('Gmail API Python Quickstart', 'me', message['id'])
        # Print message snap
        if msg_count >= num_messages - 1 :
          print ("Done")
          
          break
          
        msg_count = msg_count + 1
      main()



    else:
      main()




    #return messages
  except errors.HttpError, error:
    print ('An error occurred: %s' % error)



def SendMessage(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print ('Message Id: %s' % message['id'])
    return message
  except errors.HttpError, error:
    print ('An error occurred: %s' % error)


def CreateMessage(sender, to, subject, message_text):
  """Create
   a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64 encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.b64encode(message.as_string())}




    
def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
  try:
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    print ('Id -' + str(message['id']) + ' \n'+'Time Stamp:' + str(message['internalDate']) + ' \n' + str(message['snippet']) + ' \n') 

    #return message
  except errors.HttpError, error:
    print ('An error occurred: %s' % error   )
    
def DeleteMessage(service, user_id, msg_id):
  """Delete a Message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: ID of Message to delete.
  """
  try:
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    service.users().messages().delete(userId=user_id, id=msg_id).execute()
    print ('Message with id: %s deleted successfully.' % msg_id)
  except errors.HttpError, error:
    print ('An error occurred: %s' % error)





def GetMimeMessage(service, user_id, msg_id):
  """Get a Message and use it to create a MIME Message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A MIME Message, consisting of data from Message.
  """
  try:
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    message = service.users().messages().get(userId=user_id, id=msg_id,
                                             format='full').execute()
    print (message['payload']['parts'])
    #print ('Message snippet: %s' % message['snippet'])
    
    msg_str = base64.urlsafe_b64decode(message['payload']['parts'][1]["body"]["data"].encode('ASCII'))

    #print(msg_str)
    mime_msg = email.message_from_string(msg_str)

    print (mime_msg)

    inp = raw_input("\n Display HTML in browser ? [y/n]")
    inp = str(inp)
    if inp == "y" or inp == "Y":
      html = str(mime_msg)
      print ("Opening Browser")
      path = os.path.abspath('temp.html')
      url = 'file://' + path
      with open(path, 'w') as f:
          f.write(html)
      webbrowser.open(url)
      time.sleep(3)
      main()
    else:
      main()



    
  except errors.HttpError, error:
    print ('An error occurred: %s' % error)




def SendMessage(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print ('Message Id: %s' % message['id'])
    return message
  except errors.HttpError, error:
    print ('An error occurred: %s' % error)


def CreateMessage(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64 encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.b64encode(message.as_string())}


def get_email():
  

  credentials = get_credentials()
  http = credentials.authorize(httplib2.Http())
  service = discovery.build('gmail', 'v1', http=http)

  user_info = None
  try:
    user_profile = service.users().getProfile(userId='me').execute()
    user_email = user_profile['emailAddress']
    return user_email
  except errors.HttpError, e:
    print("Error")

def multi_input(prompt):
  lines = []
  while True:
      line = raw_input()
      if line:
          lines.append(line)
      else:
          break
  text = '\n'.join(lines)
  text = str(text)
  return text

def main():
  print("Gmail API - Gmail Backdoor By Darsh \n")
  print(" 1) Search and List Emails \n 2) Delete Email \n 3) Read Email (ID Required) \n 4) Send Email  \n 0) Exit")
  print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
  choice = raw_input("Please Select a function: ")
  choice = int(choice)


#Using If .. elif ladder because python dosent have a switch case

  if choice == 1:
    #Choice 1
    search_string = raw_input("Enter Search String: ")
    search_string = str(search_string)
    ListMessagesMatchingQuery('Gmail API Python Quickstart','me',search_string)

  elif choice == 2:
    #choice 2
    msg_id= raw_input("Enter message id:  ")
    msg_id = str(msg_id)
    DeleteMessage('Gmail API Python Quickstart','me',msg_id)
  elif choice == 3:
    #choice 3
    msg_id=  raw_input("Enter message id:  ")
    msg_id = str(msg_id)
    GetMimeMessage('Gmail API Python Quickstart','me',msg_id)
    
  elif choice == 4:
    #choice 4
    #to_email= raw_input("Enter Enter E-Mail id to send email to:  ")
    #to_email = str(to_email)
    #subject_text = raw_input("Enter Subject Text: ")
    #subject_text = str(subject_text)
    #body_text = multi_input("Enter Text in email body : \n leave a blank line to exit to exit")
    #SendMessage('Gmail API Python Quickstart','me',CreateMessage(str(get_email()),to_email,subject_text, body_text))
    print("This Still needs a bit of tweaking")


  elif choice == 0:
    exit()

  else:
    "invalid Choice"
    time.sleep(2)


if __name__ == '__main__':
  main()

  
