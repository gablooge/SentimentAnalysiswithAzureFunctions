from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential

class RecognizeReceiptsFromURLSample(object):

    def recognize_receipts_from_url(self):
        # This is your client - a one entry point to working with the resource
        form_recognizer_client = FormRecognizerClient(
            endpoint = "https://receiptformanalyzer.cognitiveservices.azure.com/",
            credential=AzureKeyCredential("KEY_CREDENTIAL")
        )

        # This is the receipt we will be recognizing - you can swap it with any other receipt url
        url = "https://raw.githubusercontent.com/Azure/azure-sdk-for-python/master/sdk/formrecognizer/azure-ai-formrecognizer/tests/sample_forms/receipt/contoso-receipt.png"

        # Here we start the recognition and poll to see if we have results available
        poller = form_recognizer_client.begin_recognize_receipts_from_url(receipt_url=url)
        receipts = poller.result()

        # We know we sent only one receipt so we get the first (and only) item in the list of returned results
        recognized_receipt = receipts[0].fields

        # Let's see what we recognized
        print("Receipt Type: {}".format(recognized_receipt.get("ReceiptType").value))
        print("Merchant Name: {}".format(recognized_receipt.get("MerchantName").value))
        print("Transaction Date: {}".format(recognized_receipt.get("TransactionDate").value))
        print("Receipt items:")
        for idx, item in enumerate(recognized_receipt.get("Items").value):
            print("...Item #{}".format(idx+1))
            item_name = item.value.get("Name")
            if item_name:
                print("......Item Name: {} has confidence: {}".format(item_name.value, item_name.confidence))
            item_quantity = item.value.get("Quantity")
            if item_quantity:
                print("......Item Quantity: {} has confidence: {}".format(item_quantity.value, item_quantity.confidence))
            item_price = item.value.get("Price")
            if item_price:
                print("......Individual Item Price: {} has confidence: {}".format(item_price.value, item_price.confidence))
            item_total_price = item.value.get("TotalPrice")
            if item_total_price:
                print("......Total Item Price: {} has confidence: {}".format(item_total_price.value, item_total_price.confidence))
        print("Subtotal: {}".format(recognized_receipt.get("Subtotal").value))
        print("Tax: {}".format(recognized_receipt.get("Tax").value))
        print("Total: {}".format(recognized_receipt.get("Total").value))
        print("--------------------------------------")

if __name__ == '__main__':
    sample = RecognizeReceiptsFromURLSample()
    sample.recognize_receipts_from_url()
