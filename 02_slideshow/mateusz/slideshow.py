import sys

import my_io
import my_debug
import my_cleanup
import my_solution

# read input parameters
if len(sys.argv) < 2:
    print("Not enough parameters")
    sys.exit(0)

my_file = sys.argv[1]
number_of_photos, photos_list, tags_dictionary = my_io.read_input(my_file)
# print(number_of_photos)
# print(photos_list)
# print(tags_dictionary)

# this is a dictionary with all information, beside tags_dictionary which is separate
horizontal_photos, vertical_photos = my_cleanup.group_photos_dict(photos_list)
# my_debug.print_photos(horizontal_photos)
# my_debug.print_photos(vertical_photos)

# put horizontal and vertical into a buckets, but as a value keep only id of the photo in bucket
horizontal_buckets = my_cleanup.create_buckets_simple(horizontal_photos.values())
vertical_buckets = my_cleanup.create_buckets_simple(vertical_photos.values())
# my_debug.print_buckets(horizontal_buckets)
# my_debug.print_buckets(vertical_buckets)

slides = my_cleanup.create_slides(horizontal_buckets, horizontal_photos, vertical_buckets, vertical_photos)
# my_debug.print_slides(slides)

# now we need to bucket for slides
slide_buckets = my_cleanup.create_slide_buckets(slides.values())
# my_debug.print_buckets(slide_buckets)

solution, score = my_solution.create_slideshow(slide_buckets, slides)
my_io.write_solution(my_file, solution, slides, score)


