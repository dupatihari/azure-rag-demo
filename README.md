# Azure RAG Demo

A Retrieval-Augmented Generation (RAG) demo application that provides campaign insights using Azure AI services.  The project includes an Azure Function backend, a React frontend, and an MCP (Model Context Protocol) server for integration with AI assistants.

## 🏗️ Architecture

This demo consists of three main components:

1. **Azure Function** (`GetCampaignInsights/`) - Backend RAG service
2. **React Client** (`client/`) - Frontend web interface
3. **MCP Server** (`mcp-campaign-insights/`) - Integration layer for AI assistants

### Data Flow

```
User Query → Azure Function → Azure AI Search → Azure AI Foundry → JSON Response
                                ↓
                        Campaign Documents
```

## 🚀 Features

- **RAG-Powered Insights**: Combines Azure AI Search with Azure AI Foundry (OpenAI models)
- **Campaign Analysis**: Query marketing campaign data and receive structured insights
- **MCP Integration**: Expose insights via Model Context Protocol for AI assistant integration
- **React Frontend**: Modern UI for querying campaign data
- **Containerized Deployment**: Docker support for MCP server

## 📋 Prerequisites

- Azure subscription with: 
  - Azure Functions
  - Azure AI Search
  - Azure AI Foundry (or OpenAI)
  - Azure Container Apps (for MCP server)
- Python 3.11+
- Node.js 18+ (for React client)
- Docker (for MCP server deployment)

## 🛠️ Setup

### 1. Azure Resources

Use the provided Jupyter notebook to set up Azure resources:

```bash
jupyter notebook AzureResources.ipynb
```

### 2. Azure Function Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment variables
export AZURE_SEARCH_ENDPOINT="https://your-search.search.windows.net"
export AZURE_SEARCH_INDEX="your-index-name"
export AZURE_SEARCH_API_KEY="your-search-key"
export AZURE_INFERENCE_ENDPOINT="https://your-foundry.inference.ai.azure.com"
export AZURE_INFERENCE_KEY="your-inference-key"
export AZURE_INFERENCE_MODEL="gpt-4"

# Run locally
func start
```

### 3. React Client Setup

```bash
cd client

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. MCP Server Setup

#### Local Development

```bash
cd mcp-campaign-insights

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export CAMPAIGN_INSIGHTS_FUNCTION_URL="https://your-function-app.azurewebsites.net/api/getcampaigninsights"
export MCP_API_KEY="optional-api-key"  # Optional

# Run server
python server.py
```

#### Docker Deployment

```bash
cd mcp-campaign-insights

# Build image
docker build -t mcp-campaign-insights .

# Run container
docker run -p 8000:8000 \
  -e CAMPAIGN_INSIGHTS_FUNCTION_URL="https://your-function-app.azurewebsites.net/api/getcampaigninsights" \
  -e MCP_API_KEY="your-api-key" \
  mcp-campaign-insights
```

## 📡 API Usage

### Azure Function Endpoint

**GET** `/api/GetCampaignInsights?q={your-question}`

**Example:**
```bash
curl "https://your-function-app.azurewebsites.net/api/GetCampaignInsights?q=What%20is%20the%20budget%20allocation%20for%20Q3%20Summer%20campaign?"
```

**Response:**
```json
{
  "rag": {
    "summary": "The Q3 Summer campaign has a total budget of $500,000...",
    "keyPoints": [
      "Digital advertising: $250,000",
      "Social media: $150,000",
      "Traditional media: $100,000"
    ],
    "recommendations": [
      "Consider increasing social media spend",
      "Focus on video content for better ROI"
    ]
  },
  "citations": [
    {
      "id": 1,
      "title": "Q3_Campaign_Budget.pdf",
      "source": "Q3_Campaign_Budget.pdf"
    }
  ]
}
```

### MCP Server Endpoint

**POST** `/mcp`

The MCP server exposes the `get_campaign_insights` tool for AI assistant integration.

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_SEARCH_ENDPOINT` | Azure AI Search endpoint URL | Yes |
| `AZURE_SEARCH_INDEX` | Search index name | Yes |
| `AZURE_SEARCH_API_KEY` | Search service API key | Yes |
| `AZURE_INFERENCE_ENDPOINT` | Azure AI Foundry endpoint | Yes |
| `AZURE_INFERENCE_KEY` | Foundry API key | Yes |
| `AZURE_INFERENCE_MODEL` | Model name (e.g., gpt-4) | Yes |
| `AZURE_INFERENCE_API_VERSION` | API version | No (default: 2024-05-01-preview) |
| `CAMPAIGN_INSIGHTS_FUNCTION_URL` | Function URL (for MCP server) | Yes (MCP only) |
| `MCP_API_KEY` | Optional API key for MCP auth | No |
| `PORT` | MCP server port | No (default: 8000) |

## 📦 Project Structure

```
azure-rag-demo/
├── GetCampaignInsights/          # Azure Function
│   ├── __init__.py               # Main function logic
│   ├── function.json             # Function binding config
│   └── requirements.txt          # Python dependencies
├── client/                       # React frontend
│   ├── src/                      # React source code
│   ├── package.json              # Node dependencies
│   ├── vite.config.js            # Vite configuration
│   └── index.html                # Entry HTML
├── mcp-campaign-insights/        # MCP server
│   ├── server.py                 # FastMCP server
│   ├── Dockerfile                # Container config
│   └── requirements.txt          # Python dependencies
├── AzureResources.ipynb          # Azure setup notebook
├── host.json                     # Function app config
└── requirements.txt              # Root dependencies
```

## 🧪 Testing

### Test Azure Function

```bash
curl "http://localhost:7071/api/GetCampaignInsights?q=test%20query"
```

### Test MCP Server

```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/call", "params": {"name": "get_campaign_insights", "arguments": {"question": "What is the Q3 budget?"}}}'
```

## 📝 Development

### React Client

```bash
cd client

# Development
npm run dev

# Lint
npm run lint

# Build for production
npm run build

# Preview production build
npm run preview
```

### Azure Function

```bash
# Run locally
func start

# Deploy to Azure
func azure functionapp publish <function-app-name>
```

## 🐳 Deployment

### Deploy MCP Server to Azure Container Apps

```bash
# Build and push to Azure Container Registry
az acr build --registry <your-acr> --image mcp-campaign-insights:latest .

# Create Container App
az containerapp create \
  --name mcp-campaign-insights \
  --resource-group <your-rg> \
  --environment <your-environment> \
  --image <your-acr>.azurecr.io/mcp-campaign-insights:latest \
  --target-port 8000 \
  --ingress external \
  --env-vars \
    CAMPAIGN_INSIGHTS_FUNCTION_URL=<function-url> \
    MCP_API_KEY=<optional-key>
```

## 🔒 Security

- Use Azure Key Vault for storing sensitive credentials
- Enable authentication on Azure Functions in production
- Implement rate limiting for public endpoints
- Use managed identities where possible
- Set `MCP_API_KEY` to protect MCP server endpoint

## 📄 License

This project is for demonstration purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📧 Support

For questions or issues, please open an issue in this repository.