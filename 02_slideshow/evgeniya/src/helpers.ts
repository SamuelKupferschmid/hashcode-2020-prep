import fs from 'fs'
import es from 'event-stream'
import getStream from 'get-stream'
import { serializable, list, primitive, deserialize } from 'serializr'
import _ from 'lodash'

// models
export class Picture {
  @serializable idx: number = 0
  @serializable dir: 'V' | 'H' | undefined = undefined
  @serializable nOfTags: number = 0
  @serializable(list(primitive())) tags: string[] = []
}

export class Slide {
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

export async function readFile (filename: string) {
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

export function writeTofile (output: fs.WriteStream, line: number | Slide) {
  if (line instanceof Slide) output.write(_.join(line.pictures, ' ') + '\n')
  else output.write(`${line}\n`)
}

export function swap (arr: any[], i: number, j: number) {
  const tmp = arr[i]
  arr[i] = arr[j]
  arr[j] = tmp
}

export function scale(n: number, in_min: number, in_max: number, out_min: number, out_max: number) {
  // console.log(n, in_min, in_max, out_min, out_max)
  const result = (n - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
  // console.log(result)
  return result
}