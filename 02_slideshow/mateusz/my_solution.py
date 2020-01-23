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

def create_slideshow(slide_buckets, slides):
    # algorithm will be similar as with craeting slides
    # we take a first slide with highest number of tags and then we iterate through remaining ones 
    # till we have an optimal match which is k/2 - keep an eye on odd numbers there it will be rounded down
    # if we don't find any match in one iteration we add all slides to one degree below 

    slideshow_solution = []
    slideshow_score = 0

    slides_for_later = []

    # adding extra '0' as a precaution but that shouldn't be a big problem, 
    # unless there is no slide greater than expected length
    k = max(list(slide_buckets.keys()) + [0])
    while k > 1:
        # previous iteration
        slides_to_review = slides_for_later
        slides_for_later = []

        # extra values in case something like this exists
        if k in slide_buckets:
            slides_to_review += slide_buckets[k]

        # init with first slide
        if len(slideshow_solution) == 0:
            sl = slides_to_review.pop(0)
            slideshow_solution.append(sl)

        while len(slides_to_review) > 0:
            # last element on the list towards which we are comparing
            sl1 = slideshow_solution[-1]
            slide1 = slides[sl1]
            set1 = set(slide1[SLIDE_TAGS:])
            found_match = False

            # now we iterate through all remaining 
            for sl2 in slides_to_review:
                slide2 = slides[sl2]
                set2 = set(slide2[SLIDE_TAGS:])

                crossAB = len(set1 & set2)
                diffA = len(set1 - set2)
                diffB = len(set2 - set1)
                minAB = min(crossAB, diffA, diffB)

                # make sure we get the highest possible score at this bucket size
                # if yes we found a match and can iterate to next check
                if minAB >= k // 2:
                    slides_to_review.remove(sl2)

                    slideshow_solution.append(sl2)
                    slideshow_score += minAB                    

                    found_match = True
                    break
            
            # if we didn't find any solution here we need to 
            if not found_match:
                slides_for_later = slides_to_review.copy()
                slides_to_review.clear()

        k -= 1

    # this should take care of a case when we have no entry at all 
    # it shouldn't be a case for our examples
    if len(slideshow_solution) == 0:
        slideshow_solution.append(slides.values().pop(0))
    
    return slideshow_solution, slideshow_score
        