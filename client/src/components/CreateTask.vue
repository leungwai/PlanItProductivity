<template>
  <v-container fluid class="purple lighten-5 fill-height">
    <v-row class="wrap justify-center fill-height">
      <today-component class="hidden-xs-only"></today-component>

      <v-col md="8" sm="8">
        <v-form @submit="onSubmit" v-if="show" ref="form" v-model="valid" lazy-validation>
          <v-card class="rounded-lg pt-3" height="91vh" style="overflow-y:scroll">
            <v-row>
              <!--Title/Heading-->
              <v-col>
                <v-card-title class="ml-10 mb-3 mt-5 display-2 font-weight-bold"
                  >Create Task</v-card-title
                >
              </v-col>
              <v-spacer></v-spacer>
              <!--Cancel Button-->
              <v-btn
                  class="mt-9 mr-11 pa-0"
                  @click="returnHome"
                  min-width=0
                  height=36
                  width=36
                  color="red"
                  dark
                >
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </v-row>

            <!--Task Name-->
            <v-row class="name justify-center">
              <v-spacer></v-spacer>
              <v-col sm="1" md="1" class="my-auto">
                <v-icon class="ma-auto" x-large>
                  mdi-pencil
                </v-icon>
              </v-col>

              <v-col sm="8" md="8" class="my-auto">
                <v-text-field
                  id="input-1"
                  v-model="form.name"
                  :rules="nameRules"
                  :counter="50"
                  placeholder="Enter Task Name"
                  required
                ></v-text-field>
              </v-col>
              <v-spacer></v-spacer>
            </v-row>

            <!--Subcategory Selector-->
            <v-row class="subcategory justify-center">
              <v-spacer></v-spacer>
              <v-col sm="1" md="1">
                <v-icon class="mt-2" x-large>
                  mdi-format-list-bulleted-type
                </v-icon>
              </v-col>

              <v-col sm="8" md="8">
                <v-select
                  v-model="form.subcategory"
                  :items="subcategories"
                  :rules="subcatRules"
                  placeholder="Select Subcategory"
                  require
                  filled
                ></v-select>
              </v-col>
              <v-spacer></v-spacer>
            </v-row>

            <!--Date Picker-->
            <v-row class="date justify-center mt-n4">
              <v-spacer></v-spacer>
              <v-col sm="1" md="1">
                <v-icon class="mt-2" x-large> mdi-calendar </v-icon>
              </v-col>

              <v-col sm="8" md="8">
                <v-menu
                  v-model="menu2"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                  min-width="auto"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="form.date"
                      label="Select Date"
                      :rules="dateRules"
                      readonly
                      require
                      filled
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </template>

                  <v-date-picker
                    v-model="form.date"
                    @input="menu2 = false"
                  ></v-date-picker>
                </v-menu>
              </v-col>
              <v-spacer></v-spacer>
            </v-row>

            <!--Start Time-->
            <v-row class="start_time justify-center mt-n4">
              <v-spacer></v-spacer>
              <v-col sm="1" md="1">
                <v-icon class="mt-2" x-large>
                  mdi-clock-time-four-outline
                </v-icon>
              </v-col>
              <v-col sm="8" md="8">
                <v-menu
                  v-model="menu3"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                  min-width="auto"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="form.start_time"
                      label="Select Start Time"
                      :rules="startTimeRules"
                      filled
                      readonly
                      require
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </template>
                  <v-time-picker
                    v-model="form.start_time"
                    header-color="primary"
                    @input="menu3 = false"
                  ></v-time-picker>
                </v-menu>
              </v-col>
              <v-spacer></v-spacer>
            </v-row>

            <!--Duration-->
            <v-row class="duration justify-center mt-n4">
              <v-spacer></v-spacer>
              <v-col sm="1" md="1">
                <v-icon class="mt-2" x-large> mdi-timer-cog-outline </v-icon>
              </v-col>

              <v-col sm="8" md="8">
                <v-text-field
                  id="input-1"
                  v-model="form.duration"
                  :rules="durationRules"
                  placeholder="Enter Duration in Minutes"
                  filled
                  required
                ></v-text-field>
              </v-col>
              <v-spacer></v-spacer>
            </v-row>

            <!--Details-->
            <v-row class="details justify-center mt-n4">
              <v-spacer></v-spacer>
              <v-col sm="1" md="1">
                <v-icon class="mt-2" x-large>
                  mdi-clipboard-edit-outline
                </v-icon>
              </v-col>

              <v-col sm="8" md="8">
                <v-textarea
                  id="input-7"
                  v-model="form.details"
                  placeholder="Enter Details"
                  filled
                ></v-textarea>
              </v-col>
              <v-spacer></v-spacer>
            </v-row>
          </v-card>

          <!--Submit Button-->
          <v-expand-x-transition>
            <v-btn x-large rounded class="ma-6" type="submit" color="green darken-2" dark
              absolute
              bottom
              right
              elevation="10"
              v-show="valid"
              >
                <v-icon class="mr-2">mdi-content-save</v-icon>
                Save New Task
            </v-btn>
          </v-expand-x-transition>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        name: '',
        subcategory: '',
        date: '',
        duration: '',
        start_time: '',
        details: '',
      },
      nameRules: [
        (v) => !!v || 'Name is required',
        (v) => (v && v.length <= 50) || 'Name must be less than 50 characters',
      ],
      subcatRules: [
        (v) => !!v || 'Must select a subcategory',
      ],
      dateRules: [
        (v) => !!v || 'Must choose a valid date',
      ],
      startTimeRules: [
        (v) => !!v || 'Must set a start time',
      ],
      durationRules: [
        (v) => !!v || 'Must set a duration',
      ],
      subcategories: [
        { text: 'Select One', value: null },
        this.getSubcategories(),
      ],
      show: true,
      fab: false,
      valid: false,
      menu2: false,
      menu3: false,
    };
  },
  methods: {
    onSubmit(event) {
      event.preventDefault();
      const payload = {
        name: this.form.name,
        user_id: this.$store.getters.user.user,
        subcategory_id: this.form.subcategory,
        date: this.form.date,
        start_time: this.form.start_time,
        duration: Number(this.form.duration),
        details: this.form.details,
      };
      this.addTask(payload);

      // this.$router.push('/success');
      // this.initForm();
    },
    getTasks() {
      const path = 'api/tasks';
      axios
        .get(path)
        .then((res) => {
          this.tasks = res.data.name;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    addTask(payload) {
      const path = 'api/tasks';
      axios
        .post(path, payload)
        .then(() => {
          this.getTasks();
          this.$router.push('/home');
        })
        .catch((error) => {
          console.log(error);
          this.getTasks();
          this.$router.push('/error');
        });
    },
    getSubcategories() {
      const path = `api/subcategoriesNameId/${this.$store.getters.user.user}`;
      axios
        .get(path)
        .then((res) => {
          const subcat = res.data.data.subcategories;
          this.subcategories = Object.keys(subcat).map((k) => subcat[k]);
          console.log(this.subcategories);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    initForm() {
      this.form.name = '';
      this.form.subcategory = null;
      this.form.date = '';
      this.form.duration = '';
      this.form.start_time = '';
      this.form.details = '';
    },
    returnHome() {
      this.$router.push('/home');
    },
    validate() {
      this.$refs.form.validate();
    },
  },
};
</script>
