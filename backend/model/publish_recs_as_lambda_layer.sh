REGION=us-east-2
RUNTIME=python3.7

# pip install -r requirements.txt -t model-dependencies/python/lib/python3.7/site-packages/
zip -r dependencies.zip python/

aws lambda publish-layer-version \
    --layer-name dependencies \
    --region $REGION \
    --description "dependencies for model" \
    --zip-file fileb://dependencies.zip \
    --compatible-runtimes $RUNTIME

rm dependencies.zip