// ADR-007 acceptance criteria 1, 2 and 5, with no dependencies: `npm test`.
import { readFileSync, readdirSync, existsSync } from 'node:fs'
import { join } from 'node:path'

const failures = []
const tokens = 'src/prodigy-tokens.css'
const gov = '../project-gov/resources/ui-kit/prodigy-tokens.css'
const normalise = (text) => text.replace(/\r\n/g, '\n')

// 1. The tokens are the governance repository's, verbatim.
if (existsSync(gov)) {
  if (normalise(readFileSync(tokens, 'utf8')) !== normalise(readFileSync(gov, 'utf8')))
    failures.push(`${tokens} differs from ${gov}: copy it again`)
} else {
  console.log(`skip: ${gov} not found (clone project-gov beside this repository)`)
}

// 2. No raw colour values outside the tokens file.
const raw = /#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?)\(/
for (const name of readdirSync('src')) {
  const path = join('src', name)
  if (path.replace(/\\/g, '/') === tokens) continue
  readFileSync(path, 'utf8').split('\n').forEach((line, i) => {
    if (raw.test(line)) failures.push(`${path}:${i + 1}: raw colour value; use a token`)
  })
}

// 5. The runtime dependencies are react and react-dom, nothing else.
const deps = Object.keys(JSON.parse(readFileSync('package.json', 'utf8')).dependencies ?? {}).sort()
if (deps.join() !== 'react,react-dom') failures.push(`runtime dependencies are ${deps.join(', ')}; ADR-007 allows react, react-dom`)

if (failures.length) {
  failures.forEach((f) => console.error(`FAIL ${f}`))
  process.exit(1)
}
console.log('ok: tokens match, no raw colours, dependencies within budget')
