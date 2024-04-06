<template>
  <v-container fluid="sm">
    <v-jumbotron header="Today">
      <v-row class="event-header">
        <v-col sm="2" stickyColumn="true">
          <h1>Events</h1>
        </v-col>
        <v-col sm="10">
          <button
            type="button"
            @click="goCreateEvent"
            class="btn btn-success btn-sm"
            style="margin-top: 12px"
          >
            Add Event
          </button>
        </v-col>
      </v-row>

      <v-row class="event-table">
        <v-col sm="12" stickyColumn="true">
          <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">Name</th>
                <th scope="col">SubcategoryColor</th>
                <th scope="col">Date</th>
                <th scope="col">Start Time</th>
                <th scope="col">End Time</th>
                <th scope="col">Location</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(event, index) in events" :key="index">
                <td>{{ event.name }}</td>
                <td>{{ event.subcategory }}</td>
                <td>{{ event.date }}</td>
                <td>{{ event.start_time }}</td>
                <td>{{ event.end_time }}</td>
                <td>{{ event.location }}</td>
              </tr>
            </tbody>
          </table>
        </v-col>
      </v-row>

      <v-row class="task-header">
        <v-col sm="2" stickyColumn="true">
          <h1>Tasks</h1>
        </v-col>
        <v-col sm="10">
          <button
            type="button"
            @click="goCreateTask"
            class="btn btn-success btn-sm"
            style="margin-top: 12px"
          >
            Add Task
          </button>
        </v-col>
      </v-row>

      <v-row class="task-table">
        <v-col sm="12">
          <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">Name</th>
                <th scope="col">Subcategory</th>
                <th scope="col">Date</th>
                <th scope="col">Duration</th>
                <th scope="col">Start Time</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(task, index) in tasks" :key="index">
                <td>{{ task.name }}</td>
                <td>{{ task.subcategory }}</td>
                <td>{{ task.date }}</td>
                <td>{{ task.duration }}</td>
                <td>{{ task.start_time }}</td>
              </tr>
            </tbody>
          </table>
        </v-col>
      </v-row>
    </v-jumbotron>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      events: [],
      tasks: [],
      subcategories: [],
      subcategoriesColor: [],
    };
  },
  methods: {
    goCreateEvent() {
      this.$router.push('/createevent');
    },

    goCreateTask() {
      this.$router.push('/createtask');
    },

    getEvents() {
      const path = 'api/events';
      axios
        .get(path)
        .then((res) => {
          console.log(res.data.data.events);
          this.events = res.data.data.events;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getTasks() {
      const path = 'api/tasks';
      axios
        .get(path)
        .then((res) => {
          console.log(res.data.data.tasks);
          this.tasks = res.data.data.tasks;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getSubcategories() {
      const path = 'api/subcategoriesNameId';
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
    getSubcategoriesColor() {
      const path = 'api/getEvents';
      axios
        .get(path, {
          params: {
            data: this.events,
          },
        })
        .then((res) => {
          console.log(res);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  created() {
    this.getEvents();
    this.getTasks();
    this.getSubcategories();
    this.getSubcategoriesColor();
  },
};
</script>
