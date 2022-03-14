from eventbrite import Eventbrite
import json



def main():
  token = authToken('eventbrite')
  evb = Eventbrite(token)
  


def authToken(service):
  token_data = None
  with open('token.json','r') as file: token_data = json.load(file)
  return token_data[service]

if __name__ == '__main__':
  main()