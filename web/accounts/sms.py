import requests
import json


def send_sms(otp, mobile_number):
    url = "https://rest.payamak-panel.com/api/SendSMS/SendSMS"
    payload = json.dumps({
              "username": "ideveloper",
              "password": "18461336@Aa",
              "to": f"{mobile_number}",
              "from": "50004000474151",
              "text": f"{otp}",
              "isFlash": "0"
            })

    print(payload[0])
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    return print(response.text)


# send_sms("1253", "09388791325")