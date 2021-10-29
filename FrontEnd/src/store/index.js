import { createStore } from "vuex"


const state = {
    loggedUser: null,
    token: null
}

const mutations = {
    setLoggedUser(state, user_id) {
        state.loggedUser = user_id;
    },
    setToken(state, token) {
        state.token = token;
    }
}

const getters = {
    getLoggedUser(state) {
        return state.loggedUser;
    },
    getToken(state) {
        return state.token;
    }
}

export default createStore({
    state,
    mutations,
    getters
})