
REGION=us-east-2
RUNTIME=python3.7

pip install -r requirements.txt -t model-dependencies/
zip -r dependencies.zip model-dependencies/

aws lambda publish-layer-version \
    --layer-name dependencies \
    --region $REGION \
    --description "dependencies for model" \
    --zip-file fileb://dependencies.zip \
    --compatible-runtimes $RUNTIME
