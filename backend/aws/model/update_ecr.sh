docker build --pull --rm -f "Dockerfile" -t 072491736148.dkr.ecr.us-east-2.amazonaws.com/deepcite "."

eval "$(aws ecr get-login --no-include-email)"
docker push 072491736148.dkr.ecr.us-east-2.amazonaws.com/deepcite