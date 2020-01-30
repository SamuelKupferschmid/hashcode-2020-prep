import fs from 'fs'
import _ from 'lodash'
import { readFile, writeTofile, Slide, scale, swap } from './helpers'

let SCORES: any = []

function getScore (tags1: string[], tags2: string[]) {
  const intersection = _.intersection(tags1, tags2).length
  const s0 = _.difference(tags1, tags2).length
  const s1 = _.difference(tags1, tags2).length
  return Math.min(intersection, s0, s1)
}

function getTotalScore(slideShow: Slide []){
  let totalScore = 0
  for (let i = 0; i < slideShow.length - 1; i++) {
    let idx1 = slideShow[i].idx
    let idx2 = slideShow[i + 1].idx
    let score = SCORES.length > idx1 && SCORES[idx1].length > idx2 ? SCORES[idx1][idx2] : 0
    if (!score) {
      score = getScore(slideShow[i].tags, slideShow[i + 1].tags)
      SCORES[idx1][idx2] = score
      SCORES[idx2][idx1] = score
    }
    totalScore += score
  }
  return totalScore
}

async function main (filename: string) {
  const input = await readFile('./files/' + filename)
  let inputSorted = _.sortBy(input, ['nOfTags'])
  inputSorted.reverse()

  const tags: {[key: string]: number[]} = {}
  
  const output = fs.createWriteStream('./out/' + filename.slice(0, -3) + 'out', {
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
    if (indices.length === 1) {
      continue
    } else {
      for (const idx of indices) {
        if (!(input[idx].used)) {
          slideShow.push(input[idx])
          input[idx].used = true
        } 
      }
    }
  }

  // let totalScore = 0  
  // for (let i = 0; i < slideShow.length - 1; i++) {
  //   const score = getScore(slideShow[i].tags, slideShow[i + 1].tags)
  //   totalScore += score
  //   writeTofile(output, slideShow[i])
  // }
  // writeTofile(output, slideShow[slideShow.length - 1])

  // console.log(totalScore, slideShow.length, filename)
  return slideShow
}

async function main1 (filename: string) {
  // slides
  const slideShow: Slide[] = []
  const slides: Slide[] = await main(filename)
  for (let i = 0; i < slides.length; i++) {
    SCORES.push([])
    for (let j = 0; j < slides.length; j++) {
      SCORES[i].push(0)
    }
  }

  // best score
  let recordScore = 0
  let bestEver: SlideShow | undefined = undefined

  
  // population of possible orders
  let population: SlideShow[] = []
  const popTotal = 50

  for (let j = 0; j < popTotal; j++) {
    if (j === 0) {
      population[0] = new SlideShow(slides.length, slides.map((s, i) => i))
      for (let i = 1; i < 1000; i++) {
        population[i] = new SlideShow (slides.length, undefined)
      }
    }
    let minScore = Infinity
    let maxScore = 0
    for (let i = 0; i < population.length; i++) {
    
      const ss = population[i].slidesOrder.map(p => slides[p])
      let score = getTotalScore(ss)
      population[i].score = score

      if (score > recordScore) {
        recordScore = score
        bestEver = population[i]
      }

      if (score > maxScore) {
        maxScore = score
      }

      if (score < minScore) { 
        minScore = score
      }
    }

    console.log('maxScore: ', maxScore)    
    for (let i = 0; i < population.length; i++) {
      population[i].fitness = population[i].mapFitness(minScore, maxScore)
    }

    // new population
    const newPopulation = nextGeneration(population, slides.length)
    population = newPopulation
  }

  console.log(bestEver)
}

function nextGeneration (population: SlideShow[], slidesLength: number) {
  const newPopulation = []
  let count = 0
  for (let i = 0; i < population.length; i++) {
    if (population[i].fitness > 0.5) {
      count += 1
      newPopulation[i] = new SlideShow(slidesLength, population[i].slidesOrder)
    } else {
      newPopulation[i] = new SlideShow(slidesLength, undefined)
    }
  }
  console.log('Passed: ', count)
  return newPopulation
}

class SlideShow {
  slidesOrder: number[] = []
  score: number = 0
  fitness: number = 0

  constructor (nOfSlides: number, slidesOrder?: number[]) {
    if (slidesOrder) {
      this.slidesOrder = slidesOrder.slice()
      // if (Math.random() < 0.5) {
      //   this.slidesOrder = _.shuffle(this.slidesOrder)
      // }
      for (let i = 0; i < 200; i++) {
        const r1 = Math.floor(Math.random() * nOfSlides)
        const r2 = Math.floor(Math.random() * nOfSlides)
        swap(this.slidesOrder, r1, r2)
      }
    } else {
      this.slidesOrder = []
      for (let i = 0; i < nOfSlides; i++) {
        this.slidesOrder[i] = i
      }
  
      for (let i = 0; i < 100; i++) {
        this.slidesOrder = _.shuffle(this.slidesOrder)
      }
    }
  }

  mapFitness (minScore: number, maxScore: number) {
    this.fitness = scale(this.score, minScore, maxScore, 0, 1)
    return this.fitness
  }

  normalizeFitness (nOfSlides: number) {
    this.fitness /= nOfSlides
  }
}

// main1('c_memorable_moments.txt')

const files = fs.readdirSync('../../input');
for (const file of files) {
  main(file)
}


