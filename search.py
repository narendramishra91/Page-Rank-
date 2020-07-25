import json
import numpy as np

links_list = []

def find_url(keyword):
    global links_list
    with open('sample.json', 'r+') as openfile:
        json_object = json.load(openfile)
        print("Pages Without ranking")
        if keyword in json_object:
            for url in json_object[keyword]:
                print(url)
                links_list.append(url)
        else:
            print("not in database")
   
print("Write the keyword you want to search:")
keyword = input()
find_url(keyword)

matrix = []
transition_matrix = []
col = []
def create_matrix():
    global links_list
    global matrix
    global col
    with open('links.json', 'r+') as openfile:
        json_object = json.load(openfile)
        for link in links_list or []: 
            for x in links_list:
                if x in json_object[link]:
                    col.append(1)
                else:
                    col.append(0)
            n = col.count(1)
            new_col = [x/n for x in col]
            matrix.append(new_col)
            col = []
    A = np.array(matrix)
    A_transpose = A.transpose()
    return A_transpose