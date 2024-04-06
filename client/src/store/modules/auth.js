import authService from '@/api';

const state = {
  user: {},
  isLoggedIn: false,
};

/* eslint no-shadow: ["error", { "allow": ["state"] }] */
const getters = {
  isLoggedIn: (state) => state.isLoggedIn,
  user: (state) => state.user,
};

const actions = {
  async registerUser({ dispatch }, user) {
    await authService.post('api/auth/register', user);
    await dispatch('fetchUser');
  },
  async loginUser({ dispatch }, user) {
    console.log('in loginuser');
    await authService.post('api/auth/login', user).then(async (response) => {
      if (response.status !== 201) {
        throw Error(response.status);
      }
      await dispatch('fetchUser');
    }).catch(async (error) => {
      console.log('Error Authenticating', error);
      await dispatch('logoutUser');
    });
  },
  async fetchUser({ commit }) {
    await authService.get('api/auth/user')
      .then(({ data }) => {
        console.log(data);
        commit('setUser', data);
      });
  },
  async logoutUser({ commit }) {
    await authService.post('api/auth/logout');
    commit('logoutUserState');
  },
};

const mutations = {
  setUser(state, user) {
    state.isLoggedIn = true;
    state.user = user;
  },
  logoutUserState(state) {
    state.isLoggedIn = false;
    state.user = {};
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
