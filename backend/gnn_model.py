import torch
import torch.nn.functional as F
from torch_geometric.nn import GATv2Conv, global_mean_pool

class SupplyChainGATv2(torch.nn.Module):
    def __init__(self, num_node_features: int, hidden_channels: int):
        super().__init__()
        
        self.conv1 = GATv2Conv(num_node_features, hidden_channels, heads=4, concat=True, dropout=0.6)
        self.conv2 = GATv2Conv(hidden_channels * 4, hidden_channels, heads=1, concat=False, dropout=0.6)
        
        
        self.classifier = torch.nn.Linear(hidden_channels, 2)

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor, batch: torch.Tensor) -> torch.Tensor:
        x = F.dropout(x, p=0.6, training=self.training)
        x = self.conv1(x, edge_index)
        x = F.elu(x)
        
        x = F.dropout(x, p=0.6, training=self.training)
        x = self.conv2(x, edge_index)
        x = F.elu(x)
        
        x = global_mean_pool(x, batch)
        
        return self.classifier(x)