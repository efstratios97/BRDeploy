<template>
  <div>
    <Card class="component-card">
      <template v-slot:title> Time Horizon </template>
      <template v-slot:subtitle>
        Select Time Horizon for App Shut-Down</template
      >
      <template v-slot:content>
        <form class="overflow-auto">
          <Calendar
            v-model="selected_date"
            :showIcon="true"
            dateFormat="dd.mm.yy"
            @date-select="send_date()"
          />
        </form>
      </template>
    </Card>
  </div>
</template>
<script>
export default {
  data() {
    return {
      selected_date: "",
    };
  },
  methods: {
    send_date() {
      this.$emit("input-date", this.selected_date);
    },
  },
};
</script>
<style scoped>
.component-card {
  margin-top: 30px;
  position: relative;
  display: flex;
  table-layout: fixed;
  flex-grow: 1;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  background-color: #fff;
  background-clip: border-box;
  border-radius: 0.25rem;
  resize: both;
  overflow: auto;
  margin-right: 10px;
  margin-left: 10px;
  min-width: 100%;
}
</style>