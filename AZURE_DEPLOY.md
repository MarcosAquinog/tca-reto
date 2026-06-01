# Desplegar en Azure

## 1. Requisitos
- Cuenta de Azure
- Azure CLI instalado
- Docker instalado

## 2. Pasos de Despliegue

### Opción A: Azure Container Instances (ACI) - MÁS SIMPLE

```bash
# Login a Azure
az login

# Crear grupo de recursos
az group create --name tca-reto --location eastus

# Crear Azure Container Registry
az acr create --resource-group tca-reto --name tcareto --sku Basic

# Build y push de imagen
az acr build --registry tcareto --image tca-reto:latest .

# Desplegar en ACI
az container create \
  --resource-group tca-reto \
  --name tca-reto-app \
  --image tcareto.azurecr.io/tca-reto:latest \
  --registry-login-server tcareto.azurecr.io \
  --registry-username <username> \
  --registry-password <password> \
  --ports 8501 \
  --environment-variables STREAMLIT_SERVER_PORT=8501
```

### Opción B: Azure App Service

```bash
# Crear App Service Plan
az appservice plan create --name tca-plan --resource-group tca-reto --sku B1 --is-linux

# Crear Web App
az webapp create --resource-group tca-reto --plan tca-plan --name tca-reto-app --deployment-container-image-name tcareto.azurecr.io/tca-reto:latest
```

## 3. Obtener URL de la aplicación

```bash
az container show --resource-group tca-reto --name tca-reto-app --query ipAddress.fqdn
```

## 4. Variables de entorno (si es necesario)
Agregar en el comando `az container create` con `--environment-variables`

