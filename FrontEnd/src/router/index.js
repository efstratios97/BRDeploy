import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'
import DataManager from '../views/DataManager.vue'
import UserManager from '../views/UserManager.vue'
import Cleanser from '../views/Cleanser.vue'
import DataAnalyzer from '../views/DataAnalyzer.vue'
import DataHealthManager from '../views/DataHealthManager.vue'
import GoToMenuBack from '../components/GoToMenuBack.vue'
import DashboardDataHealth from '../components/DashboardDataHealth.vue'
import DashboardAnalyzer from '../components/DashboardAnalyzer.vue'
import SelectorDataset from '../components/SelectorDataset.vue'
import Login from '../views/Login.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    components: { default: Login }
  },
  {
    path: '/mainmenu',
    name: 'Home',
    components: { default: Home }
  },
  {
    path: '/datamanager',
    name: 'DataManager',
    components: { default: DataManager, header: GoToMenuBack }
  },
  {
    path: '/usermanager',
    name: 'UserManager',
    components: { default: UserManager, header: GoToMenuBack }
  },
  {
    path: '/cleanser',
    name: 'Cleanser',
    components: { default: Cleanser, header: GoToMenuBack }
  },
  {
    path: '/dataanalyzer',
    name: 'DataAnalyzer',
    components: { default: DataAnalyzer, header: GoToMenuBack }
  }, {
    path: '/dataanalyzer/',
    name: 'SelectorDatasetA',
    components: { default: DataAnalyzer, header: GoToMenuBack },
    children: [{
      path: '',
      components: { default: SelectorDataset, header: GoToMenuBack },

    }, {
      path: '/dataanalyzer/dashboard',
      name: 'DataAnalyzerDashboard',
      components: { default: DashboardAnalyzer, header: GoToMenuBack },
    }]
  },

  {
    path: '/datahealthmanager',
    name: 'DataHealthManager',
    components: { default: DataHealthManager, header: GoToMenuBack }
  },
  {
    path: '/datahealthmanager/',
    name: 'SelectorDatasetH',
    components: { default: DataHealthManager, header: GoToMenuBack },
    children: [{
      path: '',
      components: { default: SelectorDataset, header: GoToMenuBack },

    }, {
      path: '/DataHealthManager/dashboard',
      name: 'DataHealthDashboard',
      components: { default: DashboardDataHealth, header: GoToMenuBack },
    }]
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
