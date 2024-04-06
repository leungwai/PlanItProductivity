<template>
  <v-container fluid class="purple lighten-5 fill-height">
    <v-row id="content" class="wrap justify-center">
      <today-component :today="today_day"></today-component>

      <v-col class="hidden-xs-only" id="calendar-view" sm="8" md="8">
        <v-card class="rounded-lg pt-3" style="overflow: hidden">
          <v-sheet height="8vh">
            <v-toolbar flat>
              <v-btn
                absolute
                outlined
                class="mr-4 ml-3 mt-n3"
                color="grey darken-2"
                @click="setToday"
              >
                Today
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn fab text small color="grey darken-2 ma-0 mt-n4" @click="prev">
                <v-icon small> mdi-chevron-left </v-icon>
              </v-btn>

              <v-toolbar-title
                id="calendar-title"
                class="flex text-center text-h4 mt-n3"
                v-if="$refs.calendar"
              >
                {{ $refs.calendar.title }}
              </v-toolbar-title>

              <v-btn fab text small color="grey darken-2 mt-n4" @click="next">
                <v-icon small> mdi-chevron-right </v-icon>
              </v-btn>
              <v-spacer></v-spacer>
              <v-menu bottom right>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    absolute
                    right
                    outlined
                    color="grey darken-2"
                    class="mr-3 mt-n3"
                    v-bind="attrs"
                    v-on="on"
                  >
                    <span>{{ typeToLabel[type] }}</span>
                    <v-icon right> mdi-menu-down </v-icon>
                  </v-btn>
                </template>
                <v-list>
                  <v-list-item @click="type = 'week'">
                    <v-list-item-title>Week</v-list-item-title>
                  </v-list-item>
                  <v-list-item @click="type = 'month'">
                    <v-list-item-title>Month</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
            </v-toolbar>
          </v-sheet>
          <v-sheet height="81.5vh">
            <v-calendar
              ref="calendar"
              v-model="focus"
              color="primary"
              :events="events"
              :event-color="getEventColor"
              :type="type"
              @click:event="showEvent"
              @click:date="showDay"
              @change="updateRange"
            ></v-calendar>
          </v-sheet>
        </v-card>
      </v-col>
    </v-row>
    <v-speed-dial
      class="mr-5 mb-5"
      v-model="fab"
      absolute
      bottom
      right
      slide-y-reverse-transition
    >
      <template v-slot:activator>
        <v-fab-transition>
          <v-btn
            v-show="!hidden"
            v-if="fab"
            v-model="fab"
            color="red darken-2"
            dark
            fab
            elevation="10"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-btn
            x-large
            rounded
            color="green darken-2"
            dark
            v-else
            v-model="fab"
            elevation="10"
            height="56"
          >
            <v-icon class="mr-2">mdi-plus</v-icon>
            Create New
          </v-btn>
        </v-fab-transition>
      </template>
      <v-tooltip
        nudge-left="6"
        :disabled="tooltipsDisabled"
        left
        color="blue"
        :value="tooltips"
      >
        <template>
          <v-btn
            fab
            color="blue"
            dark
            small
            @click="goToCreateTask"
            slot="activator"
          >
            <v-icon>mdi-checkbox-marked-circle-plus-outline</v-icon>
          </v-btn>
        </template>
        <span>Create Task</span>
      </v-tooltip>
      <v-tooltip
        nudge-left="6"
        :disabled="tooltipsDisabled"
        left
        color="purple"
        :value="tooltips"
      >
        <template>
          <v-btn
            fab
            small
            dark
            @click="goToCreateEvent"
            color="purple"
            slot="activator"
          >
            <v-icon>mdi-calendar</v-icon>
          </v-btn>
        </template>
        <span>Create Event</span>
      </v-tooltip>
    </v-speed-dial>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      events: [],
      focus: '',
      type: 'month',
      typeToLabel: {
        month: 'Month',
        week: 'Week',
      },
      today_day: new Date(
        new Date().getTime() - new Date().getTimezoneOffset() * 60 * 1000,
      )
        .toISOString()
        .split('T')[0],
      today_events_tasks: [],
      fab: false,
      tooltips: true,
      tooltipsDisabled: false,
      cal: null,
    };
  },
  methods: {
    getEvents(start, end) {
      const path = 'api/eventsWithParams';
      const bodyParameters = {
        start_time: start,
        end_time: end,
        user: this.$store.getters.user.user,
      };
      axios
        .post(path, bodyParameters)
        .then((res) => {
          this.events = res.data.data.events;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getEventColor(event) {
      return event.color;
    },
    setToday() {
      this.focus = '';
    },
    prev() {
      this.$refs.calendar.prev();
    },
    next() {
      this.$refs.calendar.next();
    },
    showEvent({ event }) {
      console.log(event.event);
      if (typeof event.event !== 'undefined') {
        this.$router.push({
          name: 'ShowEvent',
          query: { event_id: event.event },
        });
      }
    },
    showDay(dayTime) {
      this.today_day = dayTime.date;
    },
    updateRange({ start, end }) {
      const min = start.date;
      const max = end.date;
      console.log(min);
      console.log(max);
      this.getEvents(min, max);
    },
    goToCreateTask() {
      this.$router.push('/createtask');
    },
    goToCreateEvent() {
      this.$router.push('/createevent');
    },
  },
};
</script>

<style scoped>
#today-card {
  height: 100%;
}

#calendar-card {
  height: 100vh;
}

#calendar-title {
  width: 300px;
  text-align: center;
}

/* .fab-text-custom {
  position: absolut;
  right: 50px;
  background-color: rgba(0, 0, 0, 0.5);
  padding: 10px;
  box-shadow: 0px 3px 5px -1px rgba(0, 0, 0, 0.2), 0px 6px 10px 0px rgba(0, 0, 0, 0.14),
  0px 1px 18px 0px rgba(0, 0, 0, 0.12);
  border-radius: 2px;
} */

/*
#calendar-view {
  height: 100vh;
  border: 5px solid blue;
}
*/
</style>
