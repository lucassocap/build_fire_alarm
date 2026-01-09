#!/bin/bash
set -e

# Configuration
PROJECT_ID=$1
REGION="us-central1"
REPO_NAME="cicuma-fire"
TAG="latest"

if [ -z "$PROJECT_ID" ]; then
    echo "Usage: ./deploy_gcp.sh [PROJECT_ID]"
    exit 1
fi

echo "🔥 Cicuma Fire: Starting GCP Deployment Pipeline for project: $PROJECT_ID"

# 1. Enable Services
echo "[1/4] Enabling Required APIs..."
# gcloud services enable run.googleapis.com artifactregistry.googleapis.com --project $PROJECT_ID

# 2. Create Artifact Registry (if not exists)
echo "[2/4] Checking Artifact Registry..."
if ! gcloud artifacts repositories describe $REPO_NAME --project $PROJECT_ID --location $REGION > /dev/null 2>&1; then
    echo "Creating repository $REPO_NAME..."
    gcloud artifacts repositories create $REPO_NAME --repository-format=docker --location=$REGION --description="Cicuma Fire Containers" --project=$PROJECT_ID
fi

# 3. Build & Submit Images (Cloud Build)
echo "[3/4] Building Containers (Cloud Build)..."

# Cortex
echo " -> Building Cortex..."
gcloud builds submit ./cortex --tag "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/cortex:$TAG" --project $PROJECT_ID

# Cell
echo " -> Building Cell..."
gcloud builds submit ./cell_fire_alarm --tag "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/cell:$TAG" --project $PROJECT_ID

# Web
echo " -> Building Web Workbench..."
gcloud builds submit ./web --tag "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/web:$TAG" --project $PROJECT_ID

# 4. Deploy to Cloud Run
echo "[4/4] Deploying to Cloud Run..."

# Deploy Cell (Internal)
echo " -> Deploying Cell Logic..."
gcloud run deploy cicuma-cell-fire \
    --image "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/cell:$TAG" \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --project $PROJECT_ID
    
CELL_URL=$(gcloud run services describe cicuma-cell-fire --platform managed --region $REGION --format 'value(status.url)' --project $PROJECT_ID)
echo "    Cell URL: $CELL_URL"

# Deploy Cortex (Gateway)
echo " -> Deploying Cortex Gateway..."
gcloud run deploy cicuma-cortex \
    --image "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/cortex:$TAG" \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars CELL_URL=$CELL_URL \
    --project $PROJECT_ID

CORTEX_URL=$(gcloud run services describe cicuma-cortex --platform managed --region $REGION --format 'value(status.url)' --project $PROJECT_ID)
echo "    Cortex URL: $CORTEX_URL"

# Deploy Web (Frontend)
echo " -> Deploying Web Workbench..."
gcloud run deploy cicuma-web \
    --image "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/web:$TAG" \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars NEXT_PUBLIC_CORTEX_URL=$CORTEX_URL \
    --set-env-vars AUTH_SECRET="CicumaFireAlarmSecretKey2026" \
    --set-env-vars NEXTAUTH_SECRET="CicumaFireAlarmSecretKey2026" \
    --set-env-vars AUTH_TRUST_HOST=true \
    --set-env-vars AUTH_URL="https://cicuma-web-yp7mw3rcmq-uc.a.run.app" \
    --set-env-vars GOOGLE_CLIENT_ID="${GOOGLE_CLIENT_ID}" \
    --set-env-vars GOOGLE_CLIENT_SECRET="${GOOGLE_CLIENT_SECRET}" \
    --project $PROJECT_ID

WEB_URL=$(gcloud run services describe cicuma-web --platform managed --region $REGION --format 'value(status.url)' --project $PROJECT_ID)

echo "✅ Deployment Complete!"
echo "🌍 Access the Workbench at: $WEB_URL"
echo ""
echo "⚠️  ACTION REQUIRED: COPY-PASTE CONFIGURATION ⚠️"
echo "To enable Login, you MUST add this URL to your Google Cloud Console:"
echo "---------------------------------------------------------------"
echo "URI: $WEB_URL/api/auth/callback/google"
echo "---------------------------------------------------------------"
echo ""
echo "👉 Direct Link: https://console.cloud.google.com/apis/credentials/oauthclient/${GOOGLE_CLIENT_ID}?project=$PROJECT_ID"
echo ""
