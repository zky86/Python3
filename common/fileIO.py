import requests
import utils
import json
import os
from requests_toolbelt.multipart import encoder
from minio import Minio
from minio.error import S3Error

data_res_type = {
    "image": 1,  # 图片
    "audio": 2,  # 音频
}

data_res_type = {
    "A_D01": 'A-D01',  # 世界灌溉工程遗产
    "A_E01": 'A-E01',  # 历史文化名城
}


# print(data_res_type)

class BaseUpload(object):
    # 服务器 nginx 访问前缀
    __prefix = 'http://172.16.20.213:9999'
    # 后台登录地址以及登录用户名和密码
    __login_url = f'{__prefix}/auth/oauth/token?randomStr=blockPuzzle&code=&grant_type=password'
    __user_name = 'admin'
    __password = 'cnb7v4Lz'
    __Authorization = None
    __Cookie = None

    # 单文件上传
    __single_upload_url = f'{__prefix}/dr/drattach/upload'

    # 文件夹上传
    __folder_create_url = f'{__prefix}/dr/drdatares/disPath'
    __folder_binding_url = f'{__prefix}/dr/drdatares/biandingFolder'

    # 获取文件信息
    __attaches_list_url = f'{__prefix}/dr/drdatares/getinfo'

    __is_logined = False

    def __init__(self):
        self.__logger = utils.get_logger()
        self.__minio = Minio(
            "172.16.20.28:9090",
            access_key="NGBR2B9R30BI0LWMN672",
            secret_key="eSURBjy8GI1oCdESQ4BfjqHO+3fgJ6whaLRhRptB",
            secure=False
        )

    def login(self):
        self.__logger.info("用户登录")
        self.__logger.debug("用户名:%s, 密码:%s", self.__user_name, self.__password)

        headers = {'Authorization': 'Basic cGlnOnBpZw=='}
        resp = requests.post(self.__login_url, headers=headers,
                             data={'username': self.__user_name, 'password': self.__password})
        if resp.status_code == requests.codes.ok:
            result = resp.json()
            self.__Authorization = f"Bearer {result['access_token']}"
            self.__Cookie = f"Authorization={result['access_token']}"
            self.__logger.info("登录成功, 获取到结果：%s", result)
        else:
            raise Exception(resp.reason)

        self.__is_logined = True

    def upload_callback(self, monitor):
        self.__logger.debug("%s%%", monitor.bytes_read * 100 // monitor.len)

    def single_file_upload(self, owner_id, owner_type, res_type, file_path):
        if not self.__is_logined:
            self.login()
        self.__logger.info("单文件上传: %s", file_path)
        self.__logger.info("owner_id: %s, owner_type: %s, res_type: %s, file_path: %s", owner_id, owner_type, res_type,
                            file_path)
        e = encoder.MultipartEncoder({
            'ownerId': owner_id,
            'ownerType': owner_type,
            'resType': res_type,
            'file': (os.path.basename(file_path), open(file_path, 'rb'))
        })

        m = encoder.MultipartEncoderMonitor(e, self.upload_callback)
        print(m)

        resp = requests.post(self.__single_upload_url, data=m,
                             headers={'Authorization': self.__Authorization, 'Cookie': self.__Cookie,
                                      'Content-Type': m.content_type})

        if not resp.status_code == requests.codes.ok:
            self.__logger.error(resp.text)
            raise Exception(resp.reason)

    def folder_uplad(self, owner_id, owner_type, res_type, folder_path):
        if not self.__is_logined:
            self.login()

        # 创建文件夹
        resp = requests.post(self.__folder_create_url,
                             json={
                                 'attachDir': '',
                                 'ownerId': owner_id,
                                 'ownerType': owner_type,
                                 'resType': res_type
                             },
                             headers={'Authorization': self.__Authorization, 'Cookie': self.__Cookie})
        if not resp.status_code == requests.codes.ok:
            self.__logger.error(resp.text)
            raise Exception(resp.reason)
        minio_folder = resp.json()['data']
        print(minio_folder)

        # 上传文件夹
        files_list = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                from_file_path = os.path.normpath(os.path.join(root, file))
                to_file_path = f"{'/'.join(os.path.split(os.path.relpath(from_file_path, start=folder_path)))}"
                to_file_path = to_file_path if to_file_path.startswith("/") else f'/{to_file_path}'
                files_list.append({
                    "from": from_file_path,
                    "to": f'{minio_folder}{to_file_path}'
                })
                # print(files_list)
        self.__logger.info("文件夹上传:%s, 共有 %s 文件, minio文件夹 %s", folder_path, len(files_list), minio_folder)

        try:
            for index, file in enumerate(files_list):
                self.__minio.fput_object("okdc-dev", file['to'], file['from'], num_parallel_uploads=20)
                # self.__logger.info("%s %s", index, file['from'])
        except S3Error as e:
            self.__logger.error(e)
            raise

        # 绑定文件信息
        resp = requests.post(self.__folder_binding_url,
                             json={
                                 'attachDir': minio_folder,
                                 'ownerId': owner_id,
                                 'ownerType': owner_type,
                                 'resType': res_type
                             },
                             headers={'Authorization': self.__Authorization, 'Cookie': self.__Cookie})
        if not resp.status_code == requests.codes.ok:
            self.__logger.error(resp.text)
            raise Exception(resp.reason)

if __name__ == '__main__':
    bu = BaseUpload()
    bu.single_file_upload("111111", "A-P01", "1",  r"D:\测试全媒体\全媒体资源平台交接技术文档.docx")
    # r = bu.fetch_attaches("111111", "A-P01")
    # bu.folder_uplad("111111", "A-E04", "4", r"D:\测试全媒体")
    # print(r)
