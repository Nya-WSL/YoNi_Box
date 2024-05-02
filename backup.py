import os
from qiniu import Auth, put_file, etag

#需要填写你的 Access Key 和 Secret Key
access_key = 'Access_Key'
secret_key = 'Secret_Key'

#构建鉴权对象
q = Auth(access_key, secret_key)

#要上传的空间
bucket_name = 'Your_Bucket_Name'

#上传后保存的文件名
key = 'YoNi/AskBox/yoni_box.db'

#生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)

#要上传文件的本地路径
localfile = 'yoni_box.db'

ret, info = put_file(token, key, localfile, version='v1') 
print(info)
assert ret['key'] == key
assert ret['hash'] == etag(localfile)

os.system('cp -r yoni_box.db yoni_box.db.bak')