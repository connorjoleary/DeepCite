# DeepCite ![extension](https://img.shields.io/badge/extension-1.6.0-blue)

<p> In a world filled with fake news and alternative facts, get the real deep sources for your information. </p>

https://chrome.google.com/webstore/detail/deepcite/oibmgglhkkaigemacdkfeedffkjbpgoi?hl=en-US

Join the discussion here:

https://discord.gg/wr7uMAdWGz

![Discord Banner 2](https://discordapp.com/api/guilds/726491103381028884/widget.png?style=banner2)

## Table of Contents

* [Donate](#donate)
* [Run Locally](#run-locally)
* [Testing](#testing)
* [Configuration](#configuration)
* [Maintainers](#for-maintainers-eyes-only-eyes)
* [Authors](#authors)

## Donate

Unfortunatly running code is not cheap and I would really appreciate any support you could give to see this project flourish.

| website               | payment address                    |
|-----------------------|------------------------------------|
| Bitcoin               | 361Dq2e5wnjAhCnQ8FEkeiK3CYZZJ9QuGs |
| Venmo                 | @fippy24                           |
| Paypal and Sofi Money | connor.trumpet@gmail.com           |

## Run Locally

### Extension

Before it can connect to your local running lambda, update the call to talk to local host

##### Chrome

1. Install Google Chrome
2. In Chrome, navigate to `chrome://extensions/`
3. Enable developer mode
4. Then click `Load unpacked` 
5. Select DeepCite/extension folder

##### Firefox

1. Install Firefox
2. Navigate to `about:debugging`
3. Then select `This FireFox`
4. Next click on the button `Load Temporary Add-on...`
5. Select `DeepCite/extension/manifest.json`

### Lambda

Before if can connect to your local running model, update the env var `EC2_IP` to be `0.0.0.0`

##### Run
```
cd backend/lambda
python3 -m venv v-env-test
source v-env-test/bin/activate
pip3 install -r requirements.txt -r test_requirements.txt
gunicorn -c gunicorn_config.py wsgi:app
```

### Model

Run `python -m spacy download en_core_web_lg` once to download the model

```
cd backend/model
python3 -m venv v-env
source v-env/bin/activate
pip3 install -r requirements.txt
gunicorn -c gunicorn_config.py wsgi
```

## Testing

### Frontend Testing
* Download and install node.js from <a href="https://nodejs.org/en/"> their website </a>
* For the following commands navigate to DeepCite/extension folder
  * Use command `npm install mocha` to install testing framework
  * Use command `npm test` to run tests


* DeepCite/test-folder contains a basic web server meant for testing frontend functionality before we connect the frontend and backend together.
  * Follow the readme in that folder for its instructions

### System Testing
* To run a local server testing bash shell script:
* python -m spacy download en_core_web_sm
* run `pip install coverage`
* In DeepCite/backend, run run_tests.sh 

<small>Note: connection issues make occur when webscrapping, wait a minute then run again</small>

## Curl request for testing model

* Local testing:
`curl -d '{"claim":"the death of Sherlock Holmes almost destroyed the magazine that had originally published the stories. When Arthur Conan Doyle killed him off in 1893, 20,000 people cancelled their subscriptions. The magazine barely survived. Its staff referred to Holmes’ death as “the dreadful event”.", "link":"http://www.bbc.com/culture/story/20160106-how-sherlock-holmes-changed-the-world"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/api/v1/deep_cite`

## Reporting Bugs

If you happen upon any bugs please feel free to submit an official issue. When submitting bugs please try to follow these guidlines:

```
### Issue description: 

...

### Steps to reproduce:

...

### Expected result:

...

### Actual result:

...

### Details:

 * Browser version:
 * OS:
 * ( any additional relevant information and/or screenshots )
```

## Configuration

There are a couple ways to configure both the backend and the aws lambda service. The first priority, or the first place the config will look is in the root folder for a json file named `deep-cite-config.json`. Next the config will look in the environment, and finally anything not found in the json config or environment will fallback to the defaults. Here are the defaults and config options:

 * As a JSON `./DeepCite/deep-cite-config.json`:

 ```json
 {
  "backend": {
    "env": "development",
    "language": "en",
    "gn_path": "./DeepCite/backend/word_vectors/GoogleNews-vectors-negative300.bin",
    "server": {
      "host": "0.0.0.0",
      "port": "5000" 
    },
    "gunicorn": {
      "host": "0.0.0.0",
      "port": "8000" ,
      "workers": "1",
      "timeout": "180"
    },
    "model": {
        "similarity_cutoff": 0.67,
        "num_claims_returned": 15,
        "max_height": 5
    }
  },
  "aws": {
    "env": "development",
    "versions": {
      "model": "0.8.1",
      "lambda": "0.8.1",
      "api": "0.4.0",
      "extension": "1.6.0"
    },
    "secret": {
      "region": "us-east-2",
      "name": "rds_deepcite_sample"
    },
    "ec2": {
      "ip": "172.31.35.42",
      "port": "8000",
      "url": "http://172.31.35.42:8000/api/v1/deep_cite"
    }
  }
}
 ```

 * As an `.env`:

 ```bash
 ENV=development
 LANGUAGE=en
 GN_PATH=./DeepCite/backend/word_vectors/GoogleNews-vectors-negative300.bin
 SERVER_HOST=0.0.0.0
 SERVER_PORT=5000
 GUNICORN_HOST=0.0.0.0
 GUNICORN_PORT=8000
 GUNICORN_WORKERS=1
 GUNICORN_TIMEOUT=180
 MODEL_SIMILARITY_CUTOFF=.67
 MODEL_NUM_CLAIMS_RETURNED=15
 MODEL_MAX_HEIGHT=5
 EC2_IP=172.31.35.42
 EC2_PORT=8000
 SECRET_REGION=us-east-2
 SECRET_NAME=rds_deepcite_sample
 VERSIONS_MODEL=0.8.1
 VERSIONS_LAMBDA=0.8.1
 VERSIONS_API=0.4.0
 VERSIONS_EXTENSION=1.6.0
 ```

## For Maintainers eyes only :eyes:

#### Semantic Versioning Policy

It's not really the responsiblity of contributors to manange the CHANGELOG and/or version numbers. Also adding the version number to PR's can lead to needless conflicts. After a PR is merged it is a good idea to see if the CHANGELOG needs to be updated. If the CHANGELOG needs to be updated then the extension version should also be updated. For our version control we follow [semantic verisoning standards](https://semver.org/), which follows the general format: `MAJOR.MINOR.PATCH`.

 * **Patch:** increase when you make backwards compatible bug fixes.
 * **Minor:** increase when you add functionality in a backwards compatible manner and set _patch_ to 0.
 * **Major:** when you make incompatible API changes and set _patch_ and _minor_ to 0.

There are multiple services in this repo and each has there own version number. Luckily there is a shell script in the `scripts/` that makes updating the version for each service very simple.

 * The script itself is pretty self explanitory for example if you just added functionality _(so a minor update)_ to the `model` you can update its version like so:

```bash
$ cd scripts/
$ ./semver.sh minor model
```

 * There are also some git options so if you fix a bug in lambda and you want the version number to be committed then do this:

```bash
$ cd scripts/
$ ./semver.sh patch lambda commit
```

 * Note: in this case the commit message will be "lambda patch update" and in general these auto commit messages follow this format `"$SERVICE $ACTION update"`

**NOTE:** Our git tags are associated with the `extension` version number so if you update the extension version number a git tag will be added. This means that when you end up pushing your changes don't forget to push the tags like so:

```bash
$ git push --follow-tags
```

## Authors
Connor O'Leary, Joe Pagani, and Jake Heaser

With great help from the University of Wisconsin, Madison CS506 team
Shourya Goel, Jiayi Hu, Vinay Janardhanam, Dillon O'Leary, Noah SickLick, and Catherine Yan
