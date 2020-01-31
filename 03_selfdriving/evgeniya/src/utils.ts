import fs from 'fs'
import es from 'event-stream'
import getStream from 'get-stream'
import { serializable, list, primitive, deserialize } from 'serializr'
import _ from 'lodash'

export class Simulation {
  @serializable rows: number = 0
  @serializable columns: number = 0
  @serializable vehicles: number = 0
  @serializable rides: number = 0
  @serializable bonus: number = 0
  @serializable steps: number = 0
}

export class Ride {
  @serializable id: number = 0
  @serializable(list(primitive())) startPos: number[] = []
  @serializable(list(primitive())) endPos: number[] = []
  @serializable earliestStart: number = 0
  @serializable latestFinish: number = 0
  assigned: boolean = false
  started: number = 0
  willFinish: number = 0

  get length () {
    return Math.abs(this.endPos[0] - this.startPos[0]) + Math.abs(this.endPos[1] - this.startPos[1])
  }

  get latestStart () {
    return this.latestFinish - this.length
  }
}

export class Vehicle {
  @serializable id: number = 1
  @serializable(list(primitive())) currentPos: number[] = [0, 0]
  // @serializable status: number = 0 // 0 - free, 1 - busy
  // nextRide: number | undefined = undefined
  // currentRide: number | undefined = undefined
  rides: number[] = []

  constructor (id: number) {
    this.id = id
  }
}

export function getDistance (pos1: number[], pos2: number[]) {
  return Math.abs(pos2[0] - pos1[0]) + Math.abs(pos2[1] - pos2[1])
}

export function getScore (ride1: Ride | null, ride2: Ride, bonus = 0, steps: number) {
  let score = 0
  // when ride2 can start
  let canStart = ride1 ? ride1.willFinish + getDistance(ride1.endPos, ride2.startPos) : getDistance([0, 0], ride2.startPos)
  if (canStart > ride2.latestStart) {
    return 0
  } else {
    if (canStart <= ride2.earliestStart) {
      canStart = ride2.earliestStart
      // console.log('got bonus of', bonus)
      score += bonus
    } 
    if (canStart + ride2.length > steps) {
      return 0
    } else {
      score += ride2.length
    }
  }

  return score
}

export async function readFile (filename: string) {
  let idx = 0
  let sim: Simulation = new Simulation()
  // const rides: {[key: string]: Ride } = {}
  const rides: Ride[] = []
  const data = fs.createReadStream(filename)
                  .pipe(es.split())
                  .pipe(es.mapSync((line: any) => {
                    const arr = line.split(' ').map((char: any) => Number(char))
                    if (idx == 0) {
                      sim = deserialize(Simulation, {rows: arr[0], columns: arr[1], vehicles: arr[2], rides: arr[3], bonus: arr[4], steps: arr[5]})
                    } else {
                      if (arr.length > 1) {
                        const ride = deserialize(Ride, {id: idx - 1, startPos: [arr[0], arr[1]], endPos: [arr[2], arr[3]], earliestStart: arr[4], latestFinish: arr[5]})
                        // rides[ride.id] = ride
                        rides.push(ride)
                      }
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
  return { sim, rides }
}

export function writeTofile (output: fs.WriteStream, line: Vehicle) {
  output.write(`${line.rides.length} ${line.rides.join(' ')}`)
}
