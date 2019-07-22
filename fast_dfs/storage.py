from fdfs_client.client import Fdfs_client
from django.core.files.storage import Storage
from ljq_blogs import settings


#定义储存文件的类
class FastDfs(Storage):
    def _open(self, name, mode='rb'):
        print("hello")
        pass

    def _save(self, name, content):
        print("hello")
        #name 是你选择上传文件的名字
        # content 一个文件对象
        # 下面的执行的是  向FastDFS发送一个连接请求 返回一个storage(包括storage的ip 和id)
        client = Fdfs_client("./fast_dfs/client.conf")
        # 在上面_open 中我们固定参数传值为'rb' 读取文件buffer 所以在上传文件的时候使用下面这个方法
        res = client.upload_appender_by_buffer(content.read())
        #返回一个字典格式如下
        '''
        @return dict {
            'Group name'      : group_name,
            'Remote file_id'  : remote_file_id,文件上传成功之后返回的文件的ID
            'Status'          : 'Upload successed.',
            'Local file name' : '',
            'Uploaded size'   : upload_size, 文件的大小
            'Storage IP'      : storage_ip 储存文件storage 服务器的ip地址
        } if success else None
        '''
        if res.get('Status') == 'Upload successed.':
            filename = res.get("Remote file_id")
            return filename
        else:
            raise Exception("上传文件失败")

        def exists(self, name):
            #判断文件是不是存在
            return False

        def url(self, name):
            #返回图片的储存路径地址
            print(name)
            return settings.FDFS_SERVER_URL + name
