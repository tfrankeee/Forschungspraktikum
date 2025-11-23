import Vue from 'vue'
import App from './App.vue'
import router from './router'

import { TestService } from '@/helpers/TestService'

Vue.config.productionTip = false

const testService = new TestService()

async function bootstrap() {
  // Dateinamen angeben, die unter public/qti/tests liegen
  const filenames = [
    'test1.xml',
    'test2.xml',
    'cloud_computing_test.xml'
    // ..alle anderen QTI-XMLs
  ]

  await testService.loadAllTests(filenames)

  Vue.prototype.$testService = testService

  new Vue({
    router,
    render: h => h(App)
  }).$mount('#app')
}

bootstrap()
