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

# # return separate list of horizontal and vertical photos list
# def group_photos_list(photos_list):
#     horizontal_photos = []
#     vertical_photos = []

#     for photo in photos_list:
#         if photo[PHOTO_ORIENTATION] == 'H':
#             horizontal_photos.append(photo)
#         elif photo[PHOTO_ORIENTATION] == 'V':
#             vertical_photos.append(photo)

#     return horizontal_photos, vertical_photos

# return separate dict of horizontal and vertical photos list - this enhancement to have a link between photo id and object
def group_photos_dict(photos_list):
    horizontal_photos = {}
    vertical_photos = {}

    for photo in photos_list:
        if photo[PHOTO_ORIENTATION] == 'H':
            horizontal_photos[photo[PHOTO_ID]] = photo
        elif photo[PHOTO_ORIENTATION] == 'V':
            vertical_photos[photo[PHOTO_ID]] = photo

    return horizontal_photos, vertical_photos


# # we add photos into size buckets that we could control them better and create more effective slides
# # this version creates buckets with whole content
# def create_buckets_full(photos_list):
#     buckets = {}

#     for photo in photos_list:
#         n = photo[PHOTO_NUMBER_OF_TAGS]
        
#         if n in buckets.keys():
#             buckets[n].append(photo)
#         else:
#             buckets[n] = []
#             buckets[n].append(photo)
    
#     return buckets

# we add photos into size buckets that we could control them better and create more effective slides
# this version creates buckets with id to photos
def create_buckets_simple(photos_list):
    buckets = {}

    for photo in photos_list:
        n = photo[PHOTO_NUMBER_OF_TAGS]
        
        if n in buckets.keys():
            buckets[n].append(photo[PHOTO_ID])
        else:
            buckets[n] = []
            buckets[n].append(photo[PHOTO_ID])
    
    return buckets

# create new buckets for horizontal and vertical slides
# slide 0 -> [0, '0', 'H', 3, 0, 1, 2]
# slide 1 -> [1, '3', 'H', 2, 5, 0]
# slide 2 -> [2, '1 2', 'V', 3, 3, 4, 5]
def create_slide_buckets(slides):
    buckets = {}

    for slide in slides:
        n = slide[SLIDE_NUMBER_OF_TAGS]

        if n in buckets.keys():
            buckets[n].append(slide[SLIDE_ID])
        else:
            buckets[n] = []
            buckets[n].append(slide[SLIDE_ID])

    return buckets

# we create a new dictionary with id and 
# horizontal and vertical photos are dicts
def create_slides(horizontal_buckets, horizontal_photos, vertical_buckets, vertical_photos):
    slides = {}
    id = 0

    # horizontal photos 
    # we have simple method, we just need to add a slide id to already existing horizontal photo
    # we iterate through each list of values in horizontal bucket list
    # beside adding an id we need to add the rest of the photo, to be able to grab remain
    for l in horizontal_buckets.values():
        for i in l:
            photo = horizontal_photos[i]
            slides[id] = [id] + [str(photo[PHOTO_ID])] + photo[PHOTO_ORIENTATION:]
            id +=1

    # vertical photos
    # now we have to merge, we start from the end and we have to make as longest tags
    # ideally if we have 2 vertical photos of length k we should have a final tag size 2k
    # if that's not possible we can make 2k - 1
    # if that doesn't work all unpaired vertical photos go to lower categor of k-1

    # photos for later are these which didn't make in current round and will be added to next round
    photos_for_later = []

    # we iterate from maximum bucket key to 1, 
    # adding extra '0' in case we have no vertical entries in bucket
    k = max(list(vertical_buckets.keys()) + [0])
    while k > 0:
        # we have at least two options to build vertical slides, either fully recursive with optimal solution
        # or greedy first good match and we go further

        # photos which will be taken in current iteration 
        # once photos for later are added we can reinitialize them
        photos_to_review = photos_for_later
        photos_for_later = []

        if k in vertical_buckets:
            photos_to_review += vertical_buckets[k]

        # the best option will be then when we have the most tags in slides
        # we take iterative solution with comparing all items with each other - start with simplest matches later we figure out other way
        # remember that when a photos to review list is updated it has to updated be aware of concurency exception

        # we can add random selector but that won't give us a better solution, but may
        while len(photos_to_review) > 0:
            ph1 = photos_to_review.pop(0)
            photo1 = vertical_photos[ph1]
            set1 = set(photo1[PHOTO_TAGS:])
            found_match = False

            # we search a first best match if that we find we move on to next iteration
            for ph2 in photos_to_review:
                photo2 = vertical_photos[ph2]
                set2 = set(photo2[PHOTO_TAGS:])

                # if we get an optimal match then remove also second from the list and go with next iteration
                if len(set1 | set2) >= 2*k:
                    photos_to_review.remove(ph2)

                    # and now we need to create a new slide with ph1 and ph2
                    # slides[id] = [ph1, ph2, 'V', len(set1 | set2)] + sorted(set1 | set2)
                    slides[id] = [id] + [str("%s %s" %(ph1, ph2)), 'V', len(set1 | set2)] + sorted(set1 | set2)
                    id +=1

                    # this just in case but should be ok without conditional case
                    found_match = True
                    break

            if not found_match:
                photos_for_later.append(ph1)
        
        # end of the iteration don't adjust value earlier !!!
        k -= 1

    # # if at the end we still have some photos to review we can still do something about them
    # # connect them and make a slides of size at least 2
    # for k = min(slide_buckets.keys()) - 1 to 2:
    #     photos_to_review = photos_for_later + list(vertical_buckets[k])
    #     photos_for_later = []

    #     ph1 = photos_for_later.pop(0)
    #     photo1 = vertical_photos[ph1]
    #     set1 = set(photo1[PHOTO_TAGS:])
    #     found_match = False

    #     # we search a first best match if that we find we move on to next iteration
    #     for ph2 in photos_for_later:
    #         photo2 = vertical_photos[ph2]
    #         set2 = set(photo2[PHOTO_TAGS:])

    #         # if we get an optimal match then remove also second from the list and go with next iteration
    #         if len(set1 | set2) >= 2*k:
    #             photos_for_later.remove(ph2)

    #             # and now we need to create a new slide with ph1 and ph2
    #             # slides[id] = [ph1, ph2, 'V', len(set1 | set2)] + sorted(set1 | set2)
    #             slides[id] = [id] + [str("%s %s" %(ph1, ph2)), 'V', len(set1 | set2)] + sorted(set1 | set2)
    #             id +=1

    #             # this just in case but should be ok without conditional case
    #             found_match = True
    #             break

    #     # don't have to do anything more first element already removed
    #     if not found_match:
    #         photos_for_later.append(ph1)


    return slides


