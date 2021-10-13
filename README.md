# pyDecryptCookies
This script decrypts encryted cookies from `Cookie` file, with using `Local State` file and DPAPI. 

Works for Chrome-like browsers (Chrome, Chromium, Edge, ...).

## Install
This script has to be exeucted **on the same machine, that browser runs on** (because of usage of DPAPI).

Python install:
```bash
$ python3 -m venv venv-profile
$ source venv-profile/bin/activate
$ pip install -r requirements.txt
```

## Usage
- example usage for Edge with saving output to file:
```bash
$ python .\decrypt-cookie.py -c "C:\Users\USER\AppData\Local\Microsoft\Edge\User Data\Default\Cookies" -l "C:\Users\USER\AppData\Local\Microsoft\Edge\User Data\Local State" -o "output.csv"
- decrytion starts
- decrytion is complete, total number of decrypted cookies: 21
- output successfully saved to: output.csv
```
- example usage for Chrome without saving output to file:
```bash
PS C:\Users\PA51NA\Onedrive - NN\desktop\Tools\py-decrypt-chrome-cookies> python .\decrypt-cookie.py -c "C:\Users\USER\AppData\Local\Google\Chrome\User Data\Default\Cookies" -l "C:\Users\USER\AppData\Local\Google\Chrome\User Data\Local State"
- decrytion starts
- cookie SignInStateCookie (for site .login.microsoftonline.com):
CAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXfaQ

- cookie Signature (for site euno-1.api.microsoftstream.com):
XXXXXXXXXXXXXXXXE%253d

- cookie Signature_Api (for site .api.microsoftstream.com):
ADXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX53d

- decrytion is complete, total number of decrypted cookies: 3
```

## Thanks
Core functionality is inspired by [topaco](https://stackoverflow.com/users/9014097/topaco) and his [post on StackOverflow](https://stackoverflow.com/questions/60416350/chrome-80-how-to-decode-cookies). Thanks! ;)
