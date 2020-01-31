import { readFile, writeTofile, Ride, Simulation, Vehicle, getScore, getDistance } from "./utils"
import fs from 'fs'
import _ from "lodash"

async function main (filename: string) {
  const input = await readFile('../../input/' + filename)

  const sim: Simulation | undefined = input.sim
  const rides = _.sortBy(input.rides, ['earliestStart']) //removed by length
  const ridesDict: {[key: string]: Ride} = rides.reduce((map: {[key: string]: Ride}, obj) => ( map[obj.id] = obj, map ), {})
  // console.log(ridesDict)
  // console.log(rides)
  const vehicles: Vehicle[] = []
  let totalScore = 0

  if (sim && rides) {
    for (let i = 0; i < sim.vehicles; i++) {
      // vehicles[`${i + 1}`] = new Vehicle(i + 1)
      vehicles.push(new Vehicle(i))
    }
    while (rides.length) {
      const r = rides.shift()
      if (!r) break
      for (const v of vehicles) {
        const lastRide = v.rides.length ? ridesDict[v.rides[v.rides.length - 1]] : null
        const potentialScore = getScore(lastRide, r, sim.bonus, sim.steps)
        if (potentialScore) {
          // console.log('potScore', potentialScore)
          v.rides.push(r.id)
          r.started = lastRide ? lastRide.willFinish + getDistance(lastRide.endPos, r.startPos) : getDistance([0, 0], r.startPos)
          r.willFinish = r.started + r.length
          totalScore += potentialScore
          break
        }
      }
    }
  }



  const output = fs.createWriteStream('../../output/' + filename.slice(0, -3) + `_${totalScore}` + '_evgeniya.out', {
    flags: 'a' // 'a' for appending
  })
  for (const v of vehicles) {
    writeTofile(output, v)
  }
  

  // console.log('Vehicles: ', vehicles)
  console.log('Score: ', totalScore)
}

// main('a_example.in')
// main('b_should_be_easy.in')
// main('c_no_hurry.in')
// main('d_metropolis.in')
// main('e_high_bonus.in')

const files = fs.readdirSync('../../input/');
for (const file of files) {
  main(file)
}