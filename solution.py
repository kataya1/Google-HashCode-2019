import sys
import logging
import collections

# setps of solution by kataya
# things changed while writing the doc and while coding so it's not very consistent with what i did and it's not complete
# Hash code
# 0.
# 1.Add all H images into a List(make it a dict with image number as key and set of tags as value)
# 2. Get the image with  minimum tags to start the iterative process with iy. (for better score)
# 3,Put the tags of that image in a dict ( hash table) and while you’re inserting the tags into a dict
# 	Use variable dictsize and for each tag dictsize += 1
# 4. three variables ( in1not2, common, in2not1) iterate over the list(stack)  (the complexity should be less than O(n2) as we pop one element from the list every iteration if we iterate over all pictures but it is a stack that is part of the list containing all pictures if the stack size was 10 it only compare the current image with the images in the stack so the complexity is O(10n)
#  we can trade off between score and efficiency )we will try to get max score here for now for each element we have at most 100 tags so O(100* n^2). And we can see which element is in the hash at O(1) -amortized cost O(n),
# 5- compare the tags image we at now in the list with the image that we have it’s tags in a dict
# If exists
# 	common += 1
# If doesn’t
# 	In2not1 += 1
# You get dictsize  when you were inserting the elements in the dictionary
# And to get>>  in1not2 = dictsize - common
# (revision; it’s actully set rather than a dict)
# len() time complexity is O(1) so if we get the 3 vars by
# Common by intersection O(len(min(len(s),len(t)) worestcase O(len(s) * len(t)
# len(comparator) - common it O(1) in1not2
# And len(current)-len(common) O(1) in2not1
#
# 6- We take the minimum of those 3 variables and put it in a variable (interest) and iterate over the whole stack to find the picture that give the maximum interest
# 	Save the picture number and the interest and put it into the output file
#
# 7-Then we pop this comparator image from the list and use the the image with max interest as the new comparator,delete the dict (del dict) the go to number 3
#
# 8- as for vertical images V now this solution in not optimal or scalable but we can make a list with 2 picture and a set of tags set because
# *new: if we sort the vertical and horizontal list according to no of tags we could get a maximum likely hood of where the best next slide could be depending on the number of tags in this slide
# if you you have the current slide with ten tag so idiely you'd want the next slide with 10 tags 5 common and 5 not each
# instead of sorting will make another hash with keys as the number of tags and values as the position in the big_hash
# and then we'll push those positions into a stack of maximum likelyhood
# logging.basicConfig(filename='debugging.log',level=logging.DEBUG)
# logging.debug('This message should go to the log file')
# global vars
startline, mintags, HorV = 0, 200, None
keyH, keyV, keyVV = 0, 0, 0
slides = []
hash_v = {}
hash_h = {}
# is a compination of elements in hashV  key -> pos. in big_hash  value -> tuple(positions in input, union of tags)
hash_vv = {}
# hash max likelyhood
# key -> no. of tags  value -> list of positions in big_hash

hash_tags = {}


def main():
    file_reader()
    vertical_combiner()
    slide_creator()
    file_writer()
    # print(startline, mintags)
    # print(hash_h)
    # print(hash_v)
    # print(hash_v[1][1])
    # print(hash_h, '\n', hash_vv)
    # print(hash_tags, type(hash_tags), type(hash_tags[2]))


def file_reader():
    f = open('b_lovely_landscapes.txt', 'r')
    n = int(f.readline())
    for line in range(n):
        linecontent = f.readline().split()
        hash_maker(line, linecontent)
    f.close()


def hash_maker(line, linecontent):
    # to optimize the start check no. 2
    global keyH, keyV, mintags, startline
    tags = set(linecontent[2:])
    if linecontent[0] == "H":
        hash_h[keyH] = line, tags
        # parsing keyH instead of line to know it's place in the new list
        start_line_finder(int(linecontent[1]), keyH, "H")
        hash_tags_maker(int(linecontent[1]), keyH)
        keyH += 1
    elif linecontent[0] == "V":
        hash_v[keyV] = line, tags
        keyV += 1
    # print(hash_vv)
    # print(HorV, startline,mintags)

    del tags


def start_line_finder(no_of_tags, line, vertical_or_H):
    # takes number of tags , line (position in big_hash) and checks  where to start
    global mintags, startline, HorV
    if no_of_tags < mintags:
        startline = line
        mintags = no_of_tags
        HorV = vertical_or_H


