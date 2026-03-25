import json

# Load data once
with open("mcp_server/data.json") as f:
    DATA = json.load(f)


def get_disease_info(disease: str):
    disease = disease.lower()
    if disease in DATA:
        return DATA[disease]["info"]
    return {"error": "Disease not found"}


def get_disease_remedy(disease: str):
    disease = disease.lower()
    if disease in DATA:
        return DATA[disease]["remedy"]
    return {"error": "Disease not found"}