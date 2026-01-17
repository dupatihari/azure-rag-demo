import json
import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("GetCampaignInsights triggered")

    campaign_id = req.params.get("campaignId")
    if not campaign_id:
        return func.HttpResponse(
            json.dumps({"error": "campaignId is required"}),
            status_code=400,
            mimetype="application/json"
        )

    # Dummy response for now (replace with Foundry later)
    payload = {
        "campaignId": campaign_id,
        "summary": "Campaign performance is stable",
        "recommendations": [
            "Increase budget for high-performing channels",
            "Reduce spend on low-converting audiences"
        ]
    }

    return func.HttpResponse(
        json.dumps(payload),
        status_code=200,
        mimetype="application/json"
    )
