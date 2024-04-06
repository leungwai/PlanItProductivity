<template>
<v-app>
<v-app-bar
      absolute
      color="deep-purple accent-2"
      dark
      prominent
      extended="true"
      extension-height="64px"
    >
    <v-col>
      <v-row class="no-gutters mt-3">
        <v-spacer></v-spacer>
          <v-img
            src="@/assets/planitLogo_white_fullsize.png"
            max-width="300"
          ></v-img>
        <v-spacer></v-spacer>
      </v-row>
      <v-row class="headline">
        <v-spacer></v-spacer>
          <v-app-bar-text align="center">
            Because your world should revolve around you</v-app-bar-text>
        <v-spacer></v-spacer>
      </v-row>
    </v-col>
    </v-app-bar>
  <v-container fluid class="purple lighten-5 fill-height">
    <v-row class="wrap">
      <v-col md="5" sm="7" class="ma-auto">
        <v-alert
          v-if="show"
          color="red"
          type="error"
          outlined
          dark
          class="ma-auto mb-2"
        >
          {{ alert_message }}
        </v-alert>
        <v-card class="rounded-lg pt-3">
          <v-card-title class="mb-3 justify-center display-3 display-2"
            >Login</v-card-title
          >
          <v-form @submit="onSubmit">
            <v-row class="username">
              <v-col sm="8" md="8" class="ma-auto">
                <v-text-field
                  class="rounded-lg"
                  id="input-1"
                  v-model="form.username"
                  label="Username"
                  outlined
                  required
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row class="password">
              <v-col sm="8" md="8" class="ma-auto">
                <v-text-field
                  class="mt-n5 rounded-lg"
                  id="input-2"
                  v-model="form.password"
                  type="password"
                  label="Password"
                  outlined
                  required
                ></v-text-field>
              </v-col>
            </v-row>

            <v-row>
              <v-card-actions class="ma-auto mt-n5 mb-5">
                <v-col class="justify-start">
                  <v-btn plain color="blue" @click="goRegister"
                    >Create User</v-btn
                  >
                </v-col>
                <v-col class="justify-end">
                  <v-btn color="green" dark type="submit" variant="primary"
                    >Login</v-btn
                  >
                </v-col>
              </v-card-actions>
            </v-row>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
  </v-app>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  // APP_URL: process.env.VUE_APP_URL,
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
      show: false,
      alert_message: '',
    };
  },
  computed: {
    ...mapGetters(['user', ['/user']]),
    user: {
      get() {
        return this.$store.user;
      },
      set(user) {
        return user;
      },
    },
  },
  methods: {
    onSubmit(event) {
      event.preventDefault();
      const payload = {
        username: this.form.username,
        password: this.form.password,
      };
      this.login(payload);
      this.initForm();
    },
    ...mapActions(['loginUser', 'logoutUser']),
    async login(payload) {
      await this.loginUser(payload).then(() => {
        if (this.$store.getters.isLoggedIn) {
          this.$router.push('/home');
        } else {
          console.log('authenticationfailed');
          this.$router.push('/login');
          this.user = {
            username: null,
            password: null,
          };
          this.show = true;
          this.alert_message = 'Unable to log in! Please check credentials again!';
        }
      });
    },
    goRegister() {
      this.$router.push('/register');
    },
    initForm() {
      this.form.username = '';
      this.form.password = '';
    },
  },
  async mounted() {
    await this.logoutUser();
  },
};
</script>
