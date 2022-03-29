import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'
import DataManager from '../views/DataManager.vue'
import UserManager from '../views/UserManager.vue'
import Cleanser from '../views/Cleanser.vue'
import DataAnalyzer from '../views/DataAnalyzer.vue'
import DataHealthManager from '../views/DataHealthManager.vue'
import KPIManager from '../views/KPIManager.vue'
import ExecutiveDashboardManager from '../views/ExecutiveDashboardManager.vue'
import ExecutiveDashboard from '../views/ExecutiveDashboard.vue'
import DefaultNavBar from '../components/NavBar/DefaultNavBar.vue'
import AdminNavBar from '../components/NavBar/AdminNavBar.vue'
import UserNavBar from '../components/NavBar/UserNavBar.vue'
import DashboardDataHealth from '../components/Dashboards/DashboardDataHealth.vue'
import DashboardAnalyzer from '../components/Dashboards/DashboardAnalyzer.vue'
import DashboardKPI from '../components/Dashboards/DashboardKPI.vue'
import DashboardExecutiveDashboard from '../components/Dashboards/DashboardExecutiveDashboard.vue'
import DashboardExecutiveDashboardManager from '../components/Dashboards/DashboardExecutiveDashboardManager.vue'
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
    components: { default: Home, header: DefaultNavBar }
  },
  {
    path: '/mainmenu-landing-u',
    name: 'Home-U',
    components: { default: Home, header: UserNavBar }
  },
  {
    path: '/mainmenu-landing-a',
    name: 'Home-A',
    components: { default: Home, header: AdminNavBar }
  },
  {
    path: '/datamanager',
    name: 'DataManager',
    components: { default: DataManager, header: DefaultNavBar }
  },
  {
    path: '/usermanager',
    name: 'UserManager',
    components: { default: UserManager, header: DefaultNavBar }
  },
  {
    path: '/cleanser',
    name: 'Cleanser',
    components: { default: Cleanser, header: DefaultNavBar }
  },
  {
    path: '/dataanalyzer',
    name: 'DataAnalyzer',
    components: { default: DataAnalyzer, header: DefaultNavBar }
  }, {
    path: '/dataanalyzer/',
    name: 'SelectorDatasetA',
    components: { default: DataAnalyzer, header: DefaultNavBar },
    children: [{
      path: '',
      components: { default: SelectorDataset, header: DefaultNavBar },

    }, {
      path: '/dataanalyzer/dashboard',
      name: 'DataAnalyzerDashboard',
      components: { default: DashboardAnalyzer, header: DefaultNavBar },
    }]
  },

  {
    path: '/datahealthmanager',
    name: 'DataHealthManager',
    components: { default: DataHealthManager, header: DefaultNavBar }
  },
  {
    path: '/datahealthmanager/',
    name: 'SelectorDatasetH',
    components: { default: DataHealthManager, header: DefaultNavBar },
    children: [{
      path: '',
      components: { default: SelectorDataset, header: DefaultNavBar },

    }, {
      path: '/datahealthmanager/dashboard',
      name: 'DataHealthDashboard',
      components: { default: DashboardDataHealth, header: DefaultNavBar },
    }]
  },

  {
    path: '/kpimanager',
    name: 'KPIManager',
    components: { default: KPIManager, header: DefaultNavBar }
  },
  {
    path: '/kpimanager/',
    name: 'SelectorDatasetK',
    components: { default: KPIManager, header: DefaultNavBar },
    children: [{
      path: '',
      components: { default: SelectorDataset, header: DefaultNavBar },

    }, {
      path: '/kpimanager/dashboard',
      name: 'KPIDashboard',
      components: { default: DashboardKPI, header: DefaultNavBar },
    }]
  },
  {
    path: '/executivedashboardmanager',
    name: 'ExecutiveDashboardManager',
    components: { default: ExecutiveDashboardManager, header: DefaultNavBar }
  },
  {
    path: '/executivedashboardmanager/',
    name: 'ExecutiveDashboardManagerDashboard',
    components: { default: ExecutiveDashboardManager, header: DefaultNavBar },
    children: [{
      path: '',
      name: 'ExecutiveDashboardManagerDashboardC',
      components: { default: DashboardExecutiveDashboardManager, header: DefaultNavBar },
    }]
  },
  {
    path: '/executivedashboard',
    name: 'ExecutiveDashboard',
    components: { default: ExecutiveDashboard, header: DefaultNavBar }
  },
  {
    path: '/executivedashboard/',
    name: 'ExecutiveDashboardC',
    components: { default: ExecutiveDashboard, header: DefaultNavBar },
    children: [{
      path: '',
      name: 'ExecutiveDashboardDashboardC',
      components: { default: DashboardExecutiveDashboard, header: DefaultNavBar },
    }]
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
