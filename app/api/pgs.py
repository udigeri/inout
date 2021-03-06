import json
from .rest import Restful
from .transaction import Transaction

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

    def _getShopInfo(self):
        return getattr(self.config, "provider_TrustCommerce_shopInfo")

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

    def get_shopping_cart(self, trx):
        trx.shop = self._getShop()
        trx.shopInfo = self._getShopInfo()
        featureURL = "/paymentcart/{tenant}".format(tenant=self._getTenant())
        body = {"requestor": f"{trx.shop}", 
                # "id": "1",
                "correlationId": trx.correlationId,
                "amount": trx.amount,
                "currency": trx.currency,
                "reason": trx.reason,
                "reference": trx.reference,
                "successCallbackUrl": f"{self._getSuccessUrl()}",
                "failureCallbackUrl": f"{self._getFailureUrl()}",
                "customStyle": "style=\"color:red;\""
                }

        self.logger.debug(featureURL + " " + json.dumps(body))
        resp = self.put(self._url(featureURL), 
                        data=json.dumps(body), 
                        auth=self.auth)
        trx.rsp_status_code = resp.status_code
        trx.rsp_text = resp.text
        if trx.rsp_status_code == 401:
            self.logger.warn(f"StatusCode:{trx.rsp_status_code} {json.dumps(json.loads(trx.rsp_text))}")
        elif trx.rsp_status_code == 500:
            self.logger.error(f"StatusCode:{trx.rsp_status_code} {trx.rsp_text}")
        else:
            self.logger.debug(f"StatusCode:{trx.rsp_status_code} {json.dumps(json.loads(trx.rsp_text))}")
        return trx

    def get_payment_methods(self, trx):
        trx.costCentre = self._getCostCentre()
        featureURL = "/paymenttypes/{tenant}/{cart}/{correlationId}/{requestor}/{locale}?costCenter={costCentre}".format(
            tenant=self._getTenant(),
            cart=trx.shoppingCartUuid,
            correlationId=trx.correlationId,
            requestor=trx.shop,
            locale=self._getLocale(),
            costCentre=trx.costCentre,
            )

        self.logger.debug(featureURL)
        resp = self.get(self._url(featureURL), 
                        data=None, 
                        auth=self.auth)
        trx.rsp_status_code = resp.status_code
        trx.rsp_text = resp.text
        if trx.rsp_status_code == 401:
            self.logger.warn(f"StatusCode:{trx.rsp_status_code} {json.dumps(json.loads(trx.rsp_text))}")
        elif trx.rsp_status_code == 500:
            self.logger.error(f"StatusCode:{trx.rsp_status_code} {trx.rsp_text}")
        else:
            self.logger.debug(f"StatusCode:{trx.rsp_status_code}")
        return trx
