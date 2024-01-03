# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure
account_sid = "ACaa9720195b1101f4f741a8336d53886a"
auth_token = "61c285feca64120fd87869311fd19c1a"
client = Client(account_sid, auth_token)

message = client.messages.create(
  body="Hello augustus",
  from_="+16515656402",
  to="+918593948358"
  
)

print(message.sid)