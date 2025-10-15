import { mount } from 'svelte'
import './app.css'
import App from './App.svelte'

/**
 * @type {import('svelte').SvelteComponent}
 */
const app = mount(App, {
  target: /** @type {HTMLElement} */ (document.getElementById('app')),
})

export default app
