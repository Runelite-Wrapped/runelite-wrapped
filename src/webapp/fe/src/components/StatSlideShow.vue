<template>
  <div class="slide-show-container">
    <div class="stat-container">
      <StatDisplay :stat="stats[current]" />
    </div>
  </div>
  <button @click="next">Next</button>
  <button @click="prev">Prev</button>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import StatDisplay from "@/components/StatDisplay.vue";

// TODO: get stats from backend
let stats = [
  {
    image: "https://oldschool.runescape.wiki/images/Hans.png?1a5c5",
    text: "You've played for:<br />100 hours",
  },
  {
    image: "https://oldschool.runescape.wiki/images/Goblin.png?3e49a",
    text: "Your most killed mob is:<br />Goblin",
  },
];

export default defineComponent({
  name: "StatSlideShow",
  components: {
    StatDisplay,
  },
  data() {
    return {
      current: 0,
      stats: stats,
    };
  },
  methods: {
    next() {
      this.current = (this.current + 1) % this.stats.length;
    },
    prev() {
      this.current = (this.current - 1 + this.stats.length) % this.stats.length;
    },
  },
});
</script>

<style lang="css" scoped>
.slide-show-container {
  /* allow children to stack */
  margin: 0px;
  height: 500px;
  width: 500px;
  /* center content */
  align-items: center;
  justify-content: center;
  position: relative;
}
</style>
