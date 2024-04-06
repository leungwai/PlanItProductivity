<template>
  <v-container fluid class="purple lighten-5 fill-height">
    <v-row class="wrap justify-center">
      <today-component></today-component>

      <v-col md="8" sm="8">
        <v-form @submit="onSubmit" v-if="show" ref="form" v-model="valid" lazy-validation>
          <v-card
            class="rounded-lg pt-3"
            height="91vh"
            style="overflow-y: scroll"
          >
            <v-row>
              <v-col>
                <v-card-title
                  class="pa-0 ml-14 mb-3 mt-5 display-2 font-weight-bold"
                >
                <v-text-field
                  class="text-h4"
                  id="input-1"
                  v-model="form.name"
                  :rules="nameRules"
                  :counter="50"
                ></v-text-field>
                </v-card-title>
              </v-col>
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

            <!--Subcategory Selector-->
            <v-row class="subcategory justify-center">
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
                  transition="slide-y-transition"
                  persistent-hint
                  require
                  filled
                ></v-select>
              </v-col>
            </v-row>

            <!--Date Selector-->
            <v-row class="date justify-center mt-n4">
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
                      :rules="dateRules"
                      readonly
                      filled
                      locale="current"
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
            </v-row>

            <v-row class="time justify-center mt-n4">
              <v-col sm="1" md="1">
                <v-icon class="mt-2" x-large>
                  mdi-clock-time-four-outline
                </v-icon>
              </v-col>

              <!--Start Time-->
              <v-col sm="4" md="4">
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
                      :rules="startTimeRules"
                      readonly
                      filled
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </template>

                  <v-time-picker
                    v-model="form.start_time"
                    header-color="primary"
                    @input="menu3 = false"
                    format="ampm"
                    scrollable
                  ></v-time-picker>
                </v-menu>
              </v-col>

              <!--End Time-->
              <v-col sm="4" md="4">
                <v-menu
                  v-model="menu4"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                  min-width="auto"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="form.end_time"
                      :rules="endTimeRules"
                      readonly
                      filled
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </template>

                  <v-time-picker
                    v-model="form.end_time"
                    header-color="primary"
                    @input="menu4 = false"
                    format="ampm"
                    scrollable
                  ></v-time-picker>
                </v-menu>
              </v-col>
            </v-row>

            <!--Location-->
            <v-row class="location justify-center mt-n4">
              <v-col sm="1" md="1">
                <v-icon class="mt-2" x-large> mdi-map-marker </v-icon>
              </v-col>

              <v-col sm="8" md="8">
                <v-text-field
                  id="input-6"
                  v-model="form.location"
                  filled
                  required
                ></v-text-field>
              </v-col>
            </v-row>

            <!--Details Section-->
            <v-row class="details justify-center mt-n4">
              <v-col sm="1" md="1">
                <v-icon class="mt-2" x-large>
                  mdi-clipboard-edit-outline
                </v-icon>
              </v-col>

              <v-col sm="8" md="8">
                <v-textarea
                  id="input-7"
                  v-model="form.details"
                  filled
                ></v-textarea>
              </v-col>
            </v-row>

            <!--Delete Button-->
            <v-row class="justify-center mt-n4" sm="2" md="2">
              <v-col sm="9" md="9">
                <v-dialog
                  v-model="dialog"
                  width="500"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      block
                      color="red"
                      dark
                      v-bind="attrs"
                      v-on="on"
                    >
                      <v-icon class="mr-2">mdi-delete</v-icon>
                      Delete Event
                    </v-btn>
                  </template>
                  <v-card>
                    <v-card-title class="justify-center ma-auto text-h4 red darken-2 white--text">
                      Confirm Delete
                    </v-card-title>

                    <v-card-text class="justify-center pa-12 text-h5">
                      Are you sure you want to delete this event?
                    </v-card-text>

                    <v-divider></v-divider>

                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        :disabled="loading"
                        class="ma-1"
                        color="grey"
                        plain
                        @click="dialog = false"
                      >
                        CANCEL
                      </v-btn>
                      <v-spacer></v-spacer>
                      <v-btn
                        :loading="loading"
                        class="ma-1"
                        color="red darken"
                        dark
                        @click="deleteEvent"
                      >
                        DELETE
                      </v-btn>
                      <v-spacer></v-spacer>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-col>
            </v-row>
          </v-card>

          <!--Save Changes FAB-->
          <v-btn x-large rounded class="ma-6" type="submit" color="green darken-2" dark
            absolute
            bottom
            right
            elevation="10"
            v-show="valid"
            >
              <v-icon class="mr-2">mdi-content-save</v-icon>
              Save Changes
          </v-btn>
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
        start_time: '',
        end_time: '',
        location: '',
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
      endTimeRules: [
        (v) => !!v || 'Must set an end time',
      ],
      subcategories: [
        { text: 'Select One', value: null },
        this.getSubcategories(),
      ],
      event: {},
      event_id: this.$route.query.event_id,
      show: true,
      fab: false,
      dialog: false,
      valid: false,
      // changes: false,
      menu2: false,
      menu3: false,
      menu4: false,
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
        end_time: this.form.end_time,
        location: this.form.location,
        details: this.form.details,
      };

      this.saveChanges(payload);
      this.initForm();
    },
    getEvent() {
      const path = `api/event/${this.event_id}`;
      axios
        .get(path)
        .then((res) => {
          this.event = res.data.data.event;
          this.form.name = this.event.name;
          this.form.subcategory = this.event.subcategory_id;
          this.form.date = this.event.date;
          this.form.start_time = this.event.start_time;
          this.form.end_time = this.event.end_time;
          this.form.location = this.event.location;
          this.form.details = this.event.details;
          console.log(res);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    saveChanges(payload) {
      const path = `api/event/${this.event_id}`;
      console.log(payload);
      axios
        .put(path, payload)
        .then((res) => {
          this.event_id = res.data.data.event.event_id;
          this.getEvent();
          this.$router.push('/home');
        })
        .catch((error) => {
          console.log(error);
          this.getEvent();
          this.$router.push('/error');
        });
    },
    deleteEvent() {
      // this.loading = true;
      const path = `api/event/${this.event_id}`;
      axios
        .delete(path)
        .then((res) => {
          console.log(res);
          // console.log('Reached here');
          this.returnHome();
        })
        .catch((error) => {
          console.log(error);
          this.$router.push('/error');
        });
      // this.loading = false;
    },
    getSubcategories() {
      const path = `api/subcategoriesNameId/${this.$store.getters.user.user}`;
      axios
        .get(path)
        .then((res) => {
          const subcat = res.data.data.subcategories;
          this.subcategories = Object.keys(subcat).map((k) => subcat[k]);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    printSuccess() {},
    initForm() {
      this.form.name = '';
      this.form.subcategory_id = null;
      this.form.date = '';
      this.form.start_time = '';
      this.form.end_time = '';
      this.form.location = '';
      this.form.details = '';
    },
    returnHome() {
      this.$router.push('/home');
    },
    validate() {
      this.$refs.form.validate();
    },
    formatDate(date) {
      if (!date) {
        return null;
      }

      const [year, month, day] = date.split('-');
      return `${month}/${day}/${year}`;
    },
  },
  mounted() {
    this.getEvent();
  },

};
</script>

<style scoped>
.subcategory select::placeholder{
  color: black!important;
}

</style>
