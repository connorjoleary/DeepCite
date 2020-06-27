from config import config
from claim import Claim
import tokenizer as nlp

def test_controller():
    test_set_claims = os.path.join(config['cwd'], 'testing_set', 'claims.txt')
    f_claim = open(test_set_claims, 'r', errors='replace')
    claims = [line for line in f_claim]
    f_claim.close()

    test_set_links = os.path.join(config['cwd'], 'testing_set', 'links.txt')
    f_links = open(test_set_links, 'r', errors='replace')
    links = [line for line in f_links]
    f_links.close()

    claim_Class = []
    for x in range(len(claims)):
        claim_new = Claim(links[x].strip(), claims[x].strip(), 0)
        claim_Class.append(claim_new)

    for claim in claim_Class:
        # print(claim)
        print(claim.get_full_claim())

test = []
def test_accuracy():
    test_set_claims = os.path.join(config['cwd'], 'testing_set', 'claims.txt')
    f_claim = open(test_set_claims, 'r', errors='replace')

    claims = [line for line in f_claim]
    f_claim.close()

    for num, claim in enumerate(claims):
        test_set_links = os.path.join(config['cwd'], 'testing_set', 'link')
        f_text = open(test_set_links+ str(num) + ".txt", 'r', errors='replace')

        text = [paragraph for paragraph in f_text]
        f_text.close()

        test.append(nlp.predict(claim, text, 1))
        #print("\nNext set: \n")

    file_path = os.path.join(config['cwd'], 'test-file.txt')
    test_file = open(file_path, 'w+', errors='replace')
    for x in test:
        test_file.write(str(x) + '\n\n\n\n\n')
    test_file.close()


def test_structure():
    test_set_claims = os.path.join(config['cwd'], 'testing_set', 'simdiff.txt')
    f_claim = open(test_set_claims, 'r', errors='replace')

    claims = [line for line in f_claim]
    f_claim.close()


    test_set_links = os.path.join(config['cwd'], 'testing_set', 'simdiffsents.txt')
    f_text = open(test_set_links, 'r', errors='replace')

    text = [line for line in f_text]
    f_text.close()

    predict = []
    for x in range(len(claims)):
        
        predict.append(nlp.predict(claims[x], text[x], 1))

    for x in range(len(claims)):
        print(text[x])
        print(predict[x])


if "__main__":
    test_controller()
    test_accuracy()
    test_structure()
