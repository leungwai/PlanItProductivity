<template>
  <v-col id="today-view" sm="3" md="3">
    <v-card class="rounded-lg pt-3" style="overflow: hidden">
      <v-sheet id="today-card" class="rounded-lg pt-3 mt-n7" height="93vh">
        <v-calendar
          ref="today_calendar"
          v-model="focus"
          color="primary"
          type="day"
          :events="today_events_tasks"
          :event-color="getEventColor"
          @change="updateToday"
          @click:event="showEvent"
        >
        <template v-slot:day-body>
          <div
            class="v-current-time"
            :class="{ first: true }"
            :style="{ top: nowY }"
          ></div>
        </template>
        </v-calendar>
      </v-sheet>
    </v-card>
  </v-col>
</template>

<script>
import axios from 'axios';

export default {
  props: ['today'],
  watch: {
    today: {
      async handler() {
        this.setToday();
      },
    },
  },
  data() {
    return {
      focus: '',
      today_day: new Date(new Date().getTime() - (new Date().getTimezoneOffset() * 60 * 1000)).toISOString().replace('T', ' ').substring(0, 19),
      today_events_tasks: [],
      cal: null,
    };
  },
  computed: {
    nowY() {
      return this.cal ? `${this.cal.timeToY(this.cal.times.now)}px` : '-10px';
    },
  },
  methods: {
    getCurrentTime() {
      return this.cal
        ? this.cal.times.now.hour * 60 + this.cal.times.now.minute
        : 0;
    },
    scrollToTime() {
      const time = this.getCurrentTime();
      const first = Math.max(0, time - (time % 30) - 30);

      this.cal.scrollToTime(first);
    },
    updateTime() {
      setInterval(() => this.cal.updateTimes(), 60 * 1000);
    },
    getEventColor(event) {
      return event.color;
    },
    // dateDiff(first, second) {
    //   return Math.round((second - first) / (1000 * 60 * 60 * 24));
    // },
    setToday() {
      let formatDay = new Date();
      const ymd = this.today.split('-');
      formatDay.setFullYear(ymd[0]);
      formatDay.setMonth(ymd[1] - 1);
      formatDay.setDate(ymd[2]);
      formatDay = new Date(formatDay.getTime() - (new Date().getTimezoneOffset() * 60 * 1000));
      this.focus = formatDay.toISOString().replace('T', ' ').substring(0, 19);
      this.today_day = this.focus;
      this.updateToday();
    },
    updateToday() {
      const path = 'api/eventsAndTasksWithParams';
      const bodyParameters = {
        start_time: this.today_day.split(' ')[0],
        end_time: this.today_day.split(' ')[0],
        user: this.$store.getters.user.user,
      };
      axios
        .post(path, bodyParameters)
        .then((res) => {
          this.today_events_tasks = res.data.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    showEvent({ event }) {
      console.log(event.task_id);
      if (typeof event.task_id !== 'undefined' && this.$route.query.task_id !== event.task_id) {
        this.$router.push({ name: 'ShowTask', query: { task_id: event.task_id } });
      } else if (this.$route.query.event_id !== event.event_id) {
        console.log(event.event_id);
        this.$router.push({ name: 'ShowEvent', query: { event_id: event.event_id } });
      }
    },
  },
  mounted() {
    console.log(this.today_day);
    this.cal = this.$refs.today_calendar;
    this.scrollToTime();
    this.updateTime();
  },
};
</script>

<style lang="scss">
.v-current-time {
  height: 2px;
  background-color: #ea4335;
  position: absolute;
  left: -1px;
  right: 0;
  pointer-events: none;
  &.first::before {
    content: '';
    position: absolute;
    background-color: #ea4335;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    margin-top: -5px;
    margin-left: -6.5px;
  }
}
</style>
