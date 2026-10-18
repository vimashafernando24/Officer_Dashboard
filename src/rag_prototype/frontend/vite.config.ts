import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import type { Plugin } from 'vite'

/**
 * The generated comparison-data loaders use `import(json, { with: { type: "json" } })`
 * so Node's test runner can load the data. The dev server serves JSON as a JavaScript
 * module but keeps the attribute on dynamic imports, which browsers then reject.
 * Production builds already handle it, so the attribute is removed in dev only.
 */
function comparisonLoadersDevFix(): Plugin {
  return {
    name: 'comparison-loaders-dev-json-attribute',
    apply: 'serve',
    transform(code, id) {
      if (!id.endsWith('/src/data/comparisonDataLoaders.ts')) return null
      return code.replaceAll(', { with: { type: "json" } })', ')')
    },
  }
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), comparisonLoadersDevFix()],
})
