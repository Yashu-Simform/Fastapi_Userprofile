import requests

def main():
    res = requests.post('http://127.0.0.1:8000/user/reset-password', data={'email': 'yashuranparia@gmail.com', 'password': 'Yashu@13', 'confirm_password': 'Yashu@13'}, params={'callback_url': 'http://127.0.0.1:8000/user/dummy-callback-url'})

    print(res.status_code)
    print(res.json())

main()