import random
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog


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

def create_permutations(vocabulary, p=4):
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


def load_text_from_file(text_area):
    file_path = filedialog.askopenfilename(
        title="Select Text File",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text_area.delete("1.0", tk.END)
                text_area.insert(tk.END, file.read())
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")

def compare_texts():
    text1 = text_area1.get("1.0", tk.END).strip()
    text2 = text_area2.get("1.0", tk.END).strip()

    if not text1 or not text2:
        messagebox.showerror("Error", "Please enter text in both text areas or load files.")
        return

    shingles1 = create_shingles(text1)
    shingles2 = create_shingles(text2)
    vocabulary = create_vocabulary(shingles1, shingles2)

    if not vocabulary:
        result_text.delete("1.0", tk.END)
        result_text.insert("1.0", "No common shingles found. Cannot calculate similarity.")
        return

    vector1 = create_vector(vocabulary, shingles1)
    vector2 = create_vector(vocabulary, shingles2)
    permutations_list = create_permutations(vocabulary)
    signature1 = create_signatures(permutations_list, vocabulary, vector1)
    signature2 = create_signatures(permutations_list, vocabulary, vector2)

    j_index = calculate_jaccard_index(vector1, vector2)
    sig_sim = signature_similarity(signature1, signature2)

    result_text.delete("1.0", tk.END)
    result_text.insert("1.0", f"Jaccard Index Similarity: {j_index}\n")
    result_text.insert(tk.END, f"MinHash Signature Similarity: {sig_sim}\n")

# GUI Setup
window = tk.Tk()
window.title("Text Similarity Checker")

# Text Area 1
label1 = tk.Label(window, text="Text 1:")
label1.pack(pady=5)
text_area1 = scrolledtext.ScrolledText(window, height=10, width=50)
text_area1.pack(padx=10, pady=5)
load_button1 = tk.Button(window, text="Load from File", command=lambda: load_text_from_file(text_area1))
load_button1.pack(pady=2)

# Text Area 2
label2 = tk.Label(window, text="Text 2:")
label2.pack(pady=5)
text_area2 = scrolledtext.ScrolledText(window, height=10, width=50)
text_area2.pack(padx=10, pady=5)
load_button2 = tk.Button(window, text="Load from File", command=lambda: load_text_from_file(text_area2))
load_button2.pack(pady=2)

# Compare Button
compare_button = tk.Button(window, text="Compare Texts", command=compare_texts)
compare_button.pack(pady=10)

# Result Area
result_label = tk.Label(window, text="Similarity Results:")
result_label.pack(pady=5)
result_text = scrolledtext.ScrolledText(window, height=5, width=50)
result_text.pack(padx=10, pady=5)

window.mainloop()
