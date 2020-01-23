import fs from 'fs'
import es from 'event-stream'
import getStream from 'get-stream'
import { serializable, list, primitive, deserialize } from 'serializr'
import _ from 'lodash'

class Picture {
  @serializable idx: number = 0
  @serializable dir: 'V' | 'H' | undefined = undefined
  @serializable nOfTags: number = 0
  @serializable(list(primitive())) tags: string[] = []
}

class Slide {
  @serializable idx: number = 0
  @serializable nOfTags: number = 0
  @serializable(list(primitive())) tags: string[] = []
  @serializable pictures: number[] = []
  used: boolean = false

  constructor (pictures: Picture[], idx: number) {
    this.tags = pictures.length === 1 ? pictures[0].tags : _.union(pictures[0].tags, pictures[1].tags)
    this.nOfTags = this.tags.length
    this.pictures = pictures.map(p => p.idx)
    this.idx = idx
  }
}

async function readFile (filename: string) {
  let idx = 0
  let slideIdx = 0
  let verticalSlidesTmp: Picture[] = []
  const slides: Slide[] = []
  const data = fs.createReadStream(filename)
                  .pipe(es.split())
                  .pipe(es.mapSync((line: any) => {
                    const arr = line.split(' ')
                    if (arr.length !== 1) {
                      const pic = deserialize(Picture, { idx, dir: arr[0], nOfTags: parseInt(arr[1]), tags: arr.slice(2) })
                      if (pic.dir === 'V') {
                        verticalSlidesTmp.push(pic)
                        if (verticalSlidesTmp.length === 2) {
                          slides.push(new Slide(verticalSlidesTmp, slideIdx))
                          verticalSlidesTmp = []
                          slideIdx += 1
                        }
                      } else {
                        slides.push(new Slide([pic], slideIdx))
                        slideIdx += 1
                      }
                      idx += 1
                    }
                  })
                  .on('error', function(err) {
                      console.log('Error while reading file.', err);
                  })
                  .on('end', function() {
                      // console.log('Read entire file.')
                  }))

  await getStream(data)
  return slides
}

function writeTofile (output: fs.WriteStream, line: number | Slide) {
  if (line instanceof Slide) output.write(_.join(line.pictures, ' ') + '\n')
  else output.write(`${line}\n`)
}

function getScore (tags1: string[], tags2: string[]) {
  const intersection = _.intersection(tags1, tags2).length
  const s0 = _.difference(tags1, tags2).length
  const s1 = _.difference(tags1, tags2).length
  return Math.min(intersection, s0, s1)
}

async function main (filename: string) {
  const input = await readFile('./files/' + filename)
  let inputSorted = _.sortBy(input, ['nOfTags'])
  inputSorted.reverse()

  const tags: {[key: string]: number[]} = {}
  
  const output = fs.createWriteStream('./out/' + filename.slice(0, -3) + '.out', {
    flags: 'a' // 'a' for appending
  })
  writeTofile(output, input.length)

  for (let i = 0; i < inputSorted.length; i++) {
    for (const tag of inputSorted[i].tags) {
      if (tags[tag]) tags[tag].push(inputSorted[i].idx)
      else tags[tag] = [inputSorted[i].idx]
    }
  }

  const tagsSorted = Object.keys(tags).sort(function(a, b) {return tags[b].length - tags[a].length})

  const slideShow: Slide[] = []
  for (const tag of tagsSorted) {
    const indices = tags[tag]
    for (const idx of indices) {
      if (!(input[idx].used)) {
        slideShow.push(input[idx])
        input[idx].used = true
      } 
    }
  }

  let totalScore = 0  
  for (let i = 0; i < slideShow.length - 1; i++) {
    const score = getScore(slideShow[i].tags, slideShow[i + 1].tags)
    totalScore += score
    writeTofile(output, slideShow[i])
  }
  writeTofile(output, slideShow[slideShow.length - 1])

  console.log(totalScore, slideShow.length, filename)
}

const files = fs.readdirSync('./files');
for (const file of files) {
  main(file)
}


