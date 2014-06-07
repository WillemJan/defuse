import fuse, os, Image
from stat import S_IRUSR, S_IXUSR, S_IWUSR, S_IRGRP, S_IXGRP, S_IXOTH, S_IROTH

from fs import FS, BaseMetadata
import StringIO

PATH_TO_ORG_IMAGES = '/usr/share/doc//python-pygame/tut/surfarray/'
img_list = os.listdir(PATH_TO_ORG_IMAGES)

fs = FS.get()

@fs.route('/')
class Root(object):
    def __init__(self):
        root_mode = S_IRUSR|S_IXUSR|S_IWUSR|S_IRGRP|S_IXGRP|S_IXOTH|S_IROTH
        self.dir_metadata = BaseMetadata(root_mode, True)

    def getattr(self, *args, **kwargs):
        return self.dir_metadata

    def readdir(self, *args, **kwargs):
        for f in img_list:
            yield fuse.Direntry(f)

@fs.route('/<filepath>')
class Files(object):
    def __init__(self):
        file_mode = S_IRUSR|S_IWUSR|S_IRGRP|S_IROTH
        self.file_metadata = BaseMetadata(file_mode, False)

    def getattr(self, *args, **kwargs):
        filepath = kwargs['filepath']
        isize = 100,100
        im = Image.open(PATH_TO_ORG_IMAGES + filepath)
        im.thumbnail(isize, Image.ANTIALIAS)
        output = StringIO.StringIO()
        im.save(output, 'JPEG')
        data = output.getvalue()
        output.close()
        self.file_metadata.st_size = len(data*4)
        return self.file_metadata

    def read(self, size, offset, *args, **kwargs):
        filepath = kwargs['filepath']
        isize =  100,100
        im = Image.open(PATH_TO_ORG_IMAGES + filepath)
        im.thumbnail(isize, Image.ANTIALIAS)
        output = StringIO.StringIO()
        im.save(output, 'JPEG')
        data = output.getvalue()
        output.close()
        return data[offset:size+offset]
