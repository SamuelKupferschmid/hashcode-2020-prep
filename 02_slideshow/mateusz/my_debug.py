# looks it's not necessary in the end :D
debug_option = True

def print_photos(photos):
    for k in sorted(photos.keys()):
        print("photo %d -> %s" %(k, photos[k]))

def print_buckets(buckets):
    if not debug_option:
        return 

    for k in sorted(buckets.keys()):
        print("Bucket key: %d" %(k))

        for p in buckets[k]:
            print(p)

        print()

def print_slides(slides):
    if not debug_option:
        return 

    for k in sorted(slides.keys()):
        print("slide %d -> %s" %(k, slides[k]))