import json
from .rest import Restful

class Pgs(Restful):
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.auth = None 

    def _url(self, path):
        return self._getHost() + self._getBaseUrl() + path

    def setAuth(self, auth):
        self.auth = auth

    def _getShop(self):
        return getattr(self.config, "provider_TrustCommerce_shop")

    def _getLocale(self):
        return getattr(self.config, "provider_TrustCommerce_locale")

    def _getCostCentre(self):
        return getattr(self.config, "provider_TrustCommerce_costCentre")

    def _getHost(self):
        return getattr(self.config, "provider_TrustCommerce_host")

    def _getBaseUrl(self):
        return getattr(self.config, "provider_TrustCommerce_baseURL")

    def _getSuccessUrl(self):
        return getattr(self.config, "provider_TrustCommerce_successURL")

    def _getFailureUrl(self):
        return getattr(self.config, "provider_TrustCommerce_failureURL")

    def _getTenant(self):
        return getattr(self.config, "provider_TrustCommerce_tenant")

    def get_shopping_cart(self, pp, lpn, amount):
        featureURL = "/paymentcart/{tenant}".format(tenant=self._getTenant())
        body = {"requestor": f"{self._getShop()}", 
                # "id": "1",
                "correlationId": "0123456789",
                "amount": f"{amount}",
                "currency": "EUR",
                "reason": f"Parking fee {lpn}",
                "reference": f"{pp}",
                "successCallbackUrl": f"{self._getSuccessUrl()}",
                "failureCallbackUrl": f"{self._getFailureUrl()}",
                "customStyle": "style=\"color:red;\""
                }

        self.logger.debug(featureURL + " " + json.dumps(body))
        resp = self.put(self._url(featureURL), 
                        data=json.dumps(body), 
                        auth=self.auth)
        if resp.status_code == 401:
            self.logger.warn(f"StatusCode:{resp.status_code} {json.dumps(json.loads(resp.text))}")
        else:
            self.logger.debug(f"StatusCode:{resp.status_code} {json.dumps(json.loads(resp.text))}")
        return resp

    def get_payment_methods(self, cart):
        featureURL = "/paymenttypes/{tenant}/{cart}/{correlationId}/{requestor}/{locale}?costCenter={costCentre}".format(
            tenant=self._getTenant(),
            cart=cart,
            correlationId="0123456789",
            requestor=self._getShop(),
            locale=self._getLocale(),
            costCentre=self._getCostCentre(),
            )

        self.logger.debug(featureURL)
        resp = self.get(self._url(featureURL), 
                        data=None, 
                        auth=self.auth)
        if resp.status_code == 401:
            self.logger.warn(f"StatusCode:{resp.status_code} {json.dumps(json.loads(resp.text))}")
        else:
            self.logger.debug(f"StatusCode:{resp.status_code}")
        return resp
