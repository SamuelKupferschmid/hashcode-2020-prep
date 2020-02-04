import fs from 'fs'
import es from 'event-stream'
import getStream from 'get-stream'
import { serializable, list, primitive, deserialize } from 'serializr'
import _ from 'lodash'

export class Video {
  @serializable id: number = 0
  @serializable size: number = 0
}

export class Endpoint {
  @serializable id: number = 0
  @serializable latToDC: number = 0
  latsToCaches: {[key: string]: number} = {}
}

export class Request {

}

export async function readFile (filename: string) {
  let idx = 0
  let cachelines = 0
  let endpointline = 0
  let requestLine = 0
  const videos: Video[] = []
  const endpoints: Endpoint[] = []
  const requests: Request[] = []
  let caches = 0
  let cacheSize = 0
  const data = fs.createReadStream(filename)
                  .pipe(es.split())
                  .pipe(es.mapSync((line: any) => {
                    const arr = line.split(' ')
                    if (idx === 0) {
                      caches = arr[3]
                      cacheSize = arr[4]
                    }
                    if (idx === 1) {
                      for (let i = 0; i < arr.length; i++) {
                        const v = deserialize(Video, { id: i, size:arr[i] })
                        videos.push(v)
                      }
                    } else {
                      const endpoint = deserialize(Endpoint, {id: endpointline, latToDC: arr[0]})
                      if (cachelines) cachelines = arr[1]
                      endpointline += 1
                    
                      // for (let j = 0; j < lats.length; j++) {
                      //   endpoint.latsToCaches[]
                      // }
                    }
                      idx += 1
                  })
                  .on('error', function(err) {
                      console.log('Error while reading file.', err);
                  })
                  .on('end', function() {
                      // console.log('Read entire file.')
                  }))

  await getStream(data)
  return { videos, endpoints, requests, caches, cacheSize}

export function writeTofile (output: fs.WriteStream, line: number | Slide) {
  if (line instanceof Slide) output.write(_.join(line.pictures, ' ') + '\n')
  else output.write(`${line}\n`)
}
