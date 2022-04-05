import requests
import json as complex_json

from common.logger import logger


class RestClient:

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.session()

    def get(self, uri, **kwargs):
        return self.request(uri, "GET", **kwargs)

    def post(self, uri, data=None, json=None, **kwargs):
        return self.request(uri, "POST", data, json, **kwargs)

    def put(self, uri, data=None, **kwargs):
        return self.request(uri, "PUT", data, **kwargs)

    def delete(self, uri, **kwargs):
        return self.request(uri, "DELETE", **kwargs)

    def patch(self, uri, data=None, **kwargs):
        return self.request(uri, "PATCH", data, **kwargs)

    def request(self, uri, method, data=None, json=None, **kwargs):
        request_url = self.base_url + uri
        headers = dict(**kwargs).get("headers")
        params = dict(**kwargs).get("params")
        files = dict(**kwargs).get("params")
        cookies = dict(**kwargs).get("params")
        self.request_log(request_url, method, data, json, params, headers, files, cookies)
        if method == "GET":
            return self.session.get(request_url, **kwargs)
        if method == "POST":
            return requests.post(request_url, data, json, **kwargs)
        if method == "PUT":
            if json:
                # PUT 和 PATCH 中没有提供直接使用 json 参数的方法，因此需要用 data 来传入
                data = complex_json.dumps(json)
            return self.session.put(request_url, data, **kwargs)
        if method == "DELETE":
            return self.session.delete(request_url, **kwargs)
        if method == "PATCH":
            if json:
                data = complex_json.dumps(json)
            return self.session.patch(request_url, data, **kwargs)

    @staticmethod
    def request_log(self, url, method, data=None, json=None, params=None, headers=None, files=None, cookies=None):
        logger.info("接口请求地址 ==>> {}".format(url))
        logger.info("接口请求方式 ==>> {}".format(method))
        # Python3中，json在做dumps操作时，会将中文转换成unicode编码，因此设置 ensure_ascii=False
        logger.info("接口请求头 ==>> {}".format(complex_json.dumps(headers, indent=4, ensure_ascii=False)))
        logger.info("接口请求 params 参数 ==>> {}".format(complex_json.dumps(params, indent=4, ensure_ascii=False)))
        logger.info("接口请求体 data 参数 ==>> {}".format(complex_json.dumps(data, indent=4, ensure_ascii=False)))
        logger.info("接口请求体 json 参数 ==>> {}".format(complex_json.dumps(json, indent=4, ensure_ascii=False)))
        logger.info("接口上传附件 files 参数 ==>> {}".format(files))
        logger.info("接口 cookies 参数 ==>> {}".format(complex_json.dumps(cookies, indent=4, ensure_ascii=False)))
