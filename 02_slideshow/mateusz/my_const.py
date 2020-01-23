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