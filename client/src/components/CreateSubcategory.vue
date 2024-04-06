<template>
  <v-container fluid class="teal lighten-5 fill-height">
    <v-row class="wrap justify-center">
      <today-component></today-component>

      <v-col md="8" sm="8">
        <v-form @submit="onSubmit">
          <v-card class="rounded-lg pt-3" height="91vh" style="overflow-y:scroll">
            <v-row>
              <v-col>
                <v-card-title class="ml-6 mb-3 mt-5 display-2 font-weight-bold"
                  >Create Subcategory</v-card-title
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
                  placeholder="Enter Subcategory Name"
                  required
                ></v-text-field>
              </v-col>
            </v-row>

            <v-row class="category justify-center">
              <v-col sm="1" md="1">
                <v-icon class="mt-2" x-large>
                  mdi-format-list-bulleted-type
                </v-icon>
              </v-col>

              <v-col sm="8" md="8">
                <v-select
                  v-model="form.category"
                  :items="categories"
                  placeholder="Select Category"
                  require
                  filled
                ></v-select>
              </v-col>
            </v-row>

            <v-row class="justify-center">
            <v-col sm="1" md="1">
                <v-icon class="mt-2" x-large>
                  mdi-palette
                </v-icon>
              </v-col>

            <v-col sm="8" md="8">
                <v-select
                  v-model="form.color"
                  :items="colors"
                  placeholder="Select Color"
                  require
                  filled
                  :color="form.color"
                ></v-select>
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
        category: '',
        color: '',
      },
      categories: [
        { text: 'Select One', value: null },
        this.getCategories(),
      ],
      colors: [
        'red',
        'purple',
        'indigo',
        'blue',
        'teal',
        'green',
        'yellow',
        'orange',
        'blue-grey',
        'grey',
      ],
    };
  },
  methods: {
    onSubmit(event) {
      event.preventDefault();
      const payload = {
        name: this.form.name,
        category_id: this.form.category,
        color: this.form.color,
      };
      this.addSubcategory(payload);
    },
    addSubcategory(payload) {
      const path = 'api/subcategories';
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
    getCategories() {
      const path = `api/categoriesNameId/${this.$store.getters.user.user}`;
      axios
        .get(path)
        .then((res) => {
          if (res.status === 200) {
            const cat = res.data.data.categories;
            this.categories = Object.keys(cat).map((k) => cat[k]);
            console.log(this.categories);
          } else {
            // direct user to add category first
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    initForm() {
      this.form.name = '';
      this.form.category = null;
      this.form.color = '';
    },
    returnHome() {
      this.$router.push('/home');
    },
  },
};
</script>
