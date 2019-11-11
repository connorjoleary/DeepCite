import os
CWD_FOLDER = os.path.dirname(os.path.abspath(__file__))

from claim import Claim

test_set_claims = os.path.join(CWD_FOLDER, 'testing_set', 'dillon_claims.txt')
f_claim = open(test_set_claims, 'r', errors='replace')
claims = [line for line in f_claim]
f_claim.close()

test_set_links = os.path.join(CWD_FOLDER, 'testing_set', 'dillon_links.txt')
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




