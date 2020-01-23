# photo structure [3, 'H', 2, 5, 0]]
# id, orientation, number of tags, *tags
# photo 0 -> [0, 'H', 3, 0, 1, 2]
# photo 3 -> [3, 'H', 2, 5, 0]
# photo 1 -> [1, 'V', 2, 3, 4]
# photo 2 -> [2, 'V', 2, 5, 3]
PHOTO_ID = 0
PHOTO_ORIENTATION = 1
PHOTO_NUMBER_OF_TAGS = 2
PHOTO_TAGS = 3 

# slide 0 -> [0, '0', 'H', 3, 0, 1, 2]
# slide 1 -> [1, '3', 'H', 2, 5, 0]
# slide 2 -> [2, '1 2', 'V', 3, 3, 4, 5]
SLIDE_ID = 0
SLIDE_PARTS = 1
SLIDE_ORIENTATION = 2
SLIDE_NUMBER_OF_TAGS = 3
SLIDE_TAGS = 4

def read_input(file_name):
    f = open('./input/' + file_name, "r")
    
    l1 = f.readline().strip()
    number_of_photos = int(l1)
    
    photos_list = []
    photo_id = 0
    tags_dictionary = {}
    tag_id = 0

    for l in f:
        photo = l.strip().split(" ")

        tags = []
        for tag in photo[2:]:
            if tag in tags_dictionary.keys():
                tags.append(tags_dictionary[tag])
            else:
                tags_dictionary[tag] = tag_id
                tags.append(tag_id)
                tag_id += 1

        orientation = photo[0]
        number_of_tags = int(photo[1]) 

        photos_list.append([photo_id, orientation, number_of_tags] + tags)
        photo_id += 1

    f.close()

    return number_of_photos, photos_list, tags_dictionary

def write_solution(file_name, solution, slides, score=0):
    f = open('./output/' + file_name, "w")

    if score > 0:
        f.write("score -> %d\n" %(score))

    size = len(solution)
    f.write("size -> %d\n" %(size))
    
    for x in solution:
        slide = slides[x]
        f.write("%s\n" %(slide[SLIDE_PARTS]))

    f.close()

    return