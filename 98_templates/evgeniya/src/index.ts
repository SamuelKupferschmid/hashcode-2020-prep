import { readFile, writeTofile } from "./utils"
import fs from 'fs'

async function main (filename: string) {
  const input = await readFile('../../input/' + filename)

  // const output = fs.createWriteStream('../../output/' + filename.slice(0, -4) + '_evgeniya.out', {
  //   flags: 'a' // 'a' for appending
  // })
  // writeTofile(output, input.length)
}

const files = fs.readdirSync('../../input/');
for (const file of files) {
  main(file)
}