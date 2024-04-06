import Vue from 'vue';
import App from './App.vue';
import TodayComponent from './components/TodayComponent.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import store from './store';

Vue.config.productionTip = false;
Vue.component('today-component', TodayComponent);

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
