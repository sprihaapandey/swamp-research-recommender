#!/bin/bash
# Google Cloud deployment script

set -e

echo "🚀 Deploying Research Paper Recommender to Google Cloud"
echo "=================================================="

if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud CLI not found. Please install it first:"
    echo "   https://cloud.google.com/sdk/docs/install"
    exit 1
fi

if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
    echo "🔐 Please login to Google Cloud:"
    gcloud auth login
fi

PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo "📝 Please set your Google Cloud project ID:"
    read -p "Enter project ID: " PROJECT_ID
    gcloud config set project $PROJECT_ID
fi

echo "📋 Using project: $PROJECT_ID"

echo "🔌 Enabling required APIs..."
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Check if App Engine is initialized
if ! gcloud app describe &>/dev/null; then
    echo "🏗️  Initializing App Engine..."
    echo "Please choose your region (recommended: us-central for US, europe-west for Europe)"
    gcloud app create
fi

# Generate data files locally (faster than in cloud)
echo "📊 Generating data files locally..."
if [ ! -f "data/papers.json" ]; then
    echo "  Fetching papers..."
    cd scripts && python fetch_data.py && cd ..
fi

if [ ! -f "data/embeddings.npy" ]; then
    echo "  Generating embeddings..."
    cd scripts && python embeddings.py && cd ..
fi

if [ ! -f "data/index.idx" ]; then
    echo "  Building search index..."
    cd scripts && python index.py && cd ..
fi

echo "✅ Data files ready"

echo "🚀 Deploying to App Engine..."
gcloud app deploy app.yaml --quiet

URL=$(gcloud app describe --format="value(defaultHostname)")
echo ""
echo "🎉 Deployment complete!"
echo "🌐 Your app is live at: https://$URL"
echo ""
echo "📊 Monitor your app:"
echo "   Logs: gcloud app logs tail -s default"
echo "   Console: https://console.cloud.google.com/appengine"
echo ""