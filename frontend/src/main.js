import './app.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import App from './App.svelte'

const app = new App({
  target: document.getElementById('app'),
  headers: {
    'Access-Control-Allow-Origin': '*' // or, e.g. replacing * by http://localhost:8000
  }
})

export default app
