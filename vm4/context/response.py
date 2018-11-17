import json


class Response(object):

    def __init__(self, code, desc):
        if code is None:
            self.code = 0
        else:
            self.code = code
        if desc is None:
            self.desc = "success"
        else:
            self.desc = desc
        self.res = None

    def setRes(self, res):
        self.res = res


    def __str__(self):
        respDict = {'code': self.code, 'desc': self.desc, 'res': self.res}
        return json.dumps(respDict,ensure_ascii=False)