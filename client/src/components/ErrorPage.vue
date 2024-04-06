<template>
  <v-container fluid class="purple lighten-5 fill-height">
    <v-row class="wrap">
      <v-col md="3" sm="3" class="ma-auto">
        <v-card class="rounded-lg pt-3">
          <v-row>
            <v-col>
              <v-card-title class="ml-6 mb-3 mt-5 display-2 font-weight-bold"
                >Error! </v-card-title
              >
            </v-col>
          </v-row>

          <v-row class="mt-n5">
            <v-card-actions class="ma-auto">
              <v-col>
                <v-btn
                  type="button"
                  color="blue"
                  dark
                  @click="returnHome()"
                  class="btn btn-success btn-sm"
                >
                  Return Home
                </v-btn>
              </v-col>
            </v-card-actions>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  methods: {
    returnHome() {
      this.$router.push('/home');
    },
  },
};
</script>
