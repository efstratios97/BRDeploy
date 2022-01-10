import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'
import DataManager from '../views/DataManager.vue'
import UserManager from '../views/UserManager.vue'
import Cleanser from '../views/Cleanser.vue'
import DataAnalyzer from '../views/DataAnalyzer.vue'
import DataHealthManager from '../views/DataHealthManager.vue'
import KPIManager from '../views/KPIManager.vue'
import ExecutiveDashboard from '../views/ExecutiveDashboard.vue'
import GoToMenuBack from '../components/GoToMenuBack.vue'
import DashboardDataHealth from '../components/Dashboards/DashboardDataHealth.vue'
import DashboardAnalyzer from '../components/Dashboards/DashboardAnalyzer.vue'
import DashboardKPI from '../components/Dashboards/DashboardKPI.vue'
import DashboardExecutiveDashboard from '../components/Dashboards/DashboardExecutiveDashboardMockup.vue'
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
    components: { default: Home, header: GoToMenuBack }
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
      path: '/datahealthmanager/dashboard',
      name: 'DataHealthDashboard',
      components: { default: DashboardDataHealth, header: GoToMenuBack },
    }]
  },

  {
    path: '/kpimanager',
    name: 'KPIManager',
    components: { default: KPIManager, header: GoToMenuBack }
  },
  {
    path: '/kpimanager/',
    name: 'SelectorDatasetK',
    components: { default: KPIManager, header: GoToMenuBack },
    children: [{
      path: '',
      components: { default: SelectorDataset, header: GoToMenuBack },

    }, {
      path: '/kpimanager/dashboard',
      name: 'KPIDashboard',
      components: { default: DashboardKPI, header: GoToMenuBack },
    }]
  },

  {
    path: '/executivedashboard',
    name: 'ExecutiveDashboard',
    components: { default: ExecutiveDashboard, header: GoToMenuBack }
  },
  {
    path: '/executivedashboard/',
    name: 'SelectorDatasetE',
    components: { default: ExecutiveDashboard, header: GoToMenuBack },
    children: [{
      path: '',
      name: 'ExecutiveDashboardDashboard',
      components: { default: DashboardExecutiveDashboard, header: GoToMenuBack },
    }]
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
