import random
import time


def create_shingles(text, k=2):
    # k variable represents our shingle size
    if not text:
        return []

    result = []
    for i in range(len(text) - 1):
        result.append(text[i:i+2])
    return result

def create_vocabulary(*args):
    vocabulary = {}
    i = 0
    if not args:
        print("no arguments were passed")
        return []

    for arg in args:
        if not isinstance(arg, list):
            continue

        for shingle in arg:
            vocabulary.update({i: shingle})
            i += 1
    return vocabulary

def create_vector(vocabulary, shingle_sequence):
    vector_list = []
    for shingle in vocabulary.values():
        if shingle in shingle_sequence:
            vector_list.append(1)
        else:
            vector_list.append(0)
    return vector_list

def calculate_jaccard_index(*vectors):
    c11, c10, c01 = 0, 0, 0
    counts_list = []
    jaccard_index_list = []
    if not vectors:
        print("No vectors were passed")
        return
    for i in range(len(vectors)-1):
        for j in range(len(vectors)-1):
            if i == j + 1:  # Skip same vector comparison
                continue
            # print("Comparing: " + "v" + str(i+1) + " and v" + str(j+2))
            for x in range(len(vectors[i])):
                if vectors[i][x] == vectors[j+1][x] and vectors[i][x] == 1:
                    c11 += 1
                elif vectors[i][x] != vectors[j+1][x] and vectors[i][x] == 1:
                    c10 += 1
                elif vectors[i][x] != vectors[j+1][x] and vectors[i][x] == 0:
                    c01 += 1
            if not c11 == c10 == c01 == 0:
                counts_list.append([c11, c01, c10])
            c11, c10, c01 = 0, 0, 0
    for x11, y01, z10 in counts_list:
        jaccard_index_list.append(round(x11/(x11+y01+z10),4))
    return jaccard_index_list

def create_permutations(vocabulary, p=100):
    numbers = list(vocabulary.keys())
    perm_list = []
    for i in range(p):
        temp_nums = numbers[:]
        random.shuffle(temp_nums)
        perm_list.append(temp_nums)
    return perm_list

def create_signatures(permutations, vocabulary, *vectors):
    p = permutations
    temp_signature = []
    signature = []

    for i in range(len(permutations)):
        for j in range(len(vectors)):
            # print("Comparing: " + "p" + str(i+1) + " and v" + str(j+1))
            for x in range(len(vectors[j])):
                # print("at " + str(vectors[j][p[i][x]]) + " x = " + str(x))
                if vectors[j][p[i][x]] == 1:
                    temp_signature.append(x)
                    # print("appended")
                    break
        signature.append(temp_signature[:])
        temp_signature.clear()

    return signature

def get_vector_signatures(signature):
    sig = []
    temp_sig = []
    # print(len(signature[0]))
    # print(len(signature))
    for j in range(len(signature[0])):
        for i in range(len(signature)):
            temp_sig.append(str(signature[i][j]))
        sig.append(temp_sig[:])
        temp_sig.clear()
    return sig

def signature_similarity(s1, s2):
    identical_count = 0
    for i in range(len(s1)):
        if s1[i] == s2[i]:
            identical_count += 1
    return identical_count/len(s1)

text1, text2, text3 = "bvxvmt", "brxvmt", "vvkxvb3"

s1, s2, s3 = create_shingles(text1), create_shingles(text2), create_shingles(text3)

vocab = create_vocabulary(s1, s2, s3)
v1, v2, v3 = create_vector(vocab, s1), create_vector(vocab, s2), create_vector(vocab, s3)

jaccard_index = calculate_jaccard_index(v1, v2, v3)

permutations_list = create_permutations(vocab)
signatures = create_signatures(permutations_list, vocab, v1,v2,v3)

v_signatures = get_vector_signatures(signatures)
print("Signatures:")
for i in range(len(v_signatures)):
    print("".join(v_signatures[i]))
print("Jaccard Index =", jaccard_index)
print("Signature Similarity = ", signature_similarity(v_signatures[0], v_signatures[1]))
