import requests
import json
from .rest import Restful

class Pgs(Restful):
    def __init__(self, config):
        self.config = config

    def _url(self, path):
        return self._getBaseUrl() + path

    def _getShop(self):
        return getattr(self.config, "provider_TrustCommerce_shop")

    def _getBaseUrl(self):
        return getattr(self.config, "provider_TrustCommerce_baseURL")

    def _getSuccessUrl(self):
        return getattr(self.config, "provider_TrustCommerce_successURL")

    def _getFailureUrl(self):
        return getattr(self.config, "provider_TrustCommerce_failureURL")

    def get_shopping_cart(self, pp, lpn, amount):
        body = {"requestor": f"{self._getShop()}", 
                "id": "1",
                "correlationId": "0123456789",
                "amount": f"{amount}",
                "currency": "EUR",
                "reason": f"Parking {lpn}",
                "reference": f"{pp}",
                "successCallbackUrl": f"{self._getSuccessUrl()}",
                "failureCallbackUrl": f"{self._getFailureUrl()}",
                "customStyle": "style=\"color:red;\"",
                }
        return self.get(self._url("/posts/"), data=json.dumps(body))
        #return self.get(self._url("/paymentcart/"))
