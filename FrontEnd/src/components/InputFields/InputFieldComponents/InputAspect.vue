<template>
  <div>
    <Card class="component-card">
      <template v-slot:title> Aspects </template>
      <template v-slot:subtitle> Select Aspects </template>
      <template v-slot:content>
        <form class="overflow-auto">
          <MultiSelect
            v-model="selected_aspects"
            :options="aspects"
            :filter="true"
            optionLabel="aspect.name"
            placeholder="Select Aspect"
            filterPlaceholder="Find an Aspect"
            @change="send_aspect()"
          />
        </form>
      </template>
    </Card>
  </div>
</template>
<script>
export default {
  props: ["selected_dataset_id", "selected_dataset_label"],
  data() {
    return {
      aspects: this.get_aspects(),
      selected_aspects: "",
    };
  },
  methods: {
    send_aspect() {
      this.$emit("input-aspect", this.selected_aspects);
    },
    get_aspects() {
      this.$axios
        .get("/get_aspects_by_dataset_label/" + this.selected_dataset_label)
        .then((res) => {
          var aspects_tmp = [];
          for (let index = 0; index < res.data.data.length; index++) {
            aspects_tmp.push({ aspect: res.data.data[index] });
          }
          this.aspects = aspects_tmp;
        });
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
  min-height: 175px;
}
</style>