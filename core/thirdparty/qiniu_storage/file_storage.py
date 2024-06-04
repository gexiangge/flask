# @Time    : 2020-11-06 16:16
# @Author  : 老赵
# @File    : file_storage.py
import logging

from qiniu import Auth, put_file, etag, urlsafe_base64_encode, put_data

# 需要填写你的 Access Key 和 Secret Key
access_key = 'IGwLUvXx5BKXjW9pZwpyQVTvuDMIpxibqjCezh0q'
secret_key = '9Ttq77KTl-9DHUWMxRIxG_TjBeIBMQU6YtTa8i58'

# 要上传的空间
bucket_name = 'cili-avatar'


def image_storage(image_data):
    # 上传图片

    if not image_data:
        return None

    try:
        # 构建鉴权对象
        q = Auth(access_key, secret_key)

        # 生成上传 Token，空间名称,名字不传由七牛云维护, 可以指定过期时间等
        token = q.upload_token(bucket_name)

        # 上传文件
        ret, info = put_data(token, None, image_data)

    except Exception as e:
        logging.error(e)
        raise e

    # 判断图片是否有上传成功
    if info and info.status_code != 200:
        raise Exception("上传文件到七牛失败")

    # 返回七牛中保存的图片名，这个图片名也是访问七牛获取图片的路径
    return ret["key"]


if __name__ == '__main__':
    with open('gpu.png', 'rb') as f:
        print(image_storage(f.read()))
    url_prefix = 'http://qipjg3ur6.hb-bkt.clouddn.com/'