def vertical_combiner():
    # print(hash_v)
    # print(type(hash_v),
    #       type(hash_v[0]),
    #       type(hash_v[0][0]),
    #       type(hash_v[0][1]))
    # keyVV = keyH; to use chainmapping of two dicts
    global keyVV
    keyVV = keyH
    for i in hash_v:
        for j in range(i, len(hash_v)):
            if i == j:
                continue
            else:
                # print(i, j, "\t", hash_v[i], hash_v[j], '\t', hash_v[i][0], hash_v[j][0], "\t", hash_v[i][1],
                #       hash_v[j][1])
                union_of_two_sets = hash_v[i][1].union(hash_v[j][1])
                hash_vv[keyVV] = "{} {}".format(hash_v[i][0], hash_v[j][0]), union_of_two_sets
                start_line_finder(len(union_of_two_sets), keyVV, "V")
                hash_tags_maker(len(union_of_two_sets), keyVV)
                keyVV += 1
                # print(hash_vv)
                # print(HorV,startline,mintags)


def hash_tags_maker(no_of_tags, line):
    # makes
    if no_of_tags in hash_tags:
        hash_tags[no_of_tags].add(line)
    else:
        # hash_tags[no_of_tags] = collections.deque([line])
        hash_tags[no_of_tags] = {line}


def slide_creator():
    big_hash = {**hash_h, **hash_vv}
    current_line = startline
    slides.append(big_hash[current_line][0])
    for i in range(len(big_hash)):
        install_xxx()
        line = abs_maxinterestfinder(current_line, big_hash)
        # print(current_line,"-",line)
        # print(slides)

        if line is None:
            break
        slides.append(big_hash[line][0])
        # print(current_line,"-",line)
        # print(slides)
        big_hash.pop(current_line)
        current_line = line


def install_xxx():
    print("Installing XXX...      ", end="", flush=True)


def relative_max_interest(current_line,big_hash):

    pass


def abs_maxinterestfinder(currentline, givenhash):
    # returns the line where the max interest is at
    current_interest = 0
    line_of_max_interest = None
    for keys in givenhash.keys():
        if currentline == keys:
            continue
        challenging_interest = interest(givenhash[currentline][1], givenhash[keys][1])
        if challenging_interest >= current_interest:
            current_interest = challenging_interest
            line_of_max_interest = keys
        else:
            continue
    return line_of_max_interest

    # if challenging_interest > max_interest_val:
    #     return challenging_interest, line
    # else:
    #     return max_interest_val, currentline


# optimize later
# def slide_maker():
#     pass
#     # slides[] will contain the final the slides that's written in the final output file
#     # a stack of maximum likelyhood which will contain the positions slides in
#     # the big_hash that contains the maximum likelyhood of bigger interst
#     big_hash = collections.ChainMap(hash_h, hash_vv)
#     #current_tag is the key in the hash_tags hash
#     current_tag = mintags
#     #currennt line is the line that should pass on all big_hash
#     current_line = startline
#
#     current_max_interest = 0
#     for x in hash_tags[current_tag]:
#         challenging_interest = max_interest(big_hash[current_line][1], big_hash[x][1])
#         current_max_interest, line = abs_maxinterestfinder(current_max_interest,challenging_interest, current_line, x)
#     hash_tags[current_tag].remove(line)
#     current_line = line
#
#
#     # print("\n", big_hash, "\n", type(big_hash), "\n", big_hash.maps, "\n", type(big_hash.maps), "\n", list(big_hash.keys()),
#     #       "\n", type(big_hash.keys()), "\n", "\n", list(big_hash.values()),
#     #       "\n", type(big_hash.values()), "\n")
#     # for key, val in big_hash.items()
#     # print(stack_ml)
#
#


def interest(current, challenger):
    # takes two stacks compares them and reurns max interest
    common = len(current.intersection(challenger))
    in1not2 = len(current) - common
    in2not1 = len(challenger) - common
    return min(common, in1not2, in2not1)


#
#
# def stack_feeder(set, dirChange):
#     if dirChange > 0:
#         pass
#     elif dirChange < 0:
#         pass


def file_writer():
    f = open("b_sol.txt", "w")
    f.write("{}\n".format(int(len(slides))))
    for i in range(len(slides)):
        if isinstance(slides[i], int):
            f.write("{}\n".format(slides[i]))
        elif isinstance(slides[i], str):
            f.write("{} {}\n".format(int(slides[i][0]), int(slides[i][2])))
    f.close()


main()


def files_iterator():
    pass


def reseter():
    pass

# main()
