<template>
  <div class="home">
    <div class="main-container">
      <StatSlideShow />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import StatSlideShow from "@/components/StatSlideShow.vue";

export default defineComponent({
  name: "HomeView",
  components: {
    StatSlideShow,
  },
});
</script>

<style lang="css" scoped>
.main-container {
  display: grid;
  place-items: center;
}
</style>
