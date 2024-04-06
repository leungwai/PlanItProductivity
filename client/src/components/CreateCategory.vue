<template>
  <v-container fluid class="lime lighten-5 fill-height">
    <v-row class="wrap justify-center">
      <today-component></today-component>

      <v-col md="8" sm="8">
        <v-form @submit="onSubmit">
          <v-card class="rounded-lg pt-3" height="91vh" style="overflow-y:scroll">
            <v-row>
              <v-col>
                <v-card-title class="ml-6 mb-3 mt-5 display-2 font-weight-bold"
                  >Create Category</v-card-title
                >
              </v-col>
            </v-row>

            <v-row class="name justify-center">
              <v-col sm="1" md="1" class="my-auto">
                <v-icon class="ma-auto" x-large>
                  mdi-pencil
                </v-icon>
              </v-col>

              <v-col sm="8" md="8" class="my-auto">
                <v-text-field
                  id="input-1"
                  v-model="form.name"
                  placeholder="Enter Category Name"
                  required
                ></v-text-field>
              </v-col>
            </v-row>

          </v-card>
          <v-speed-dial
            class="mr-5 mb-5"
            v-model="fab"
            absolute
            bottom
            right
            slide-y-reverse-transition
          >
            <template v-slot:activator>
              <v-btn v-model="fab" color="green darken-2" dark fab>
                <v-icon v-if="fab"> mdi-close </v-icon>
                <v-icon v-else> mdi-content-save </v-icon>
              </v-btn>
            </template>
            <v-btn fab dark small type="submit" color="green">
              <v-icon>mdi-content-save</v-icon>
            </v-btn>
            <v-btn fab small dark @click="returnHome" color="red">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-speed-dial>
        </v-form>
      </v-col>
    </v-row>

<!--
    <v-row>
      <v-col md="7" sm="7" class="ma-auto">
        <v-card class="mt-3" header="Form Data Result">
          <pre class="m-0">{{ form }}</pre>
        </v-card>
      </v-col>
    </v-row>
    -->
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        name: '',
      },
    };
  },
  methods: {
    onSubmit(event) {
      event.preventDefault();
      const payload = {
        name: this.form.name,
        user_id: this.$store.getters.user.user,
      };
      this.addCategory(payload);
    },
    addCategory(payload) {
      const path = 'api/categories';
      axios
        .post(path, payload)
        .then(() => {
          this.$router.push('/success');
        })
        .catch((error) => {
          console.log(error);
          this.$router.push('/error');
        });
    },
    initForm() {
      this.form.name = '';
    },
    returnHome() {
      this.$router.push('/home');
    },
  },
};
</script>
