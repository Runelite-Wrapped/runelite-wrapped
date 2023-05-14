<template>
  <div class="home">
    <img
      alt="Vue logo"
      src="../assets/runelite_wrapped_icon_wide.png"
      class="top-image"
    />
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
.top-image {
  width: 20%;
  top: 0;
  left: 0;
}

.main-container {
  display: grid;
  place-items: center;
}
</style>
