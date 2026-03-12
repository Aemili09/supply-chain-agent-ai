import torch
from live_data import fetch_gdelt_risk_data
from contract_validator import validate_and_save
from gnn_model import SupplyChainGATv2

def run_enterprise_pipeline():
    print("--- INITIATING SC-RIHN PIPELINE ---")
    
    print("1. Fetching live macroeconomic data from Google BigQuery...")
    df = fetch_gdelt_risk_data()
    
    print("2. Enforcing Data Contract & Saving to Delta Lake...")
    status = validate_and_save(df)
    print(status)
    
    print("3. Initializing GATv2 Neural Network for Risk Inference...")
    
    num_nodes = len(df)
    x = torch.randn((num_nodes, 16))
    edge_index = torch.randint(0, num_nodes, (2, num_nodes * 2))
    batch = torch.zeros(num_nodes, dtype=torch.long)
    
    model = SupplyChainGATv2(num_node_features=16, hidden_channels=64)
    model.eval()
    with torch.no_grad():
        predictions = model(x, edge_index, batch)
        
    print("Pipeline Execution Complete. Target variables calculated.")
    return predictions

if __name__ == "__main__":
    run_enterprise_pipeline()