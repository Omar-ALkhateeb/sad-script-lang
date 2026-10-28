# lang/stdlib/http.py
"""HTTP/Network Standard Library (`استورد طلبات`)."""

import json as _py_json
import urllib.request as _urllib_req
from ..types import RuntimeError, String, wrap


class Response:
    """Represents an HTTP response."""

    __type_name__ = "استجابة"

    def __init__(self, status: int, text: str):
        self.الحالة = status
        self.النص = String(text)

    def كقاموس(self):
        try:
            return wrap(_py_json.loads(self.النص))
        except Exception:
            raise RuntimeError("محتوى الاستجابة ليس بتنسيق JSON صالح للتحويل إلى قاموس.")

    def __repr__(self) -> str:
        return f"<استجابة الحالة={self.الحالة}>"


class HttpModule:
    __type_name__ = "مكتبة"

    @staticmethod
    def احصل(الرابط: str) -> Response:
        url_str = str(الرابط).strip()
        try:
            try:
                from pyodide.http import open_url
                text = open_url(url_str).read()
                return Response(200, text)
            except ImportError:
                req = _urllib_req.Request(url_str, headers={"User-Agent": "SadScript/1.0"})
                with _urllib_req.urlopen(req, timeout=10) as resp:
                    return Response(resp.status, resp.read().decode("utf-8"))
        except Exception:
            raise RuntimeError(
                f"تعذر الاتصال بالرابط '{url_str}'. تأكد من صحة الرابط ومن اتصالك بالإنترنت."
            )

    @staticmethod
    def جلب(الرابط: str):
        return HttpModule.احصل(الرابط).كقاموس()

    @staticmethod
    def جلب_بيانات(الرابط: str):
        return HttpModule.جلب(الرابط)