<!--
<script>
import axios from 'axios';

export default {
  props: ['subcategory'],
  data() {
    return {
      filterTasksAndEvents: [],
    };
  },
  methods: {
    getFilteredTasksAndEvents() {
      const path = 'api/eventsAndTasksBySubcategory';
      const bodyParameters = {
        start_time: this.today_day.split(' ')[0],
        end_time: this.today_day.split(' ')[0],
        user: this.$store.getters.user.user,
        subcategory: this.subcategory,
      };
      axios
        .post(path, bodyParameters)
        .then((res) => {
          this.filterTasksAndEvents = res.data.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
-->
